# Use the official Python 3.11 image
FROM python:3.11

# Install dependencies for compiling some libraries
RUN apt-get update && \
    apt-get install -y build-essential

# Install necessary libraries from system packages
RUN pip install --no-cache-dir numpy psycopg2

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run the DB initialization script and the main application
CMD ["sh", "-c", "python init_db.py && python app.py"]
