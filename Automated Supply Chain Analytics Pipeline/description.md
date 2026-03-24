# Automated Supply Chain Analytics Pipeline

## Repository Outline
1. images - A folder containing all screenshots related to Kibana dashboard  
   1.1 introduction & objective - A screenshot of identification with dashboard's background and objectives  
   1.2 kesimpulan - A screenshot of analysis conclusion along with the business insight  
   1.3 plot & insight 01 - A screenshot of chart 1 with its insight  
   1.4 plot & insight 02 - A screenshot of chart 2 with its insight  
   1.5 plot & insight 03 - A screenshot of chart 3 with its insight  
   1.6 plot & insight 04 - A screenshot of chart 4 with its insight  
   1.7 plot & insight 05 - A screenshot of chart 5 with its insight  
   1.8 plot & insight 06 - A screenshot of chart 6 with its insight  
2. P2M3_clarence_manzo_DAG.py - Main notebook containing DAG of extracting data from PostgreSQL, clean data and save to CSV, and insert it into Elasticsearch 
3. P2M3_clarence_manzo_DAG_graph.jpg - A screenshot of DAG flow graph
4. P2M3_clarence_manzo_GX.ipynb - Notebook to do validation data with Expectations
5. P2M3_clarence_manzo_conceptual.txt - A text file containing conceptual problem's answers
6. P2M3_clarence_manzo_data_clean.csv - A CSV file containing the cleaned dataset
7. P2M3_clarence_manzo_data_raw.csv - A CSV file containing the original dataset
8. P2M3_clarence_manzo_ddl.txt - A text file containing dataset URL, DDL syntax for table creation, and DML syntax for data insertion to database
9. README.md - Summary description about the project
10. description.md - Repository project description and documentation

## Problem Background
Management often struggles to gain a consolidated view of operations because data are stored in separate systems and reviewed independently. As the business expands, decision-making becomes difficult. Inventory shortages occur, logistics costs fluctuate without clear justification, and inefficient production is unnoticed. Therefore, leadership needs a centralized report to integrate operational and commercial metrics into a single and structured view.

## Project Output
A kibana dashboard containing data analysis with its business recommendations

## Data
The dataset used is a supply chain data containing information on products, sales, production, and logistics distribution. The data includes SKU attributes, product type, price, availability and stock levels, number of products sold, and revenue. In addition, this dataset contains information on production, shipping times, shipping costs, shipping carriers, transportation modes, and shipping routes.

## Method
1. Database: PostgreSQL
2. Handle missing values: median imputation and mode imputation
3. Data validation: Great expectations
4. Dashboard: Kibana

## Stacks
Programming langugage: SQL and Python

Tools: Visual Studio Code, PostgreSQL, Docker, Airflow, and Kibana

Library: psycopg2, pandas, re, datetime, pendulum, airflow, elasticsearch, great_expectations

## Reference  
Dataset URL: https://www.kaggle.com/datasets/aminasalamt/supply-chain-analysis-dataset

---
