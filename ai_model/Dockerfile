# Use an official Python image as the base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the AI model files to the container
COPY . /app/

# Install required Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn tensorflow numpy pandas scikit-learn

# Expose the FastAPI port
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
