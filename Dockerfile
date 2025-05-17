FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install PostgreSQL client and other dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . /app

# Expose the application port
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]