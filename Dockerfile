# Use the official Python image as a base
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Start the Django application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "distroplace.wsgi:application"]
