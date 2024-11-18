# Dynamic Data Extractor

## Project Overview
The **Dynamic Data Extractor** is a **Streamlit-based web application** designed for efficient and user-friendly data extraction from datasets or the web. It enables users to extract specific information like **email addresses**, **phone numbers**, **physical addresses**, or results based on **custom queries**. The app supports **CSV files** and **Google Sheets** as data sources and integrates **SerpAPI** and **GroqAPI** for advanced web searches and query processing. Extracted data is displayed in an interactive dashboard with the option to export results as a CSV file.

---

## Features
1. **Flexible Data Sources**:  
   - Upload CSV files or connect Google Sheets effortlessly.
2. **Predefined Information Extraction**:  
   - Use regex filters for precise extraction of emails, phone numbers, and addresses.
3. **Custom Queries**:  
   - Define and execute tailored queries for specific data needs.
4. **Automated Web Search**:  
   - Perform dynamic searches using SerpAPI, enhanced by GroqAPI’s processing capabilities.
5. **Downloadable Output**:  
   - Export extracted data as a CSV file for further use.

---

## Installation and Setup

### Prerequisites
- **Python 3.8+**  
- **Streamlit**: Install via `pip install streamlit`.  
- **Google Cloud Service Account**: Required for Google Sheets integration.  
- **API Keys** for:
  - SerpAPI ([Get Key](https://serpapi.com/))
  - GroqAPI ([Get Key](https://console.groq.com/keys))

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/dynamic-data-extractor.git
   cd dynamic-data-extractor
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the project directory.
   - Add the following variables:
     ```
     SERPAPI_KEY=your_serpapi_key
     GROQ_API_KEY=your_groq_api_key
     ```
4. Configure Google Service Account:
   - Place your Google credentials file in the project directory and name it `dynamic_search.json`.
   - Ensure **Google Sheets API** is enabled for the service account.
5. Start the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage Guide

### 1. Select Data Source
- **Upload CSV**: Drag and drop or upload a CSV file.
- **Google Sheets**:  
  - Ensure the service account credentials (`dynamic_search.json`) are correctly placed.
  - Enter the **Google Sheet ID** (found in the URL: `https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit`).

### 2. Choose Extraction Method
- Select the column to extract data from.
- Choose the extraction type:
  - **Predefined Types**: Email, phone number, or address.
  - **Custom Prompt**: Enter a custom query with placeholders.

### Step 3: Perform Search and Extract
- Click "Extract Information" to initiate the process. 
- The application performs searches using SerpAPI, processes the results with LangChain, and applies regex filters (if applicable).

### 4. View and Download Results
- Review extracted data on the dashboard.
- Use the **Download Results as CSV** button to save results locally.

---

## Environment Variables and API Keys

### Required Variables
| Key              | Description                                     | Source                                         |
|-------------------|-------------------------------------------------|-----------------------------------------------|
| `SERPAPI_KEY`     | API key for SerpAPI                             | [SerpAPI](https://serpapi.com/)               |
| `GROQ_API_KEY`    | API key for Groq API (e.g., `llama3-8b-8192`)  | [GroqAPI](https://console.groq.com/keys)    |

### Google Service Account
- Place the **service account credentials JSON file** as `dynamic_search.json` in the project directory.
- Ensure the service account has access to the Google Sheets being used.

---

## Optional Features

### Predefined Information Types
- Leverages regex for high-accuracy extraction of emails, phone numbers, and addresses.

### Custom Prompt Flexibility
- Enables personalized queries with dynamic placeholders for versatile data extraction.

---

## Troubleshooting
- **Google Sheets Data Not Loading**:  
  - Verify the service account’s access to the Google Sheet.
  - Check if the correct Google credentials file (`dynamic_search.json`) is placed in the directory.
- **API Keys Not Found**:  
  - Ensure the `.env` file is correctly set up and loaded.
- **Unexpected Query Results**:  
  - Refine the custom query text for better precision.

---

## Future Enhancements
1. **Additional File Formats**: Support for Excel and JSON files.
2. **Enhanced Query Processing**: Integration with advanced NLP models for more robust custom queries.
3. **Multi-Language Support**: Enable data extraction in non-English languages.

---

Feel free to contribute to this project by submitting issues or pull requests. We appreciate your feedback and suggestions!
```