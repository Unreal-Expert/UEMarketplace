# Use an official Python runtime as a parent image
FROM python:3.11 AS builder

ENV PYTHONUNBUFFERED 1
WORKDIR /uemarketplace

COPY requirements.txt /uemarketplace/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /uemarketplace/

# Nginx Stage
FROM nginx:alpine

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files and Django app from builder stage
COPY --from=builder /uemarketplace/static /uemarketplace/static
COPY --from=builder /uemarketplace /uemarketplace

# Start Nginx and Django using a script
CMD ["sh", "-c", "nginx && python /uemarketplace/manage.py runserver 0.0.0.0:8000"]
