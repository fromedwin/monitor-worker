import os
import requests
import json
import dotenv

from urllib import parse

DEFAULT_SERVER_URL = 'http://localhost:8000'
DEFAULT_WORKER_URL = 'http://localhost:8001'

def register(url):

    dotenv.load_dotenv()
    
    # Register function send to the server details about how to access it (url, username, password).
    # It receive back its unique identifier and store it within the .env file.

    SERVER_URL = os.environ.get("SERVER_URL") or url
    SERVER_REGISTER_URL = f'{SERVER_URL}/clients/register?'

    # Generate URL as SERVER_REGISTER_URL var with setup informations:
    # username: basicauth username to access prometheus API
    # password: basicauth password to access prometheus API
    # worker_url: url to access worker's APIs
    params = {}
    if os.environ.get("WEBAUTH_USERNAME"):
        params['username'] = os.environ.get("WEBAUTH_USERNAME")

    if os.environ.get("WEBAUTH_PASSWORD"):
        params['password'] = os.environ.get("WEBAUTH_PASSWORD")

    if os.environ.get("WORKER_URL"):
        params['url'] = os.environ.get("WORKER_URL")
    else:
        params['url'] = DEFAULT_WORKER_URL

    SERVER_REGISTER_URL = SERVER_REGISTER_URL + parse.urlencode(params)

    # Send registration request to SERVER_URL and receive worker's identifier (uuid)
    print(f'Register server at {SERVER_REGISTER_URL}')
    try:
        response = requests.get(SERVER_REGISTER_URL)
        response.raise_for_status()

        json = response.json()
        os.environ["UUID"] = json["uuid"]

        # Store UUID within .env file to access from anywhere
        print(os.environ.get("UUID"))
        dotenv.set_key(dotenv.find_dotenv(), "UUID", json["uuid"])

    except Exception as err:
        raise Exception(f'Error occurred: {err}')

if __name__== "__main__" :

    # Send register request
    register(DEFAULT_SERVER_URL)