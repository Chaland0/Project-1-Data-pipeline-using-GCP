from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests

MYSQL_CONNECTION = "mysql_default"

def get_data_from_mysql(transaction_path):
    mysqlserver = MySqlHook(MYSQL_CONNECTION)
    
    audible_data = mysqlserver.get_pandas_df(
        sql="SELECT * FROM audible_data")
    audible_transaction = mysqlserver.get_pandas_df(
        sql="SELECT * FROM audible_transaction")
    
    df = audible_transaction.merge(audible_data, how="left", left_on="book_id", right_on="Book_ID")
    df.to_csv(transaction_path, index=False)
    print(f"Output to {transaction_path}")

def get_conversion_rate(conversion_rate_path):
    r = requests.get("https://r2de2-workshop-vmftiryt6q-ts.a.run.app/usd_thb_conversion_rate")
    result_conversion_rate = r.json()
    df = pd.DataFrame(result_conversion_rate)
    
    df=df.reset_index().rename(columns={"index": "date"})
    df.to_csv(conversion_rate_path, index= False)
    print(f"Output to {conversion_rate_path}")
    
def merge_data(transaction_path, conversion_rate_path, output_path):
    transaction = pd.read_csv(transaction_path)
    conversion_rate = pd.read_csv(conversion_rate_path)
    
    transaction['date'] = transaction['timestamp']
    transaction['date'] = pd.to_datetime(transaction['date']).dt.date
    conversion_rate['date'] = pd.to_datetime(conversion_rate['date']).dt.date
    
    final_df = transaction.merge(conversion_rate, how='left', left_on="date", right_on='date')
    
    final_df['Price'] = final_df.apply(lambda x: x["Price"].replace("$",""),axis=1)
    final_df['Price'] = final_df["Price"].astype(float)
    final_df["THBPrice"] = final_df["Price"]*final_df["conversion_rate"]
    final_df = final_df.drop(["date","book_id"], axis=1)
    
    final_df.to_csv(output_path, inndex=False)
    print(f"Output to {output_path}")
    print("==== END ====")
    
with DAG(
    "Project1_ETL",
    start_date=days_ago(1),
    schedule_intrerval="@once"
    
) as dag:
    t1 = PythonOperator(
        task_id="Extract_from_mysql",
        python_callable=get_data_from_mysql,
        op_kwargs={"transaction_path": "/home/airflow/gcs/data/audible_data_merged.csv"}
    )
    
    t2 = PythonOperator(
        task_id="Extract_conversion_Rate",
        python_callable=get_conversion_rate,
        op_kwargs={"conversion_rate_path": "/home/airflow/gcs/data/conversion_rate.csv"}
    )
    
    t3 = PythonOperator(
        task_id="Merge_Data",
        python_callable=merge_data,
        op_kwargs={
            "transaction_path": "/home/airflow/gcs/data/audible_data_merged.csv",
            "conversion_rate_path": "/home/airflow/gcs/data/conversion_rate.csv", 
            "output_path": "/home/airflow/gcs/data/output.csv"}
    )
    
    t4 = BashOperator(
        task_id="Load_to_BigQuery",
        bash_command="bq load \
            --source_format=CSV \
            --autodetect \
            workshop.Prepared_data \
            gs://asia-east2-workshop5-03d65f08-bucket/data/output.csv"
    )

    [t1, t2] >> t3 >> t4
    


