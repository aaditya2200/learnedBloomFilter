# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install pkg-config, libhdf5-dev, and gcc
RUN apt-get update && \
    apt-get install -y pkg-config libhdf5-dev gcc

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run server.py from the specified directory when the container launches
CMD ["python3", "app/interface/server.py"]
