# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install pkg-config, libhdf5-dev, and gcc
RUN apt-get update && \
    apt-get install -y pkg-config libhdf5-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the create_topic.sh script into the container
COPY create_topic.sh /usr/bin/create_topic.sh

# Make sure the script is executable
RUN chmod +x /usr/bin/create_topic.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Ensure the script is executable
RUN chmod +x start_services.sh

# Run start_services.sh when the container launches
CMD ["./start_services.sh"]
