FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the entire project into the container image
COPY . .

EXPOSE 8000
EXPOSE 9000

CMD ["python", "backend/vulnerable_server.py"]
