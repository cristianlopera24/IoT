import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ws_connection_id_cacris')
   
    if event['requestContext']['routeKey']=='$connect':
        connectionId = event['requestContext']['connectionId']
        print(event)
        
        # Crea una clave única para el cliente basada en el connectionId
        app_id = f"connection_{connectionId}"
        
        table.put_item(
        Item={'app_id': app_id,'id':connectionId}
        )
    if event['requestContext']['routeKey']=='$disconnect':
        connectionId = event['requestContext']['connectionId']
        
        # Elimina la entrada correspondiente al cliente desconectado
        app_id = f"connection_{connectionId}"
        response = table.delete_item(
            Key={'app_id': app_id}
            )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }