FROM qubitproducts/exporter_exporter:0.4.5

RUN apk update \
 && apk add python3 py-pip

WORKDIR /opt
COPY . .
RUN pip install -r requirements.txt