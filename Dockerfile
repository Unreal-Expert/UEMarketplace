# Use an official Python runtime as a parent image
FROM python:3.11 as builder

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1

# Copy the Django application code into the builder's /uemarketplace directory
COPY uemarketplace /uemarketplace

# Copy the requirements file into the builder's root directory
COPY requirements.txt /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Run collectstatic command in the builder stage
RUN python /uemarketplace/manage.py collectstatic --noinput

# Start the second stage of the build to produce the final image
FROM python:3.11

# Copy the Python environment from the builder stage
COPY --from=builder /usr/local /usr/local

# Install Nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy static files and Django app from builder stage using absolute paths
COPY --from=builder /uemarketplace/staticfiles /uemarketplace/staticfiles
COPY --from=builder /uemarketplace /uemarketplace

# Copy root-level configuration files
COPY nginx.conf /etc/nginx/sites-available/
COPY start.sh /

# Remove default Nginx configuration and enable our configuration
RUN rm /etc/nginx/sites-enabled/default && ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled

# Ensure the start script is executable
RUN chmod +x /start.sh

# Debugging step to list contents and display the start.sh script
RUN ls -l / && cat /start.sh

# Expose port 80 for the Django application
EXPOSE 80

# Set the start script as the command to run when the container starts
CMD ["/bin/sh", "/start.sh"]