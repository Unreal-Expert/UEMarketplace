# Use an official Python runtime as a parent image
FROM python:3.11 as builder

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /uemarketplace

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run collectstatic command
RUN python uemarketplace/manage.py collectstatic --noinput

# Start the second stage of the build to produce the final image
FROM python:3.11

# Set the working directory in the container
WORKDIR /uemarketplace

# Copy static files and Django app from builder stage
COPY --from=builder /uemarketplace/static /uemarketplace/static
COPY --from=builder /uemarketplace /uemarketplace

# Expose port 80 for the Django application
EXPOSE 80

# Define the command to run when the container starts
CMD ["python", "uemarketplace/manage.py", "runserver", "0.0.0.0:8000"]

