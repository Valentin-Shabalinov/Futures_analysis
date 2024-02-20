# Use the official Python 3.11 image
FROM python:3.11

# Install dependencies required for compiling some libraries
RUN apt-get update && \
    apt-get install -y build-essential

# Install necessary libraries from system packages
RUN pip install --no-cache-dir numpy psycopg2-binary

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Command to execute
CMD ["python", "test_bd.py"]
