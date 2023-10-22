import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ws_connection_id_cacris')
   
    if event['requestContext']['routeKey']=='$connect':
        connectionId = event['requestContext']['connectionId']
        print(event)
        
        response = table.get_item(
            Key={'app_id': "connectionid"}
            )
            
        if 'Item' in response:
            response = table.update_item(
            Key={
            'app_id': "connectionid"
            },
            UpdateExpression="set id=:id",
            ExpressionAttributeValues={
            ':id': connectionId
            },
            ReturnValues="UPDATED_NEW"
            )
        else:
            table.put_item(
            Item={'app_id': "connectionid",'id':connectionId}
            )
    if event['requestContext']['routeKey']=='$disconnect':

        
        response = table.delete_item(
            Key={'app_id': "connectionid"}
            )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
