import os
import requests
import json
from dotenv import load_dotenv
import datetime

last_load = datetime.datetime.now()

def load_config(url=None):

    global last_load

    # Load varriables from .env
    load_dotenv()
    SERVER_PROTOCOL = 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
    SERVER_URL = url or os.environ.get("SERVER")
    UUID = os.environ.get("UUID")

    SERVER_PROMETHEUS_CONFIG_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/prometheus/{UUID}'
    SERVER_ALERTS_CONFIG_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/alerts/'

    print(f'{os.path.dirname( __file__ )}')
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
        with open(f'{os.path.dirname( __file__ )}/../prometheus/prometheus.yml', 'w') as file:
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
            with open(f'{os.path.dirname( __file__ )}/../prometheus/alerts/{config["title"]}.yml', 'w') as file:
                file.write(config['yaml'])
                file.close()

    now = datetime.datetime.now()

    if (now - last_load).seconds >= 30:
        try:
            response = requests.post('http://prometheus:9090/-/reload')
            response.raise_for_status()
        except Exception as err:
            pass
        last_load = now

if __name__== "__main__" :
    load_config(os.environ.get("SERVER") or 'localhost:8000')
