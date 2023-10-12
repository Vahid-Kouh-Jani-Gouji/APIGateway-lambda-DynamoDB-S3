import json
import boto3
import os
from uuid import uuid4

# Initialize the DynamoDB and S3 clients
dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
s3 = boto3.client('s3', region_name='eu-central-1')

# Define the DynamoDB table name and S3 bucket name
dynamodb_table = 'serverlessapp'
s3_bucket = 'serverlesswebappimage'

def lambda_handler(event, context):
    # Ensure that the 'body' key exists in the event and is not None
    if 'body' not in event or event['body'] is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request body"})
        }

    # Parse the incoming JSON payload (which includes the image data)
    try:
        data = json.loads(event['body'])
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON payload"})
        }

    # Access the image file data as binary from the request body
    image_data = data.get('image', '')  # Assuming the 'image' field contains the file data

    # Generate a unique ID for the DynamoDB item
    unique_id = str(uuid4())

    # Save information to DynamoDB
    dynamodb.put_item(
        TableName=dynamodb_table,
        Item={
            'id': {'S': unique_id},
            'name': {'S': data.get('name', '')},
            'email': {'S': data.get('email', '')},
            'image_path': {'S': f's3://{s3_bucket}/{unique_id}.jpg'}  # Assuming image format is JPG
        }
    )

    # Upload the image to S3
    s3.put_object(Bucket=s3_bucket, Key=f'{unique_id}.jpg', Body=image_data)

    # You can customize the response as needed
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Data saved successfully"}),
    }

    return response
