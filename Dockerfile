# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /app
COPY . /app

# Set environment variable to ensure Python uses the right directory
ENV PYTHONPATH=/app

# Run the test script when the container launches
CMD ["python", "hardware/test_mock_daq.py"]
