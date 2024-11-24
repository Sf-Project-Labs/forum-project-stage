FROM python:3.11.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Run the Django application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]