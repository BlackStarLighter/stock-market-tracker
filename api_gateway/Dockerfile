# stock-market-tracker/api_gateway/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the API Gateway
CMD ["uvicorn", "api_gateway:app", "--host", "0.0.0.0", "--port", "8000"]
