import os
import requests
import json
import datetime
import time

import sys
import load_config
from dotenv import load_dotenv

# Delete existing UUID env var to make sure the one from .env is taking into account.
# It might still exist in case of restart.
try:
	del os.environ["UUID"]
except:
	pass

# Load varriables from .env
load_dotenv()

# Collect and generate vars
SERVER_URL = os.environ.get("SERVER_URL") or 'http://host.docker.internal:8000'
UUID = os.environ.get("UUID")
SERVER_HEARTBEATS_URL = f'{SERVER_URL}/clients/heartbeat/{UUID}/'

print(f'Heartbeat to {SERVER_HEARTBEATS_URL}')

last_update = None
headers = {
    'User-Agent': 'FromEdwinBot Python heartbeats',
}

while True:
	try:
		# Send heartbeat request to server_url
	    response = requests.get(SERVER_HEARTBEATS_URL, headers=headers)
	    response.raise_for_status()

	    # Look at the last_modified_setup value to compare with the date of worker's setup.
	    content = json.loads(response.content)
	    last_modified_setup = datetime.datetime.fromisoformat(content['last_modified_setup'].replace('Z', ''))

	    # If worker config is older than the one on server, we reload it.
	    if not last_update or last_update < last_modified_setup:
	    	last_update = last_modified_setup
	    	load_config.load_config(SERVER_URL)

	except Exception as err:
		print(f'Error occurred: {err}')

	# Wait 10 seconds to send the next heartbeats
	time.sleep(10)