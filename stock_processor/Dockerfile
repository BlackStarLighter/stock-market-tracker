# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the required files first to leverage Docker's caching mechanism
COPY stock_fetcher/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the stock_fetcher source code into the container
COPY stock_fetcher/ .

# Set the default command to run the stock fetcher script
CMD ["python", "stock_fetcher.py"]
