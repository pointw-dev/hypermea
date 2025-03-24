FROM python:3.11.4-slim

ENV HY_API_PORT=80
EXPOSE $HY_API_PORT

WORKDIR /api
COPY service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY service .

CMD ["python", "run.py"]
