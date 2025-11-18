# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies using uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
