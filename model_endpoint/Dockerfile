FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV AZURE_SCRIPT="python3 model_flask.py"
EXPOSE 5000
CMD ["python3", "model_flask.py"]