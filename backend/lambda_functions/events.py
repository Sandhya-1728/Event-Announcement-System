import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['EVENTS_TABLE'])

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return get_events()
    elif http_method == 'POST':
        return create_event(json.loads(event['body']))
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Unsupported HTTP method'})
        }

def get_events():
    try:
        response = table.scan()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_event(event_data):
    try:
        event_data['id'] = str(datetime.now().timestamp())
        event_data['created_at'] = datetime.now().isoformat()
        
        table.put_item(Item=event_data)
        
        # Publish to SNS for email notifications
        sns = boto3.client('sns')
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=f"New event created: {event_data['title']}",
            Subject="New Event Announcement"
        )
        
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True
            },
            'body': json.dumps(event_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 