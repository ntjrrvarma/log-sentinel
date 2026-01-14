FROM python:3.12-slim

WORKDIR /app

# Copy requirements first (Caching strategy - efficient build)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy everything
COPY . .

CMD ["python", "app.py"]