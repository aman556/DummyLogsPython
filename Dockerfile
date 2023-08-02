FROM python:3

ADD logs.py /

RUN pip install --upgrade pip && pip install opentelemetry-api \
    && pip install opentelemetry-sdk \
    && pip install opentelemetry-exporter-otlp

CMD [ "python", "./logs.py" ]
