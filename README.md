# Project-1-Data-pipeline-using-GCP
## Data pipeline Block diagram
![Block diagram](https://github.com/Chaland0/Project-1-Data-pipeline-using-GCP/blob/main/Blockdiagram.png)

## Project Description
The Data Analyst has requested a dashboard report that presents three key metrics: Book's Revenue by Country, Revenue of each title book, and Revenue of each Category. The purpose of this dashboard is to provide a comprehensive overview of the financial performance of books based on these different dimensions.
Then, we have create Data Pipeline that can.
- Load data and transaction tables (But the transaction is in dollars, we want it to show in baht).
- Load conversion_rate (for convert dollars to baht)
- Merge transaction and conversion_rate
- Load that final data to Data Warehouse
- Query final data for create Dashboard report

### First DAG:
- Download data (audible_data, audible_transaction) from MySQL database
- Data Collected from the API




### Data Source
Have two data source MySQL and web API

### Data Lake
Use Cloud Storage for store raw data

### Data Warehouse
Use Bigquery for load final data and query

### Data Visualization
Use Looker Studio (Google Dat Studio) query data from Bigquery to create Dash Board Report 


credit data from [DATATH](https://www.facebook.com/datasciencechill/)