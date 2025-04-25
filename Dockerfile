FROM python:3.10-slim

WORKDIR /app

# Install Node.js and OpenJDK
RUN apt-get update && \
    apt-get install -y nodejs npm openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
