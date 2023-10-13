import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-central-1')

def lambda_handler(event, context):
    
   

    # Collect the search criteria
    name = event["pathParameters"]["name"]
    
    email = event["pathParameters"]["email"]
  

    # Prepare the query parameters (same as in the previous response)

    query_params = {
        'TableName': 'serverlessapp',
        'ExpressionAttributeValues': {
            ':n': {'S': name} ,
            ':e': {'S': email} 
        },
        'FilterExpression': '(#name = :n) OR (#email = :e)',
        'ExpressionAttributeNames': {
            '#name': 'name',
            '#email': 'email'
        }
    }
    
   
    
    # Query DynamoDB based on the search criteria
    try:
        response = dynamodb.scan(**query_params)
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"message": f"Error: {str(e)}"})
        }
    