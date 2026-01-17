FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY bot-groq.py .
COPY *.json ./

# Run
CMD ["python", "bot-groq.py"]
