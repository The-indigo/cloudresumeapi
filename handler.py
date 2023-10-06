import json
import boto3

# Initialize a DynamoDB client
dynamodb = boto3.client('dynamodb')


def insertCount(event, context):
    try:
        # Parse the incoming JSON data from the request body
        request_body = json.loads(event['body'])

        # Ensure that the request body contains the 'count' field
        if 'count' not in request_body:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid request body. 'count' field is missing."}),
            }

        # Retrieve the 'count' value from the request body
        count = request_body['count']

        # Use an atomic counter to increment the 'count' attribute by the retrieved value
        response = dynamodb.update_item(
            TableName='visitcount',
            Key={'id': {'S': '1'}},  #'id' is the partition key and its value is '1'
            UpdateExpression="SET #count = #count + :increment",
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':increment': {'N': str(count)}}
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Count data incremented and updated in DynamoDB."}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
        }
