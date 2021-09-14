import os
import requests
import json
from dotenv import load_dotenv

# Load varriables from .env
load_dotenv()
SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
SERVER_URL = os.environ.get("SERVER")

SERVER_REGISTER_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/register'

# Fetch PROMETHEUS configuration files
print(f'Register server at {SERVER_REGISTER_URL}')
try:
    response = requests.get(SERVER_REGISTER_URL)
    response.raise_for_status()
except Exception as err:
    raise Exception(f'Error occurred: {err}')
