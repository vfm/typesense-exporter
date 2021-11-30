import os
import json
import bottle
import requests

exporter_address = os.environ.get('TS_EXPORTER_LISTEN_ADDRESS', 'localhost')
exporter_port = os.environ.get('TS_EXPORTER_LISTEN_PORT', 9000)
exporter_prefix = os.environ.get('TS_EXPORTER_METRICS_PREFIX', 'typesense')

typesense_scheme = os.environ.get('TS_EXPORTER_TYPESENSE_SCHEME', 'http')
typesense_host = os.environ.get('TS_EXPORTER_TYPESENSE_HOST', 'localhost')
typesense_port = os.environ.get('TYPESENSE_API_PORT', 8108)
typesense_apikey = os.environ.get('TYPESENSE_API_KEY')
typesense_endpoints = {
  "health": { "url": "health" },
  "metrics": { "url": "metrics.json" },
  "stats": { "url": "stats.json" }
}

## Fetch endpoints and return dict
def scrapeEndpoints(ep):
  generated = dict()
  for endpoint, config in ep.items():
    h = {'X-TYPESENSE-API-KEY': typesense_apikey}
    r = requests.get( typesense_scheme + "://" + typesense_host + ":" + typesense_port + "/" + config["url"], headers=h )
    generated[endpoint] = json.loads(r.text)
  return generated

## Format metrics according to openmetrics
## return metrics as list of strings
def generateOutput(sd):
  generated = list()
  for endpoint, data in sd.items():
    for name, value in data.items():
      # Express Bools numerical
      if isinstance(value, bool):
        value = int(value == True)
      # Generate Labels for stats endpoint
      if isinstance(value, dict) and endpoint == "stats":
        for label, val in value.items():
          label = label.split()
          generated.append(exporter_prefix + "_" + endpoint + "_" + name + "{method=\"" + label[0] + "\",path=\"" + label[1] + "\"} " + str(val))
      else:
        # Default output format
        generated.append(exporter_prefix + "_" + endpoint + "_" + name + " " + str(value))
  return generated

## Setup Webserver
# Index
@bottle.route('/')
def index():
  return """
    <h1>typesense-exporter</h1>
    <ul>
    <li><a href="/metrics">metrics<a/></li>
    </ul>
  """

# Metrics
@bottle.route('/metrics')
def metrics():
  scrapedata = scrapeEndpoints(typesense_endpoints)
  outputlist = generateOutput(scrapedata)

  output = str()
  for i in outputlist:
    output += str(i) + "\n"
  
  bottle.response.content_type = 'text/plain'
  return output

# Run Webserver
bottle.run(host=exporter_address, port=exporter_port)