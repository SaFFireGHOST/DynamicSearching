import streamlit as st
from google.oauth2.service_account import Credentials
import pandas as pd
import json
from googleapiclient.discovery import build
import re
from serpapi import GoogleSearch
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from io import BytesIO
from dotenv import load_dotenv
# Set up API keys
load_dotenv()
# Access API keys
serpapi_key = os.getenv("SERPAPI_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM model
model = ChatGroq(model="llama3-8b-8192")

# Define regex patterns for dynamic extraction
patterns = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "address": r"[0-9]{1,5}\s\w+(?:\s\w+)*,\s\w+(?:\s\w+)*,\s\w+(?:\s\w+)*",
    "phone number": r"(\+?\d{1,3}?[-.\s]??\(?\d{1,4}?\)?[-.\s]??\d{1,4}[-.\s]??\d{1,9})",
}

# Session state initialization for credentials and other variables
if "credentials" not in st.session_state:
    st.session_state["credentials"] = None

if "output_data" not in st.session_state:
    st.session_state["output_data"] = None

if "data_source" not in st.session_state:
    st.session_state["data_source"] = None

if "sheet_id" not in st.session_state:
    st.session_state["sheet_id"] = None

st.title("Dynamic Data Extractor")

# Let the user choose a data source
data_source = st.radio("Select a data source:", ["Upload CSV", "Google Sheets"])
st.session_state["data_source"] = data_source  # Store data_source in session state
# Debugging data source
# print(f"Data source selected: {data_source}")

data = None  # Initialize `data` variable

if st.session_state["data_source"] is not None:
    data_source = st.session_state["data_source"]
   

if data_source == "Upload CSV":
    # File uploader for CSV files
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

    if uploaded_file:
        # Load CSV file
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.dataframe(data)

elif data_source == "Google Sheets":
    # Load the service account credentials from the file
        with open("dynamic_search.json", "r") as file:
            uploaded_credentials_data = json.load(file)

        # Parse and store credentials in session state
        # uploaded_credentials_data = json.load(uploaded_credentials)
        st.session_state["credentials"] = uploaded_credentials_data

        # Initialize Google Credentials object
        creds = Credentials.from_service_account_info(st.session_state["credentials"])
        st.success("Google Service Account credentials loaded successfully!")

        # Ask for Google Sheet ID and range
        sheet_id = st.text_input("Enter the Google Sheet ID:")
        st.session_state["sheet_id"] = sheet_id  # Store sheet_id in session state
        # sheet_range = st.text_input("Enter the range (e.g., Sheet1!A1:Z100):")
        # sheet_range="Sheet1"
        if st.button("Load Google Sheet Data"):
            if sheet_id:
                try:
                    # Access the Google Sheets API
                    service = build('sheets', 'v4', credentials=creds)
                    sheet = service.spreadsheets()
                    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1").execute()
                    values = result.get('values', [])

                    # Convert to a DataFrame for display
                    if values:
                        data = pd.DataFrame(values[1:], columns=values[0])  # Assuming first row is headers
                        st.session_state["google_sheet_data"] = data  # Save to session state
                        # st.write("### Google Sheet Data Preview")
                        # st.dataframe(data)
                    else:
                        st.warning("No data found in the specified range.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter the Google Sheet ID")

# Retrieve the data from session state if it exists
        if "google_sheet_data" in st.session_state:
            data = st.session_state["google_sheet_data"]
            st.write("### Google Sheet Data Preview")
            st.dataframe(data)
# Proceed with extraction if data is available
if data is not None:
    # Allow user to select a column
    selected_column = st.selectbox("Select the column to use for queries", data.columns)

    # Allow user to choose type of information to extract or define a custom prompt
    info_type = st.selectbox(
    "Select the type of information to extract or define a custom prompt",
    ["email", "address", "phone number", "Custom Prompt"])

    custom_prompt = ""
    if info_type == "Custom Prompt":
        custom_prompt = st.text_area(
    """
    Define your custom prompt using placeholders. A placeholder (like {company}) will automatically be replaced with 
    the value from each row in the selected column.

    For example:
    - If the selected column contains company names like 'Google' and 'Microsoft,' and you write:
      'Get me the email address of {company} company'

    It will turn into:
    - 'Get me the email address of Google company'
    - 'Get me the email address of Microsoft company'

    This lets you write one prompt that works for all rows in the selected column!
    """
)


    if st.button("Extract Information"):
        if not serpapi_key or not groq_api_key:
            st.error("Please provide both SerpAPI and Groq API keys.")
        else:
            # Prepare to store results
            company_results = []

            

            # Loop through each entry in the selected column
            for entry in data[selected_column]:
                # Create query from predefined types or custom prompt
                if info_type == "Custom Prompt" and custom_prompt:
                # Replace placeholders in custom prompt
                    query = custom_prompt.format(company=entry)
                    system_message = SystemMessage(content=f"Extract the requested information accurately based on the query. Ensure the output is clear, relevant, and practical.")
                else:
                    query = f"{info_type.capitalize()} of {entry} {selected_column.capitalize()}"
                    # Update the system message dynamically
                    system_message = SystemMessage(content=f"Extract only the valid and specific {info_type}s from the provided JSON search results. Exclude generic patterns, placeholder formats, or incomplete entries. Ensure the extracted {info_type}s are accurate, unique, and suitable for practical use.")

                # Query parameters for SerpAPI
                params = {
                "engine": "google",
                "q": query,
                "api_key": serpapi_key,
                }

                # Perform Google search using SerpAPI
                search = GoogleSearch(params)
                results = search.get_dict()
                print(results,'/n')
                # Check if organic results are available
                organic_results = results.get("organic_results", [])
                if organic_results:
                    # Send the results to LangChain
                    json_content = f"JSON search results: {organic_results}"
                    messages = [
                        system_message,
                        HumanMessage(content=json_content),
                    ]
                    # Get the response using LangChain
                    response = model.invoke(messages)
                    # For predefined types, use regex to extract
                    if info_type != "Custom Prompt":
                        extracted_info = re.findall(patterns[info_type], response.content)
                        result_list = ", ".join(extracted_info)
                        company_results.append({"entry": entry, info_type: result_list if result_list else f"No {info_type} found"})
                    else:
                    # For custom prompt, take LangChain's direct response
                        result_list = response.content.strip()
                        company_results.append({"entry": entry, "result": result_list if result_list else "No relevant information found"})
                        
                  
                    
                else:
                    company_results.append({"entry": entry, info_type: f"No results found"})
           
                # Convert results to a DataFrame
            output_df = pd.DataFrame(company_results)
            st.session_state["output_data"] = output_df  # Save to session state


            if st.session_state["output_data"] is not None:
                output_df = st.session_state["output_data"]
                st.write("### Extraction Results")
                st.dataframe(output_df)    



            # Prepare CSV for download
            csv_buffer = BytesIO()
            output_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(
                label="Download Results as CSV",
                data=csv_buffer,
                file_name=f"extracted_{info_type}.csv",
                mime="text/csv",
            )
