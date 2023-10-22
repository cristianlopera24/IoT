import boto3
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Verifica si 'app_id' está presente en la solicitud
    if 'queryStringParameters' not in event or 'app_id' not in event['queryStringParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps('Missing app_id')
        }
    
    app_id = event['queryStringParameters']['app_id']
    
    # Obtiene la tabla
    table = dynamodb.Table('cacris_table')
    
    # Almacena el item en la tabla con 'app_id' como clave primaria
    table.put_item(
        Item={
            'app_id': app_id,  # Utiliza app_id como clave primaria
            'timestamp': event['timestamp'],  # Utiliza timestamp como clave de ordenamiento
            'sensor': event['sensor']
        }
    )
    
    # Obtiene la conexión del cliente y envía los datos del sensor
    ws_table = dynamodb.Table('ws_connection_id_cacris')
    response = ws_table.get_item(
        Key={'app_id': app_id}
    )
    
    if 'Item' in response:
        connection_id = response['Item']['id']
        api_client = boto3.client('apigatewaymanagementapi', endpoint_url='https://nl2kp0gzc1.execute-api.us-east-1.amazonaws.com/production')
        api_client.post_to_connection(ConnectionId=connection_id, Data=json.dumps({'sensor': event['sensor']}))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data processed and sent to the client.')
    }
