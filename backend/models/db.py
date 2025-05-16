import boto3
import os
import uuid
from fastapi import HTTPException, status
from models.auth import UserInDB, UserCreate, User
from utils.password import get_password_hash, verify_password

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Get table name from environment variables or use default
USERS_TABLE = os.environ.get('USERS_TABLE', 'event_announcement_users')

# Initialize the table resource
users_table = dynamodb.Table(USERS_TABLE)


async def get_user_by_email(email: str):
    """Get a user by email from DynamoDB."""
    try:
        # Query users by email (assuming email is the primary key or has a GSI)
        response = users_table.scan(
            FilterExpression="email = :email",
            ExpressionAttributeValues={
                ":email": email
            }
        )
        
        if response['Items']:
            user_data = response['Items'][0]
            return UserInDB(**user_data)
        return None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None


async def create_user(user: UserCreate):
    """Create a new user in DynamoDB."""
    # Check if user already exists
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "email": user.email,
        "name": user.name,
        "hashed_password": get_password_hash(user.password)
    }
    
    try:
        # Insert the user into DynamoDB
        users_table.put_item(Item=user_data)
        return User(id=user_id, email=user.email, name=user.name)
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


async def authenticate_user(email: str, password: str):
    """Authenticate a user with email and password."""
    user = await get_user_by_email(email)
    
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


async def get_user_by_id(user_id: str):
    """Get a user by ID from DynamoDB."""
    try:
        response = users_table.get_item(Key={"id": user_id})
        user_data = response.get('Item')
        
        if user_data:
            return UserInDB(**user_data)
        return None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None 