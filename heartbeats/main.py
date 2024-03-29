import requests
import datetime
import json

from fastapi import FastAPI
from typing import Union

from prometheus.probe_http_status_code import get_probe_http_status_code
from prometheus.probe_duration_seconds import get_probe_duration_seconds
from prometheus.probe_ssl_earliest_cert_expiry import get_probe_ssl_earliest_cert_expiry
from prometheus.probe_http_redirects import get_probe_http_redirects
from prometheus.probe_http_version import get_probe_http_version
from prometheus.probe_tls_version_info import get_probe_tls_version_info

from prometheus.probe_http_status_code import get_probe_http_status_code_user
from prometheus.probe_duration_seconds import get_probe_duration_seconds_user
from prometheus.probe_ssl_earliest_cert_expiry import get_probe_ssl_earliest_cert_expiry_user
from prometheus.probe_http_redirects import get_probe_http_redirects_user
from prometheus.probe_http_version import get_probe_http_version_user
from prometheus.probe_tls_version_info import get_probe_tls_version_info_user

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": 200, "message": "OK"}

# http://127.0.0.1:8001/fastapi/items/5?q=somequery
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/availability/{project_id}")
def read_availability(project_id: int, duration: Union[int, None] = 600):

    # Prometheus run locally in a parallel docker image as defined in docker-compose.yml
    url = 'http://prometheus:9090'
    # Return result content as json
    result = {
        'id': project_id,
        'duration': duration,
        'services': {}, # Create dict with service_id as index {35: '', 70: '', ...}
        'errors': {},
    }
    # Define start value on each request
    start = datetime.datetime.now().timestamp()

    # Get http code for each service
    try:
        http_status_code = get_probe_http_status_code(url, project_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_status_code:
            result['services'][service_id] = {
                'http_code': http_status_code[service_id]['http_code']
            }
    except Exception as err:
        result['errors']['get_probe_http_status_code'] = getattr(err, 'message', repr(err))

    # Get http version for each service
    try:
        http_status_version = get_probe_http_version(url, project_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_status_version:
            result['services'][service_id]['http_version'] = http_status_version[service_id]['http_version']
    except Exception as err:
        result['errors']['get_probe_http_version'] = getattr(err, 'message', repr(err))

    # Get number of redirection
    try:
        http_redirects = get_probe_http_redirects(url, project_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_redirects:
            result['services'][service_id]['http_redirects'] = http_redirects[service_id]['http_redirects']
    except Exception as err:
        result['errors']['get_probe_http_redirects'] = getattr(err, 'message', repr(err))

    # Get each ping duration
    try:
        duration_seconds = get_probe_duration_seconds(url, project_id, start, duration)
        for service_id in duration_seconds:
            if service_id in result['services']:
                result['services'][service_id]['duration_seconds'] = duration_seconds[service_id]['duration_seconds']

    except Exception as err:
        result['errors']['get_probe_duration_seconds'] = getattr(err, 'message', repr(err))

    # Get HTTPS certificate expiry as timestamp
    try:
        ssl_earliest_cert_expiry = get_probe_ssl_earliest_cert_expiry(url, project_id, start)
        for service_id in ssl_earliest_cert_expiry:
            result['services'][service_id]['ssl_earliest_cert_expiry'] = ssl_earliest_cert_expiry[service_id]
    except Exception as err:
        result['errors']['get_probe_ssl_earliest_cert_expiry'] = getattr(err, 'message', repr(err))

    # Get HTTPS certificate expiry as timestamp
    try:
        tls_version_info = get_probe_tls_version_info(url, project_id, start)
        for service_id in tls_version_info:
            result['services'][service_id]['tls_version_info'] = tls_version_info[service_id]
    except Exception as err:
        result['errors']['get_probe_tls_version_info'] = getattr(err, 'message', repr(err))
        
    return result

@app.get("/availabilities/{user_id}")
def read_availabilities(user_id: int, duration: Union[int, None] = 600):

    # Prometheus run locally in a parallel docker image as defined in docker-compose.yml
    url = 'http://prometheus:9090'
    # Return result content as json
    result = {
        'id': user_id,
        'duration': duration,
        'services': {}, # Create dict with service_id as index {35: '', 70: '', ...}
        'errors': {},
    }
    # Define start value on each request
    start = datetime.datetime.now().timestamp()

    # Get http code for each service
    try:
        http_status_code = get_probe_http_status_code_user(url, user_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_status_code:
            result['services'][service_id] = {
                'http_code': http_status_code[service_id]['http_code']
            }
    except Exception as err:
        result['errors']['get_probe_http_status_code'] = getattr(err, 'message', repr(err))

    # Get http version for each service
    try:
        http_status_version = get_probe_http_version_user(url, user_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_status_version:
            result['services'][service_id]['http_version'] = http_status_version[service_id]['http_version']
    except Exception as err:
        result['errors']['get_probe_http_version'] = getattr(err, 'message', repr(err))

    # Get number of redirection
    try:
        http_redirects = get_probe_http_redirects_user(url, user_id, start)
        # Initialise list of service based on status_code value
        for service_id in http_redirects:
            result['services'][service_id]['http_redirects'] = http_redirects[service_id]['http_redirects']
    except Exception as err:
        result['errors']['get_probe_http_redirects'] = getattr(err, 'message', repr(err))

    # Get each ping duration
    try:
        duration_seconds = get_probe_duration_seconds_user(url, user_id, start, duration)
        for service_id in duration_seconds:
            if service_id in result['services']:
                result['services'][service_id]['duration_seconds'] = duration_seconds[service_id]['duration_seconds']

    except Exception as err:
        result['errors']['get_probe_duration_seconds'] = getattr(err, 'message', repr(err))

    # Get HTTPS certificate expiry as timestamp
    try:
        ssl_earliest_cert_expiry = get_probe_ssl_earliest_cert_expiry_user(url, user_id, start)
        for service_id in ssl_earliest_cert_expiry:
            result['services'][service_id]['ssl_earliest_cert_expiry'] = ssl_earliest_cert_expiry[service_id]
    except Exception as err:
        result['errors']['get_probe_ssl_earliest_cert_expiry'] = getattr(err, 'message', repr(err))

    # Get HTTPS certificate expiry as timestamp
    try:
        tls_version_info = get_probe_tls_version_info_user(url, user_id, start)
        for service_id in tls_version_info:
            result['services'][service_id]['tls_version_info'] = tls_version_info[service_id]
    except Exception as err:
        result['errors']['get_probe_tls_version_info'] = getattr(err, 'message', repr(err))

    return result

