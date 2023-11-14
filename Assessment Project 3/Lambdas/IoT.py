import math
import boto3
from decimal import Decimal
import json

# Get dynamodb resource
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
   
    # JSON object from IoT core has timestamp field
    if 'timestamp' in event:
        # Get table
        table = dynamodb.Table('cacris_table')
        
        # Put item into table
        response = table.put_item(
        Item={
        'app_id': "IoT", # Primary key
        'timestamp': event['timestamp'], # Sort key
        'sensor': event['sensor']
        }
        )
        
        # Print put_item response
        print(response)
        
        # Get recently written item
        response = table.get_item(
        Key={'app_id': "IoT", 'timestamp': event['timestamp']}
        )
        
        # Print get_item response
        print(response)
        
        # Print table scan results
        #print(table.scan()['Items'])
        
        # Obtiene la conexión del cliente y envía los datos del sensor
        table = dynamodb.Table('ws_connection_id_cacris')
        
        if event['requestContext']['routeKey']=='$connect':
            connectionId = event['requestContext']['connectionId']
            print(event)
        
            # Crea una clave única para el cliente basada en el connectionId
            app_id = f"connection_{connectionId}"
        
            response = table.get_item(
                Key={'app_id': app_id}
            )
            print(response)
    
            if 'Item' in response:
                api_client = boto3.client('apigatewaymanagementapi', endpoint_url='https://nl2kp0gzc1.execute-api.us-east-1.amazonaws.com/production')
                connectionId = response['Item']['id']
                api_client.post_to_connection(ConnectionId=connectionId, Data=json.dumps({'sensor': event['sensor']}))
                print(connectionId)

            return "DB updated"

