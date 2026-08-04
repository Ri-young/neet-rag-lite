FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Create data and chroma_db folders
RUN mkdir -p data chroma_db
EXPOSE 10000
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
