# Project-1-Data-pipeline-using-GCP
## Data pipeline Block diagram
![Block diagram](https://github.com/Chaland0/Project-1-Data-pipeline-using-GCP/blob/main/Blockdiagram.png)

## Project Description
The Data Analyst has requested a dashboard report that presents three key metrics: Book's Revenue by Country, Revenue of each title book, and Revenue of each Category. The purpose of this dashboard is to provide a comprehensive overview of the financial performance of books based on these different dimensions.
Then, we have create Data Pipeline that can.
- Load data and transaction tables (But the transaction is in dollars, we want it to show in baht).
- Load conversion_rate (for convert dollars to Thai baht)
- Merge transaction and conversion_rate
- Load that final data to Data Warehouse
- Query final data for create Dashboard report

## DAG View:
![DAGS](https://github.com/Chaland0/Project-1-Data-pipeline-using-GCP/blob/main/DAGS.png)
Using **Cloud Composer** to upload pipeline code [Data_Pipeline.py](https://github.com/Chaland0/Project-1-Data-pipeline-using-GCP/blob/main/Data_Pipeline.py) and run DAGS as Apache Airflow.

### First DAG:
- Collected data (audible_data, audible_transaction) from MySQL database by using `SQLHook` and read by `pandas`
- join table by Book id and save (audible_data_merged.csv) to **Cloud Storage**

### Second DAG:
- Data Collected from the API (conversion_rate) by using `requests.get`
- transform data .jon to Data frame
- reset index to date column and save (conversion_rate.csv) to Cloud Storage

### Third DAG:
- Use `pandas.read_csv` to get 2 data from 1st dag and 2nd dag
- Merge 2 data by `left_on="date", right_on="date"` 
- Remove the "$" sign from Price column
- Multiple Price column by conversion_rate column for convert dollars to Thai baht and save (output.csv) to Cloud Storage

### Fourth DAG:
- Use Bash operator for load data (output.csv) from Cloud Storage to **Bigquery**

## Create Dashboard
- Create View by using SQL for avoid sensitive data and Query only the necessary information
- Connect Bigquery data set for Data source to **Looker Studio**
- Create Dashboard report requested by the Data Analyst, as shown in the image below.
![Dashborrd_Report](https://github.com/Chaland0/Project-1-Data-pipeline-using-GCP/blob/main/Dashborrd_Report.png)



#### Data Source
Have two data source MySQL and web API

#### Data Lake
Use Cloud Storage for store raw data

#### Data Warehouse
Use Bigquery for load final data and query

#### Data Visualization
Use Looker Studio (Google Dat Studio) query data from Bigquery to create Dash Board Report 


credit data from [DATATH](https://www.facebook.com/datasciencechill/)