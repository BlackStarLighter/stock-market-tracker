# Use an official Python image as the base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the API Gateway files to the container
COPY . /app/

# Install required Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn grpcio grpcio-tools requests

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "api_gateway:app", "--host", "0.0.0.0", "--port", "8000"]
