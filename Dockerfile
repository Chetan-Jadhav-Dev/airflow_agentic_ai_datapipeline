FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent/ agent/
COPY dags/ dags/

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "agent/main.py"]
