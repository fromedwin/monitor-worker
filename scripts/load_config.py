import os
import requests
import json
from dotenv import load_dotenv
import datetime

headers = {
    'User-Agent': 'FromEdwinBot Python load_config',
}

# Fetch Prometheur, alertmanager, and alert rules from server_url
def load_config(url=None):

    load_dotenv()

    DISABLE_MONITORING = os.environ.get("DISABLE_MONITORING", '0')

    if DISABLE_MONITORING == '1' or DISABLE_MONITORING == 1:
        print('❌ DISABLE_MONITORING == 1, disabling prometheus monitoring')
        return

    # Server url
    SERVER_URL = os.environ.get("SERVER_URL") or url
    # worked id to fetch  assigned config files
    UUID = os.environ.get("UUID")

    # Fetch PROMETHEUS configuration files
    SERVER_PROMETHEUS_CONFIG_URL = f'{SERVER_URL}/clients/prometheus/{UUID}/'
    print(f'Loading PROMETHEUS configuration files at {SERVER_PROMETHEUS_CONFIG_URL}')
    try:
        response = requests.get(SERVER_PROMETHEUS_CONFIG_URL, headers=headers)
        response.raise_for_status()
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Prometheus have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../prometheus/prometheus.yml', 'w') as file:
            file.write(content)
            file.close()

    # Fetch ALERTS configuration files
    SERVER_ALERTS_CONFIG_URL = f'{SERVER_URL}/clients/alerts/{UUID}/'
    print(f'Loading ALERTS configuration files at {SERVER_ALERTS_CONFIG_URL}')
    try:
        response = requests.get(SERVER_ALERTS_CONFIG_URL, headers=headers)
        response.raise_for_status()
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Alerts have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../prometheus/alerts/alerts.yml', 'w') as file:
            file.write(content)
            file.close()


    # Fetch ALERTS configuration files
    SERVER_ALERTMANAGER_CONFIG_URL = f'{SERVER_URL}/clients/alertmanager/{UUID}/'
    print(f'Loading ALERTMANAGER configuration files at {SERVER_ALERTMANAGER_CONFIG_URL}')
    try:
        response = requests.get(SERVER_ALERTMANAGER_CONFIG_URL, headers=headers)
        response.raise_for_status()
    except Exception as err:
        raise Exception(f"[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: {err}")
    else:
        content = response.text
        print(f'> Alertmanager have been loaded from {SERVER_URL}')
        with open(f'{os.path.dirname( __file__ )}/../alertmanager/alertmanager.yml', 'w') as file:
            file.write(content)
            file.close()

    # When all config files are locally stored, 
    # script notify prometheus and alertmanager to reload.
    try:
        response = requests.post('http://prometheus:9090/-/reload', headers=headers)
        response.raise_for_status()
    except Exception as err:
        print(f'Prometheus reload failed: {err}')

    try:
        response = requests.post('http://alertmanager:9093/-/reload', headers=headers)
        response.raise_for_status()
    except Exception as err:
        print(f'Alertmanager reload failed: {err}')

if __name__== "__main__" :

    load_config(os.environ.get("SERVER_URL") or 'http://localhost:8000')
