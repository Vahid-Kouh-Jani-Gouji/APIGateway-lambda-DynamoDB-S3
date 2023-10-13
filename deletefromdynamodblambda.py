import json
import boto3

dynamodb = boto3.client('dynamodb', region_name='eu-central-1')

def lambda_handler(event, context):
    # Parse the ID of the item you want to delete from the request event
    item_id = event['queryStringParameters']['id']

    # Define the table name
    table_name = 'serverlessapp'  # Replace with your table name

    # Delete the item from DynamoDB
    dynamodb.delete_item(
        TableName=table_name,
        Key={'id': {'S': item_id}}
    )

    # Respond with a success message
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item deleted successfully'}),
    }

    return response