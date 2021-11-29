import os
import http.client

## Connect
connection = http.client.HTTPConnection('localhost', os.environ['TYPESENSE_API_PORT'], timeout=2)

## Metrics
headers = {'X-TYPESENSE-API-KEY': os.environ['TYPESENSE_API_KEY']}
connection.request("GET", "/metrics.json", headers=headers)
response = connection.getresponse()
print(response.read().decode())

## Health
connection.request("GET", "/health", headers=headers)
response = connection.getresponse()
print(response.read().decode())