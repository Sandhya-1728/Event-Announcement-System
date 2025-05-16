from fastapi import APIRouter, HTTPException, status, Depends
import boto3
import uuid
import os
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from utils.jwt import get_current_user

router = APIRouter()

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Get table name from environment variables or use default
EVENTS_TABLE = os.environ.get('EVENTS_TABLE', 'event_announcements')

# Initialize SNS client for notifications
sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

# Initialize the table resource
events_table = dynamodb.Table(EVENTS_TABLE)


# Event models
class EventBase(BaseModel):
    title: str
    description: str
    date: str
    location: str
    organizer: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: str
    created_at: str
    user_id: str


@router.get("/", response_model=List[Event])
async def get_events():
    """Get all events."""
    try:
        response = events_table.scan()
        return response.get('Items', [])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch events: {str(e)}"
        )


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, current_user: dict = Depends(get_current_user)):
    """Create a new event."""
    try:
        event_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        
        event_data = {
            "id": event_id,
            "created_at": created_at,
            "user_id": current_user["user_id"],
            **event.dict()
        }
        
        # Save event to DynamoDB
        events_table.put_item(Item=event_data)
        
        # Send notification if SNS topic is configured
        if SNS_TOPIC_ARN:
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Message=f"New event created: {event.title}",
                    Subject="New Event Announcement"
                )
            except Exception as sns_error:
                print(f"Error sending SNS notification: {sns_error}")
        
        return event_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        ) 