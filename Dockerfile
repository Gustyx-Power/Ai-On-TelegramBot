FROM python:3.11-slim

# Force rebuild: v2
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the bot script (not local data files)
COPY bot-groq.py .

# Create empty JSON files for fresh start
RUN echo '{}' > users.json && echo '{}' > groups.json && echo '{}' > conversations.json

# Run
CMD ["python", "bot-groq.py"]
