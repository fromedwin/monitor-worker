import os
import requests
import json
from dotenv import load_dotenv
import time as time

import load_config

del os.environ["UUID"]
# Load varriables from .env
load_dotenv()
SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
SERVER_URL = os.environ.get("SERVER") or 'host.docker.internal:8000'
UUID = os.environ.get("UUID")

SERVER_HEARTBEATS_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/heartbeat/{UUID}'

# Print Heartbeat
print(f'Heartbeat to {SERVER_HEARTBEATS_URL}')

while True:
	try:
	    response = requests.get(SERVER_HEARTBEATS_URL)
	    response.raise_for_status()

	    load_config.load_config(SERVER_URL)
	except Exception as err:
		print(f'Error occurred: {err}')

	time.sleep(10)