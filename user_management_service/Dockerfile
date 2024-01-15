# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app/ ./app

# Set environment variables
ENV FLASK_APP app/__init__.py
ENV FLASK_ENV development

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
