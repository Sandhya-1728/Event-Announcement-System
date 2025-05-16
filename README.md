# Event Announcement System

A web application for creating and subscribing to event announcements with authentication using AWS services.

## System Architecture

### Frontend
- React.js application
- User authentication
- Event creation and listing
- Email subscription

### Backend
- FastAPI for RESTful API
- JWT Authentication
- AWS DynamoDB for data storage
- AWS SNS for notifications

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- AWS Account with appropriate permissions
- AWS CLI configured locally

## AWS Resources Required

1. DynamoDB Tables:
   - `event_announcement_users` - For user data
   - `event_announcements` - For event data

2. SNS Topic:
   - For sending email notifications

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-repo/event-announcement-system.git
cd event-announcement-system
```

2. **AWS Setup**

```bash
# Create a .env file in the project root with AWS credentials
touch .env

# Add the following to the .env file:
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
EVENTS_TABLE=event_announcements
USERS_TABLE=event_announcement_users
SNS_TOPIC_ARN=your_sns_topic_arn
JWT_SECRET=your_jwt_secret
```

3. **Create the DynamoDB tables**

```bash
# Run the table creation script
cd backend
python -m scripts.create_tables
cd ..
```

4. **Start the application**

```bash
docker-compose up -d
```

5. **Access the application**

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development

### Frontend Development

```bash
cd frontend
npm install
npm start
```

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License

This project is licensed under the MIT License. See the LICENSE file for details. 