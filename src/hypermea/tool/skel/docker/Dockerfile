FROM python:3.11.4-slim

ENV HY_API_PORT=80
EXPOSE $HY_API_PORT

WORKDIR /api
COPY {$project_name}/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY {$project_name} .

CMD ["python", "run.py"]
