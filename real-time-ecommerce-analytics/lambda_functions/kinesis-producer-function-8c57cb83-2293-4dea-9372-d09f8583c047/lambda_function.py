import boto3
import json
import time
import urllib.request

s3 = boto3.client('s3')
kinesis = boto3.client('kinesis')

BUCKET_NAME = 'ecommerce-product-data-bhaskar'
OBJECT_KEY = 'product_events.json'
STREAM_NAME = 'ecommerce-product-stream'

def lambda_handler(event, context):
    # Read the JSON file from S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
    content = response['Body'].read().decode('utf-8')
    records = json.loads(content)

    for record in records:
        # Send each record to Kinesis
        kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(record),
            PartitionKey=record['transaction_id']
        )
        time.sleep(0.3)

    return {
        'statusCode': 200,
        'body': f'Sent {len(records)} records to {STREAM_NAME}'
    }
