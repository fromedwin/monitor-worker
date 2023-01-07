import os
import requests
import json
import datetime
import time

import sys
import load_config
from dotenv import load_dotenv

try:
	del os.environ["UUID"]
except:
	pass

# Load varriables from .env
load_dotenv()
SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
SERVER_URL = os.environ.get("SERVER") or 'host.docker.internal:8000'
UUID = os.environ.get("UUID")

SERVER_HEARTBEATS_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/heartbeat/{UUID}'

# Print Heartbeat
print(f'Heartbeat to {SERVER_HEARTBEATS_URL}')

last_update = None
headers = {
    'User-Agent': 'FromEdwinBot Python heartbeats',
}

while True:
	try:
	    response = requests.get(SERVER_HEARTBEATS_URL, headers=headers)
	    response.raise_for_status()

	    content = json.loads(response.content)
	    last_modified_setup = datetime.datetime.fromisoformat(content['last_modified_setup'].replace('Z', ''))

	    if not last_update or last_update < last_modified_setup:
	    	last_update = last_modified_setup
	    	load_config.load_config(SERVER_URL)

	except Exception as err:
		print(f'Error occurred: {err}')

	time.sleep(10)