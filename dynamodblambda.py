import json
import boto3
import os
from uuid import uuid4


# Initialize the DynamoDB 
dynamodb = boto3.client('dynamodb', region_name='eu-central-1')


# Define the DynamoDB table name
dynamodb_table = 'serverlessapp'


def lambda_handler(event, context):
    # Ensure that the 'body' key exists in the event and is not None
    if 'body' not in event or event['body'] is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request body"})
        }
      
      

    # Generate a unique ID for the DynamoDB item
    unique_id = str(uuid4())
    
     # Parse the incoming JSON payload (which includes the image data)
    try:
        data = json.loads(event['body'])
    except json.JSONDecodeError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid JSON payload"})
        }
    
    
    # Save information to DynamoDB
    dynamodb.put_item(
        TableName=dynamodb_table,
        Item={
            'id': {'S': unique_id},
            'name': {'S': data.get('name', '')},
            'email': {'S': data.get('email', '')},
            
        }
    )

   
    
 
    # You can customize the response as needed
    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Data saved successfully"}),
    }

    return response
