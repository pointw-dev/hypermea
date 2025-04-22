FROM python:3.13.2-alpine

ENV HY_SERVICE_PORT=80
EXPOSE $HY_SERVICE_PORT

WORKDIR /service
COPY service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip 

COPY service .

RUN addgroup --system hypermea && \
    adduser --system --ingroup hypermea appuser && \
    chown -R appuser:hypermea /service

USER appuser

CMD ["python", "run.py"]
