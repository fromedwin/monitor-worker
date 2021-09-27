import os
import requests
import json
from dotenv import load_dotenv

# Load varriables from .env
load_dotenv()
SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
SERVER_URL = os.environ.get("SERVER")
UUID = os.environ.get("UUID")

SERVER_PROMETHEUS_CONFIG_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/prometheus/{UUID}'
SERVER_ALERTS_CONFIG_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/alerts/'

# Fetch PROMETHEUS configuration files
print(f'Loading PROMETHEUS configuration files at {SERVER_PROMETHEUS_CONFIG_URL}')
try:
    response = requests.get(SERVER_PROMETHEUS_CONFIG_URL)
    response.raise_for_status()
except Exception as err:
    raise Exception(f'Error occurred: {err}')
else:
    content = response.text
    print(f'> Prometheus have been loaded from {SERVER_URL}')
    with open(f'prometheus/prometheus.yml', 'w') as file:
        file.write(content)
        file.close()

print(f'Loading ALERTS configuration files at {SERVER_ALERTS_CONFIG_URL}')
# Fetch ALERTS configuration files
try:
    response = requests.get(SERVER_ALERTS_CONFIG_URL)
    response.raise_for_status()
except Exception as err:
    raise Exception(f'Error occurred: {err}')
else:
    content = json.loads(response.content)
    print(f'> {len(content)} files have been loaded from {SERVER_URL}')
    for config in content:
        print(config['title'])
        with open(f'prometheus/alerts/{config["title"]}.yml', 'w') as file:
            file.write(config['yaml'])
            file.close()

