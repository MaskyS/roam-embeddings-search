
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv, a fast Python package installer
RUN pip install uv

# Install build-essential for compiling C extensions
RUN apt-get update && apt-get install -y build-essential

# Copy the requirements file into the container at /app
COPY requirements.txt .


# Install any needed packages specified in requirements.txt
RUN uv pip install --system -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .
