# Step 1: Use an official Python runtime as a parent image.
# Using python:3.11-slim for a smaller image size.
FROM python:3.11-slim

# Step 2: Set the working directory in the container to /app.
WORKDIR /app

# Step 3: Copy the dependencies file first and install them.
# This leverages Docker's build cache. The dependencies will only be re-installed
# if the requirements.txt file changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the application's source code into the container at /app.
COPY . .

# Step 5: Define the command to run the application.
# Uvicorn is started to serve the FastAPI application.
# --host 0.0.0.0 makes the server accessible from outside the container.
# --port 8080 is used as many hosting services (like Fly.io) default to this port.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
