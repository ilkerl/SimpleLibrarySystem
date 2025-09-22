# Step 1: Use a lightweight version of Python as the base image.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Copy only the requirements file first and install dependencies.
# This leverages Docker's caching mechanism. Layers are only rebuilt
# if the requirements.txt file changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the application's source code into the container at /app.
# This now includes our 'app' directory.
COPY ./app /app/app

# Step 5: Specify the command to run when the container starts.
# We now point to the 'app' variable inside the 'app.main' module.
# The host 0.0.0.0 makes the app accessible from outside the container.
# Fly.io typically expects services on port 8080.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

