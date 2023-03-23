import requests
import datetime
import json

from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": 200, "message": "OK"}

# http://127.0.0.1:8001/fastapi/items/5?q=somequery
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/availability/{service_id}")
def read_availability(service_id: int):

    try:
        href = 'http://prometheus:9090'

        start = datetime.datetime.now().timestamp()

        """
            Fetch prometheus probe duration seconds data
        """
        response = requests.get(f'{href}/api/v1/query_range?query=probe_duration_seconds%7Bapplication="{service_id}"%7D&step=30&start={str(start-600)}&end={str(start)}')
        response.raise_for_status()
        content = json.loads(response.content)
        for service in content['data']['result']:
            service['metric']['title'] = ''

        graph = json.dumps(content)
        """
            Fetch prometheus https expiration value
        """
        response = requests.get(f'{href}/api/v1/query?query=probe_ssl_earliest_cert_expiry%7Bapplication="{service_id}"%7D&time={str(start)}')
        response.raise_for_status()
        content = json.loads(response.content)
        https = {}
        for service in content['data']['result']:
            https[service['metric']['service']] = int(service['value'][1]) # datetime.datetime.fromtimestamp()

    except Exception as err:
        content = {
            'error': getattr(err, 'message', repr(err))
        }

    return {
        "service_id": service_id, 
        "https": https, 
        "graph": graph,
    }
