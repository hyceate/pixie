# Dockerfile for Flask
FROM python:3.10-slim

WORKDIR /app

# Copy the virtual environment and requirements file
COPY ./pixie_env/ ./pixie_env/
COPY requirements.txt .
COPY ./src/ ./src/

# Install the dependencies
RUN pip install -r requirements.txt

EXPOSE 3000
# Run the Flask app
CMD ["python", "app.py"]
