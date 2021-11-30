FROM python:3-slim

WORKDIR /opt
RUN groupadd exporter --gid 1000 \
 && useradd exporter --uid 1000 --gid exporter

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY --chown=exporter typesense-exporter.py .

USER exporter
EXPOSE 9000
ENTRYPOINT ["/usr/local/bin/python", "typesense-exporter.py"]