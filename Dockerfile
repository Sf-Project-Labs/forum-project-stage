# Use a specific Python image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Create a virtual environment and install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade pip && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the project directory into the container
COPY djangoProject /app/djangoProject

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

# Create a non-root user for better security
RUN adduser --disabled-password --gecos "" appuser

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Use Gunicorn to run the application in production
CMD ["gunicorn", "-b", "0.0.0.0:8000", "djangoProject.wsgi:application"]