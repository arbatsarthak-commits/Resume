FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Environment Defaults for Local Mode
ENV APP_ENV=production
ENV STORAGE_MODE=local
ENV DATABASE_MODE=sqlite
ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
