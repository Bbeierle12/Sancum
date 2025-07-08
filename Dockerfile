FROM python:3.11-slim

WORKDIR /app

# Copy dependency file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src

# Command to run the pivot service
# The cme_service can be run by changing the command below to:
# CMD ["uvicorn", "src.cme_service:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "src.pivot_service:app", "--host", "0.0.0.0", "--port", "8001"]
