# Dockerfile for Clinical Document Review Tool
# 완전히 격리된 환경에서 실행

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements_web.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements_web.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the web app
CMD ["streamlit", "run", "web_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
