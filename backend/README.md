# Event Announcement Backend

This is the backend service for the Event Announcement System. It provides APIs for user authentication, event creation, and event retrieval.

## AWS Setup

This backend uses AWS services for data storage and notifications:

1. **DynamoDB Tables**:
   - `event_announcement_users` - Stores user data
   - `event_announcements` - Stores event data

2. **SNS Topic**:
   - Used for sending notifications

## Required Environment Variables

Create a `.env` file in the backend directory with these variables:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
USERS_TABLE=event_announcement_users
EVENTS_TABLE=event_announcements
SNS_TOPIC_ARN=your_sns_topic_arn
JWT_SECRET=your_jwt_secret_key
```

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   uvicorn main:app --reload
   ```

## API Documentation

After starting the server, visit:
- http://localhost:8000/docs for Swagger UI
- http://localhost:8000/redoc for ReDoc

## Authentication

All requests to `/events` endpoints require a Bearer token, which you can obtain by logging in. 