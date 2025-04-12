FROM python:3.11.4-slim

ENV HY_SERVICE_PORT=80
EXPOSE $HY_SERVICE_PORT

WORKDIR /service
COPY service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service .

CMD ["python", "run.py"]
