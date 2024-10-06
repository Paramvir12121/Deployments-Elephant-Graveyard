# Use the official Python image from the Docker Hub
FROM python:3.12-slim

COPY . /usr/src/app

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
# COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
# COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Use gunicorn to run the Flask application in production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]