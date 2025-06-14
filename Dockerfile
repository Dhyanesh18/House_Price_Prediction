# Use a lightweight base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy only requirements and install first
COPY server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app and client static files
COPY server/ ./server
COPY client/ ./client

# Set working dir to server where app.py is
WORKDIR /app/server

# Use python to run app with waitress
CMD ["python", "app.py"]
