import boto3
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS configuration
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Table names
USERS_TABLE = os.environ.get('USERS_TABLE', 'event_announcement_users')
EVENTS_TABLE = os.environ.get('EVENTS_TABLE', 'event_announcements')

# Initialize DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


def create_users_table():
    """Create the users table if it doesn't exist."""
    try:
        table = dynamodb.create_table(
            TableName=USERS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'EmailIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {USERS_TABLE} is being created. Status: {table['TableDescription']['TableStatus']}")
        wait_for_table(USERS_TABLE)
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table {USERS_TABLE} already exists.")


def create_events_table():
    """Create the events table if it doesn't exist."""
    try:
        table = dynamodb.create_table(
            TableName=EVENTS_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'UserIdIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {EVENTS_TABLE} is being created. Status: {table['TableDescription']['TableStatus']}")
        wait_for_table(EVENTS_TABLE)
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table {EVENTS_TABLE} already exists.")


def wait_for_table(table_name):
    """Wait for the table to be created."""
    response = dynamodb.describe_table(TableName=table_name)
    status = response['Table']['TableStatus']
    
    while status != 'ACTIVE':
        print(f"Waiting for table {table_name} to be created... Status: {status}")
        time.sleep(5)
        response = dynamodb.describe_table(TableName=table_name)
        status = response['Table']['TableStatus']
    
    print(f"Table {table_name} is now {status}")


if __name__ == "__main__":
    print("Creating DynamoDB tables...")
    create_users_table()
    create_events_table()
    print("Tables created successfully!") 