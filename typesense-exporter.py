import os
import requests
import json

host = os.environ.get('TS_EXPORTER_HOST', 'localhost')
scheme = os.environ.get('TS_EXPORTER_SCHEME', 'http')
port = os.environ.get('TYPESENSE_API_PORT', 8108)
apikey = os.environ.get('TYPESENSE_API_KEY')
metrics_prefix = "typesense"

endpoints = {
  "health": { "url": "health" },
  "metrics": { "url": "metrics.json" },
  "stats": { "url": "stats.json" }
}

metrics = dict()

## Fetch endpoints and plug returned json into metrics dict
for endpoint, config in endpoints.items():
  h = {'X-TYPESENSE-API-KEY': os.environ['TYPESENSE_API_KEY']}
  r = requests.get( scheme + "://" + host + ":" + port + "/" + config["url"], headers=h )
  metrics[endpoint] = json.loads(r.text)

# Loop over metrics dict and generate scrapable output
for endpoint, data in metrics.items():
  for name, value in data.items():

    # Express Bools numerical
    if isinstance(value, bool):
      value = int(value == True)

    # Generate Labels for stats endpoint
    if isinstance(value, dict) and endpoint == "stats":
      for label, val in value.items():
        label = label.split()
        print(metrics_prefix + "_" + endpoint + "_" + name + "{method=\"" + label[0] + "\",path=\"" + label[1] + "\"} " + str(val))
    else:
      # Print Metric
      print(metrics_prefix + "_" + endpoint + "_" + name + " " + str(value))