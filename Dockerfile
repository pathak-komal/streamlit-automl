FROM python:3.10-slim

WORKDIR /app

# ➜ Install system-level dependency for LightGBM (fixes libgomp.so.1 error)
RUN apt-get update && apt-get install -y libgomp1

# ➜ Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ➜ Copy app files
COPY . .

# ➜ Start Streamlit
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
