FROM python:3.9-slim
WORKDIR /youtube
COPY . /youtube
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD uvicorn app.server:app --log-config=log_configuration.yaml --host 0.0.0.0 --port 8081
