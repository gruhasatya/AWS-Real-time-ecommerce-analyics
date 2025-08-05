import boto3
import json
import base64
import uuid
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = 'ecommerce-product-data-bhaskar'
prefix = 'bronze/raw-events'

def lambda_handler(event, context):
    if 'Records' not in event:
        return {
            'statusCode': 400,
            'body': 'No Records found in event payload'
        }

    for record in event['Records']:
        payload = record['kinesis']['data']
        decoded_data = json.loads(base64.b64decode(payload).decode('utf-8'))

        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        unique_id = str(uuid.uuid4())
        s3_key = f"{prefix}/{timestamp}_{unique_id}.json"

        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(decoded_data),
            ContentType='application/json'
        )

    return {
        'statusCode': 200,
        'body': f"Archived {len(event['Records'])} records to S3"
    }
