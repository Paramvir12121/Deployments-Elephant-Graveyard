# Flask React Web Application

This is a full-stack web application using a Flask backend and a React frontend. The application includes error handling using Rollbar, logging with Flask and AWS S3, and monitoring with UptimeRobot and AWS CloudWatch. This document provides setup instructions and details about the project.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Frontend (React)](#frontend-react)
- [Backend (Flask)](#backend-flask)
- [Logging](#logging)
- [Error Tracking with Rollbar](#error-tracking-with-rollbar)
- [Monitoring](#monitoring)
- [Testing](#testing)
- [Deployment](#deployment)

## Project Structure
```
. ├── backend/ │ ├── app.py # Flask backend with API routes │ ├── requirements.txt # Backend dependencies │ └── .env # Environment variables (Rollbar, DB configs) │ ├── frontend/ │ ├── src/ │ ├── public/ │ ├── vite.config.js # Vite configuration for React │ ├── package.json # Frontend dependencies │ └── .env # Frontend environment variables │ └── README.md # Project documentation
```

## Features

- **Flask Backend**: API routes to handle feedback.
- **React Frontend**: Simple React interface to interact with the backend.
- **Error Handling**: Automatic error tracking using Rollbar.
- **Logging**: Flask logs stored locally and uploaded to AWS S3 for long-term storage.
- **Monitoring**: UptimeRobot for uptime checks and AWS CloudWatch for resource monitoring.

## Prerequisites

- **Python 3.x** installed for the backend (Flask).
- **Node.js** and **npm** for the frontend (React).
- AWS account with permissions for S3 (for log storage).
- Rollbar account for error tracking.

## Installation

### 1. Clone the repository

```
git clone https://github.com/your-repo/flask-react-app.git
cd flask-react-app
```
2. Install Backend Dependencies
Navigate to the backend/ directory:

```
cd backend
pip install -r requirements.txt
```

3. Install Frontend Dependencies
Navigate to the frontend/ directory:
```
cd frontend
npm install
Environment Setup
Backend .env file
Create a .env file inside the backend/ directory with the following content:
```

# .env file for Flask (Backend)
```
ROLLBAR_ACCESS_TOKEN=your_rollbar_access_token
DATABASE_URL=sqlite:///feedback.db
FLASK_ENV=development
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=my-s3-bucket
```
Frontend .env file
Create a .env file inside the frontend/ directory:

# .env file for React (Frontend)
```
VITE_API_URL=http://localhost:5000
```

Frontend (React)
The frontend is a simple React app created using Vite. It includes a button that, when pressed, triggers an error in the backend (Flask) for testing purposes.

Running the Frontend
To start the React app:

```
cd frontend
npm run dev
```
The app should be running at http://localhost:3000.

Backend (Flask)
The backend is a Flask API that handles feedback submission and exposes a route to raise a test exception for error tracking.

Running the Backend
To start the Flask app:

```
cd backend
python app.py
```
The Flask backend should be running at http://localhost:5000.

Key API Routes
GET /feedback: Retrieve all feedback entries.
POST /feedback: Submit feedback (requires a JSON body with name and comment).
GET /cause-error: Trigger an intentional exception to test Rollbar error tracking.
Logging
Flask logs are saved to a local app.log file.
Logs are periodically uploaded to AWS S3 for centralized storage.
To configure log uploads to S3, modify the following code in app.py:

```
import boto3
from datetime import datetime

def upload_log_to_s3():
    s3 = boto3.client('s3')
    bucket_name = os.getenv('AWS_S3_BUCKET')
    log_file = 'app.log'
    s3.upload_file(log_file, bucket_name, f'logs/{datetime.now().strftime("%Y-%m-%d")}_app.log')
```

## Error Tracking with Rollbar

Rollbar is integrated into the Flask backend for real-time error tracking. You can manually trigger an error by visiting `/cause-error` in the browser.

Rollbar will capture any unhandled exceptions and send detailed reports to the Rollbar dashboard.  
To view captured errors, go to your [Rollbar dashboard](https://rollbar.com/).

## Monitoring

### UptimeRobot

UptimeRobot is used to monitor the availability of the Flask API. You can set up monitors for the `/` or `/feedback` routes.  
Alerts can be configured via email or SMS.

### AWS CloudWatch

If the app is hosted on AWS (e.g., EC2, ECS), CloudWatch is used for resource monitoring.  
Set up CloudWatch dashboards and alarms for CPU, memory, and other critical metrics.

## Testing

### Testing Error Handling

- Visit the `/cause-error` route in the browser or from the React frontend.
- Verify that the error is logged in the Rollbar dashboard.

### Testing Logging

- Check that logs are written to the `app.log` file.
- Ensure logs are periodically uploaded to S3 (or call the log upload function manually).

### Testing Monitoring

- Ensure UptimeRobot is monitoring the app and alerts you if the app goes down.
- Check CloudWatch for resource monitoring (if applicable).

## Deployment

The app can be deployed to AWS (EC2, ECS) or other hosting platforms. Use the following steps for deployment:

1. **Deploy the Backend**: Deploy the Flask app using tools like AWS Elastic Beanstalk or EC2.
2. **Deploy the Frontend**: Build the React app using `npm run build` and serve it using a static file server (e.g., Nginx or S3).
3. **Configure Monitoring**: Ensure UptimeRobot and CloudWatch are set up for the production environment.
