import json
import boto3

dynamodb = boto3.client('dynamodb', region_name='eu-central-1')

def lambda_handler(event, context):
    params = {
        'TableName': 'serverlessapp', # Replace with your table name
    }
    response = dynamodb.scan(**params)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response['Items']),
    }
