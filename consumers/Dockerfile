FROM python:3.8

COPY . /consumers
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumers/consumer.py"]