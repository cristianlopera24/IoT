import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import datetime

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    # Get dynamodb resource
    dynamodb = boto3.resource('dynamodb')
    # Get table
    table = dynamodb.Table('cacris_table')
    operation = event['resource']

    if operation == '/data':
        # Print table scan results
        body=table.scan()['Items']
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body,cls=JSONEncoder)
        }
    elif operation == '/last-entry':
        # Obtener el último dato
        body = table.scan()
        items = body.get('Items', [])
        if items:
            latest_item = items[-1]
            return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'latest_value': latest_item}, cls=JSONEncoder)
            }
    elif operation == '/max':
        # Obtener el máximo valor
        body = table.scan(
            Select='ALL_ATTRIBUTES'
        )
        items = body.get('Items', [])
        max_value = max(int(item['sensor']) for item in items)
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'max_value': max_value})
        }
    elif operation == '/min':
        # Obtener el mínimo valor
        response = table.scan(
            Select='ALL_ATTRIBUTES'
        )
        items = response.get('Items', [])
        min_value = min(int(item['sensor']) for item in items)
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'min_value': min_value})
        }
    elif operation == '/average':
        # Calcular el promedio de los valores
        response = table.scan(
            Select='ALL_ATTRIBUTES'
        )
        items = response.get('Items', [])
        values = [int(item['sensor']) for item in items]
        average_value = sum(values) / len(values) if values else 0
        return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'average_value': average_value})
        }
    elif operation == '/data-between-dates':
        query_parameters = event.get('queryStringParameters', {})
        start_date_str = query_parameters.get('start_date')
        end_date_str = query_parameters.get('end_date')

        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps('Invalid date format')
            }

        start_timestamp = int(start_date.timestamp() * 1000)
        end_timestamp = int(end_date.timestamp() * 1000)

        if start_timestamp > end_timestamp:
            end_timestamp = start_timestamp + 1
            
        response = table.query(
            KeyConditionExpression = boto3.dynamodb.conditions.Key('app_id').eq('IoT') & 
            boto3.dynamodb.conditions.Key('timestamp').between(start_timestamp, end_timestamp)
            )

        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items, cls=JSONEncoder)
        }    
    else:
        return {
        'statusCode': 400,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('Invalid operation')
        }
