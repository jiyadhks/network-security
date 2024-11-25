# Use the official Python 3.10 slim image
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the working directory in the container
COPY . /app

# Install system dependencies
RUN apt-get update -y && apt-get install -y awscli

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]


# FROM python:3.11-slim-buster
# WORKDIR /app
# COPY . /app

# RUN apt update -y && apt install awscli -y

# RUN apt-get update && pip install -r requirements.txt
# CMD [ "python3", "app.py" ]
