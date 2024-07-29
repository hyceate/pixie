# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .
# Remove the existing virtual environment if it exists
RUN rm -rf pixie_env
# Create a virtual environment using Python's built-in venv
RUN python -m venv pixie_env

# Install the dependencies into the virtual environment
RUN pixie_env/bin/pip install -r requirements.txt

# Copy the application code to the container
COPY ./src /app/src

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/app/pixie_env
ENV PATH="/app/pixie_env/bin:$PATH"
ENV PYTHONPATH=/app/src

# Expose port 3000
EXPOSE 3000

# Command to run FastAPI with Uvicorn
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "3000"]
