FROM python:3.12-slim

WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

EXPOSE 5002

CMD ["python", "app.py"]
