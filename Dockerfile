FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Install the package in development mode
RUN pip install -e .
# RUN pip install .

# Change the command to use the correct module path
CMD ["uvicorn", "src.vector_search.main:app", "--host", "0.0.0.0", "--port", "8000"]
