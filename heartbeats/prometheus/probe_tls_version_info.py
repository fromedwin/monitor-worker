import requests
import json
import datetime

def query(url, type, id, start=datetime.datetime.now().timestamp()):
    """
        Fetch prometheus probe duration seconds data
    """
    response = requests.get(f'{url}/api/v1/query?query=probe_tls_version_info%7B{type}="{id}"%7D&time={str(start)}')
    response.raise_for_status()
    content = json.loads(response.content)

    https = {}
    for service in content['data']['result']:
        service_id = int(service['metric']['service'])
        https[service_id] = service['metric']['version']

    return https


def get_probe_tls_version_info(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'project', id, start)
    
def get_probe_tls_version_info_user(url, id, start=datetime.datetime.now().timestamp()):
    return query(url, 'user', id, start)