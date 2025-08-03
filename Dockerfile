
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run Streamlit app on Render's port
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
