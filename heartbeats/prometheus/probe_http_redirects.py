import requests
import json
import datetime

def get_probe_http_redirects(url, id, start=datetime.datetime.now().timestamp()):
    """
        Fetch prometheus probe duration seconds data
    """
    response = requests.get(f'{url}/api/v1/query?query=probe_http_redirects%7Bapplication="{id}"%7D&time={str(start)}')
    response.raise_for_status()
    content = json.loads(response.content)

    response = {}

    for service in content['data']['result']:
        service_id = int(service['metric']['service'])
        response[service_id] = {
            'http_redirects': int(service['value'][1])
        }

    return response