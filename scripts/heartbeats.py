import os
import requests
import json
from dotenv import load_dotenv
import time as time

del os.environ["UUID"]
# Load varriables from .env
load_dotenv()
SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
SERVER_URL = os.environ.get("SERVER")
UUID = os.environ.get("UUID")

SERVER_HEARTBEATS_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/heartbeat/{UUID}'

# Print Heartbeat
print(f'Heartbeat to {SERVER_HEARTBEATS_URL}')

while True:
	try:
	    response = requests.get(SERVER_HEARTBEATS_URL)
	    response.raise_for_status()
	except Exception as err:
	    raise Exception(f'Error occurred: {err}')

	print('.')
	time.sleep(10)