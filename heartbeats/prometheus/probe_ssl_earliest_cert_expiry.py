import requests
import json
import datetime

def query(url, type, id, start=datetime.datetime.now().timestamp()):
    """
        Fetch prometheus probe duration seconds data
    """
    response = requests.get(f'{url}/api/v1/query?query=probe_ssl_earliest_cert_expiry%7B{type}="{id}"%7D&time={str(start)}')
    response.raise_for_status()
    content = json.loads(response.content)

    https = {}
    for service in content['data']['result']:
        service_id = int(service['metric']['service'])
        https[service_id] = int(service['value'][1]) # datetime.datetime.fromtimestamp()

    return https


def get_probe_ssl_earliest_cert_expiry(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'application', id, start)

def get_probe_ssl_earliest_cert_expiry_user(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'user', id, start)