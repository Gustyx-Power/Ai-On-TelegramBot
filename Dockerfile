FROM python:3.11-slim

# Force rebuild: v3 - Supabase
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the bot script
COPY bot-groq.py .

# Run
CMD ["python", "bot-groq.py"]
