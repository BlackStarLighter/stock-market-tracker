## stock-market-tracker/stock_fetcher/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the stock fetcher script
CMD ["python", "stock_fetcher.py"]
