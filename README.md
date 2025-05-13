# Event Announcement System

A serverless web application for managing and announcing events, built with React.js frontend and AWS serverless backend.

## Features

- View upcoming events
- Submit new events
- Email subscription for event notifications
- Serverless architecture using AWS services

## Tech Stack

### Frontend
- React.js
- React Router
- Axios for API calls

### Backend (AWS Serverless)
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon SNS
- Amazon S3

## Setup Instructions

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### AWS Setup
1. Create the following AWS resources:
   - DynamoDB table for events
   - SNS topic for notifications
   - API Gateway endpoints
   - Lambda functions
   - S3 bucket for frontend hosting

2. Configure environment variables:
   - Create a `.env` file in the backend directory
   - Add the following variables:
     ```
     EVENTS_TABLE=your-dynamodb-table-name
     SNS_TOPIC_ARN=your-sns-topic-arn
     ```

## Deployment

### Frontend Deployment
1. Build the React application:
   ```bash
   npm run build
   ```

2. Deploy to S3:
   ```bash
   aws s3 sync build/ s3://your-bucket-name
   ```

### Backend Deployment
1. Package Lambda functions:
   ```bash
   zip -r function.zip .
   ```

2. Deploy to AWS Lambda:
   ```bash
   aws lambda update-function-code --function-name your-function-name --zip-file fileb://function.zip
   ```

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 