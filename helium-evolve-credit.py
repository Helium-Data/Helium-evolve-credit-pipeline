# Load Library
import json
import requests
import config
import os
import pandas as pd

from pandas import json_normalize 
from datetime import datetime
from google.cloud import bigquery


# Authenticating token from config file. 
# token = config.token
token = os.getenv("SECRET_TOKEN")

# Using the token to create header parameter for the API get request
headers={'Authorization': f'Bearer {token}'}


# Connect to bigquery through keyfile 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.getcwd()) +'/heliumhealth-1ce77f433fc7.json'
storage_client = bigquery.Client.from_service_account_json(os.path.abspath(os.getcwd()) +'/heliumhealth-1ce77f433fc7.json')




# Function to get the total number of records
def get_total_records(name, productid, headers):
    url = f"http://configure-abierta.herokuapp.com/api/v1/{name}?product-id={productid}&per-page=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}, status code: {response.status_code}")

    try:
        total_records = response.json()['data1']['total']
        return total_records
    except KeyError:
        raise KeyError("The key 'data1' or 'total' was not found in the response. Please check the response structure.")

# Function to get and insert all datasets into database
def pull_and_insert(name, productid, tablename, headers):
    total_records = get_total_records(name, productid, headers)
    
    url = f"http://configure-abierta.herokuapp.com/api/v1/{name}?product-id={productid}&per-page={total_records}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}, status code: {response.status_code}")

    full_data = response.json().get('data', [])

    # Load into dataframe
    df = pd.json_normalize(full_data)
    df = df.rename(columns=lambda x: x.strip().lower().replace(".", '_').replace(f"{name}_info_", ''))
    df.to_csv('output.csv', index=False)

    # # Print the dataframe for debugging
    # print(df.head())

    # Uncomment the following lines to load into BigQuery
    # Exclude columns you don't want to include in BigQuery
    columns_to_exclude = ['lead_reference']
    for column in columns_to_exclude:
        if column in df.columns:
            df = df.drop(columns=column)
        
    # Load into BigQuery
    sql = f"DROP TABLE IF EXISTS src_helium_evolve_credit.stg_{tablename}"
    storage_client.query(sql)

    table_id = f'src_helium_evolve_credit.stg_{tablename}'

    job_config = bigquery.LoadJobConfig(schema=[
        bigquery.SchemaField("id", "STRING"),
    ])
    job = storage_client.load_table_from_dataframe(df, table_id, job_config=job_config)


# Function call to insert data into db
if __name__ == "__main__":
    
    # evolve credit
    pull_and_insert(name='loan_request',productid=20,tablename='loan_request_general', headers=headers)
    pull_and_insert(name='disbursement',productid=20,tablename='disbursement_general', headers=headers)
    pull_and_insert(name='repayment',productid=20,tablename='repayment_general', headers=headers)
    
    # evolve MSD
    pull_and_insert(name='loan_request',productid=290,tablename='loan_request_msd', headers=headers)
    pull_and_insert(name='disbursement',productid=290,tablename='disbursement_msd', headers=headers)
    pull_and_insert(name='repayment',productid=290,tablename='repayment_msd', headers=headers)

     # evolve Portfolio
    pull_and_insert(name='loan_request',productid=105,tablename='loan_request_portfolio', headers=headers)
    pull_and_insert(name='disbursement',productid=105,tablename='disbursement_portfolio', headers=headers)
    pull_and_insert(name='repayment',productid=105,tablename='repayment_portfolio', headers=headers)



    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("run date:", dt_string)
