import requests
import json
import datetime

def query(url, type, id, start=datetime.datetime.now().timestamp()):
    """
        Fetch prometheus probe duration seconds data
    """
    response = requests.get(f'{url}/api/v1/query?query=probe_http_version%7B{type}="{id}"%7D&time={str(start)}')
    response.raise_for_status()
    content = json.loads(response.content)

    response = {}

    for service in content['data']['result']:
        service_id = int(service['metric']['service'])
        response[service_id] = {
            'http_version': service['value'][1]
        }

    return response


def get_probe_http_version(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'project', id, start)

def get_probe_http_version_user(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'user', id, start)