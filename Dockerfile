FROM python:3 as build

WORKDIR /opt
COPY requirements.txt .
RUN python -m venv venv \
 && venv/bin/pip install -r requirements.txt

FROM qubitproducts/exporter_exporter:0.4.5 as run

WORKDIR /opt
COPY --from=build /opt/venv ./venv
COPY . .