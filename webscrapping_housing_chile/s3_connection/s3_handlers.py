import boto3
import io
import pandas as pd

def s3_connection():
    s3 = boto3.client(
        's3',
        aws_access_key_id='XXXXX',
        aws_secret_access_key='XXXXX',
    )
    return s3

def get_df_url(s3, date_extract, file):
    obj = s3.get_object(Bucket='url-scrapper', Key= f'partition_date={date_extract}/{file}/urls.csv') 
    return pd.read_csv(obj['Body'])


def write_csv_s3(s3, bucket, df, partition, folder):
    if bucket == 'features_scrapper':
        key = f"v2/{folder}/partition_date={partition}/urls.csv"
    else:
        key = f"v2/partition_date={partition}/{folder}/urls.csv"
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)
        response = s3.put_object(
            Bucket=bucket, Key=key, Body=csv_buffer.getvalue()
        )
    
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    
        if status == 200:
            return print(f"Successful S3 put_object response. Status - {status}")
        else:
            return print(f"Unsuccessful S3 put_object response. Status - {status}")
        