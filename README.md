# typesense-exporter
Prometheus exporter for typesense written in python, leveraging typesenses' api to scrape metrics.

Scraped endpoints include:
* `/metrics`
* `/health`
* `/stats`

See https://typesense.org/docs/0.21.0/api/cluster-operations.html for further Details about the provided metrics.
## Usage
### Local
```
pip install -r requirements.txt
python3 typesense-exporter.py
```
### Docker
The Container is intended to be deployed as sidecar in the same pod as the typesense container.

```
[...]
  containers:
  - name: typesense
    image: typesense/typesense:0.21.0
    ports:
    - containerPort: 8108
      name: http
      protocol: TCP
  - name: metrics
    image: typesense-exporter:latest
    name: metrics
    ports:
    - containerPort: 9000
      name: monitoring
      protocol: TCP
[...]
```

## Configuration
typesense-exporter is entirely configured via environment Variables  

|Variable|Description|Default|
|---|---|---|
| `TS_EXPORTER_LISTEN_ADDRESS` | Address to bind the local Webserver to | `0.0.0.0` |
| `TS_EXPORTER_LISTEN_PORT` | Port to bind the local Webserver to | `9000` |
| `TS_EXPORTER_METRICS_PREFIX` | Prefix for all Metrics | `typesense` |
| `TS_EXPORTER_TYPESENSE_SCHEME` | Scheme used to connect to the typesense API Port | `http` |
| `TS_EXPORTER_TYPESENSE_HOST` | Typesense Host to scrape Metrics from | `localhost` |
| `TYPESENSE_API_PORT` | Typesense Api Port | `8108` |
| `TYPESENSE_API_KEY` | Typesense Api Key for Scraping stats and metrics endpoints | `''` |