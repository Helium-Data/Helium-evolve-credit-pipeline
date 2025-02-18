# helium-evolve-credit Data Pipeline


### Overview
This project is designed to extract data from an API, transform it into a structured format using Pandas, and load it into Google BigQuery. The script fetches financial data related to loans, disbursements, and repayments across multiple product categories.

### Project Workflow
- Authenticate with API using a token from config.py.
- Fetch data from the API dynamically based on product and dataset names.
- Normalize and clean the data using Pandas.
- Store the data in a CSV file (output.csv) for debugging.
- Load the cleaned data into BigQuery, excluding unnecessary columns.
- Repeat the process for multiple product datasets (Evolve Credit, MSD, Portfolio).
- The business logic transformation queries is saved and scheduled on bigquery as "helium evolve credit", "helium evolve credit external"


## Requirements

### 1. Python Libraries
Ensure you have the required dependencies installed:
```
pip install pandas google-cloud-bigquery requests
```

### 2. API Token Configuration
Create a config.py file with the following content:
```
token = "YOUR_API_TOKEN_HERE"
```

### 3. Google Cloud Authentication
Download your Google Cloud Service Account Key (heliumhealth-1ce77f433fc7.json) and store it in the project directory.


## Project Structure
```
/project-directory
│── helium-evolve-credit.py          # Main script
│── config.py                        # Stores API authentication token
│── heliumhealth-1ce77f433fc7.json   # Google Cloud authentication file
│── output.csv                       # (Generated) CSV file with fetched data
│── README.md                        # Documentation
```

## Usage
Run the script using:
```
python helium-evolve-credit.py
```

## Key Functions
### 1. get_total_records(name, productid, headers)
- Retrieves the total number of records available for a given dataset.
### 2. pull_and_insert(name, productid, tablename, headers)
- Fetches all records for a dataset.
- Cleans the data and drops unnecessary columns.
- Loads the transformed data into BigQuery.
### 3. main execution
- Runs the pull_and_insert function for multiple datasets across three product categories.


## BigQuery Integration
The script loads data into BigQuery tables below under the src_helium_evolve_credit dataset.

- stg_loan_request_general
- stg_disbursement_msd
- stg_repayment_portfolio

Before inserting new data, it drops any existing table with the same name.

## Troubleshooting
### API Errors
If the script fails to fetch data, check:

- The API token in config.py.
- Whether the API endpoint is reachable.


## Future Improvements
- Add error handling & logging for better debugging.
- Implement incremental loading to avoid dropping tables.
