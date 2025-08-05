import base64
import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ecommerce_dedup_table')

def convert_floats(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats(i) for i in obj]
    else:
        return obj

def lambda_handler(event, context):
    print(f"📥 Received {len(event['Records'])} records")

    for record in event['Records']:
        try:
            payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
            data = json.loads(payload)

            data = convert_floats(data)

            table.put_item(
                Item={
                    'transaction_id': data['transaction_id'],
                    'product_id': data['product_id'],
                    'data': data
                },
                ConditionExpression='attribute_not_exists(transaction_id) AND attribute_not_exists(product_id)'
            )

            print(f"✅ Stored: {data['transaction_id']} | {data['product_id']}")

        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                print(f"⚠️ Duplicate: {data['transaction_id']} | {data['product_id']}")
            else:
                print("❌ DynamoDB error:", e)

        except Exception as e:
            print("❌ Error:", e)

    return {
        'statusCode': 200,
        'body': f"Processed {len(event['Records'])} records"
    }
