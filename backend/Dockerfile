# Dockerfile for Flask
FROM python:3.10-slim

WORKDIR /app

# Copy the virtual environment and requirements file
COPY ./pixie_env/ ./pixie_env/
COPY requirements.txt .


# Install the dependencies
RUN pip install -r requirements.txt
COPY ./src/ ./src/

ENV FLASK_APP=src/app.py
EXPOSE 3000
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
# CMD ["python", "src/app.py"]
