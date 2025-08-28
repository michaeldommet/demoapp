# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV NAME=World \
    FLASK_ENV=production \
    MYSQL_USER=root \
    MYSQL_SERVER=localhost \
    MYSQL_DATABASE=appdb \
    OTLP_ENDPOINT=http://localhost:4317
# Note: Do not set MYSQL_PASSWORD here; pass it securely at runtime or use Docker secrets.

# Run app.py when the container launches
CMD ["python", "app.py"]