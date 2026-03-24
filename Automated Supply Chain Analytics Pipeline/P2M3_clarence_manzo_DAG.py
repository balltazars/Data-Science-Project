'''
=================================================
Milestone 3: Automated Supply Chain Analytics Pipeline

Nama  : Clarence Manzo
Batch : FTDS-036-HCK

Program ini dibuat untuk mengambil data dari PostgreSQL, lalu data cleaning dan menyimpan data yang sudah bersih ke CSV file, dan memasukkannya
ke elasticsearch menggunakan Apache Airflow.

Dataset yang digunakan adalah data operasional supply chain yang berisi mengenai produk, penjualan, produksi, serta distribusi logistik.
Data mencakup atribut seperti SKU, tipe produk, harga, tingkat ketersediaan dan stok, jumlah produk terjual, serta revenue.
Selain itu, dataset ini berisi informasi produksi, shipping time, shipping cost, shipping carrier, transportation mode, dan rute pengiriman.
'''

# Import database connectivity library
import psycopg2

# Import data processing libraries
import pandas as pd
import re

# Import date & time utilities libarires
import datetime as dt
import pendulum

# Import airflow libraries
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import elasticsearch libraries
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def fromPostgre():
    '''
    Fungsi ini digunakan untuk mengambil data dari PostgreSQL dengan query SQL dan menyimpannya ke dalam CSV file.
        
    Contoh penggunaan:
    PythonOperator(task_id='fetch_from_postgre', python_callable=fromPostgre)
    '''
    # Establish connection to PostgreSQL database
    conn = psycopg2.connect(
        host="postgres",
        database="postgres",
        user="airflow",
        password="airflow",
        port = 5432
    )
    
    # Load SQL query result to dataframe and save to CSV file
    data = pd.read_sql_query("SELECT * FROM table_m3;", conn)
    data.to_csv('/opt/airflow/dags/P2M3_clarence_manzo_data_raw.csv', index=False)

    # Close database connection
    conn.close()

def cleanData():
    '''
    Fungsi ini digunakan untuk membersihkan data seperti menghapus data duplikat, mengubah nama kolom, dan mengatasi missing values. Setelah
    itu data yang sudah bersih akan disimpan ke dalam CSV file yang baru.
        
    Contoh penggunaan:
    PythonOperator(task_id='clean_data', python_callable=cleanData)
    '''
    # Read csv to dataframe
    df = pd.read_csv('/opt/airflow/dags/P2M3_clarence_manzo_data_raw.csv')

    # Remove duplicates
    df = df.drop_duplicates()

    # Normalize column names
    def clean_column(col):
        '''
        Fungsi ini digunakan untuk mengubah nama kolom menjadi huruf kecil, menghapus spasi di depan/belakang, menghapus simbol, serta
        menggantikan spasi antar kata dengan underscore.

        Parameters:
            col: string - nama kolom
        
        Return:
            col: string - nama kolom
            
        Contoh penggunaan:
        df.columns.values[0] = clean_column(df.columns[0])
        '''
        col = col.lower().strip() # Convert to lower case and remove leading/trailing white spaces
        col = re.sub(r"[^\w\s]", "", col) # Remove symbols except underscore
        col = re.sub(r"\s+", "_", col) # Replace white space with underscore
        return col
    
    df.columns = [clean_column(col) for col in df.columns]
    
    # Replace only white space cell into NaN
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

    # Handle missing values
    for col in df.select_dtypes(include=['float64','int64']).columns:
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Save cleaned data
    df.to_csv('/opt/airflow/dags/P2M3_clarence_manzo_data_clean.csv', index=False)

def postToElastic():
    '''
    Fungsi ini digunakan untuk load data yang sudah bersih, merubahnya ke format json, dan memasukkan ke Elasticsearch.
        
    Contoh penggunaan:
    PythonOperator(task_id='post_to_elasticsearch', python_callable=postToElastic)
    '''
    # Initialize elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")

    # Read csv to dataframe
    df = pd.read_csv('/opt/airflow/dags/P2M3_clarence_manzo_data_clean.csv')

    # Convert dataframe into json format
    actions = [
        {
            "_index": "p2m3_clarence_manzo_data_clean",
            "_source": r.to_json()
        }
        for i, r in df.iterrows()
    ]

    # Bulk insert
    helpers.bulk(es, actions)

# Default arguments
default_args = {
    'owner': 'manzo',
    'start_date': dt.datetime(2024, 11, 1, 9, 10, tzinfo=pendulum.timezone("Asia/Jakarta")), # Start from 01 November 2024 09:10 AM
    'retries': 1,
    'retry_delay': dt.timedelta(seconds=30),
}

# Define DAG called P2M3_weekly_pipeline with interval of 10 minutes every saturday 09:10-09:30 AM
with DAG('P2M3_weekly_pipeline', default_args=default_args, schedule_interval='10-30/10 9 * * 6', catchup=False) as dag:
    # Node to fetch data from PostGreSQL
    fetch_postgre = PythonOperator(task_id='fetch_from_postgre', python_callable=fromPostgre)

    # Node to clean data and save cleaned data to CSV
    clean_data = PythonOperator(task_id='clean_data', python_callable=cleanData)

    # Node to load cleaned CSV and post to Elasticsearch
    post_to_elasticsearch = PythonOperator(task_id='post_to_elasticsearch', python_callable=postToElastic)

# Define pipeline
fetch_postgre >> clean_data >> post_to_elasticsearch