# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP app.py
ENV PYTHONPATH /usr/src/app
ENV FLASK_ENV development


# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
