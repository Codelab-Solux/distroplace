# Use the official Python image as a base
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# # Use ARG to define build-time environment variable
# ARG SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

# # Set environment variable from build argument
# ENV SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=$SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

# Create the directory for the database
# RUN mkdir -p /data/db

# Copy the rest of the application code
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Start the Django application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "distroplace.wsgi:application"]
