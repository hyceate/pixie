# Dockerfile for Flask
FROM python:3.10-slim

WORKDIR /app

COPY ./pixie_env/ ./pixie_env/
COPY app.py .

RUN pip install Flask

CMD ["python", "app.py"]