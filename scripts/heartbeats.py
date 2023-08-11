import os
import requests
import json
import datetime
import time
import signal

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

IS_MONITORING_ENABLE = os.environ.get("DISABLE_MONITORING", '0') == '0'
IS_PERFORMANCE_ENABLE = os.environ.get("DISABLE_PERFORMANCE", '0') == '0'

HEADERS = {
    'User-Agent': 'FromEdwinBot Python heartbeats',
}

# Keep last update value to compare with the date of worker's setup.
last_update = None

# Class to handle graceful exit
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, *args):
    self.kill_now = True

# Main script running as a loop
if __name__ == '__main__':
    print(f'Heartbeat to {SERVER_HEARTBEATS_URL}')

    killer = GracefulKiller()
    while not killer.kill_now:
        try:

            payload = {}

            if not IS_MONITORING_ENABLE:
                payload['monitoring'] = 0
            if not IS_PERFORMANCE_ENABLE:
                payload['performance'] = 0

            # Send heartbeat request to server_url
            response = requests.get(SERVER_HEARTBEATS_URL, headers=HEADERS, params=payload)
            response.raise_for_status()

            # Look at the last_modified_setup value to compare with the date of worker's setup.
            content = json.loads(response.content)
            last_modified_setup = datetime.datetime.fromisoformat(content['last_modified_setup'].replace('Z', ''))

            # If worker config is older than the one on server, we reload it.
            if not last_update or last_update < last_modified_setup:
                last_update = last_modified_setup
                load_config.load_config(SERVER_URL)

        except Exception as err:
            print(f'[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}')
        except KeyboardInterrupt as ex:
            print('goodbye!')
            break

        # Wait 10 seconds to send the next heartbeats
        time.sleep(10)
