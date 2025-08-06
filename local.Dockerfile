FROM python:3.12-slim AS base_app

WORKDIR /app

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

COPY ./src /app/src
RUN pip install -r /app/src/requirements.txt

FROM base_app AS full_app

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
