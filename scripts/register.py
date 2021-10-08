import os
import requests
import json
import dotenv

def register(url):
    # Load varriables from .env
    dotenv.load_dotenv()
    SERVER_PROTOCOL = os.environ.get("PROTOCOL") or 'http' # if os.environ.get("PRODUCTION") == '0' else 'https'
    SERVER_URL = os.environ.get("SERVER") or url

    SERVER_REGISTER_URL = f'{SERVER_PROTOCOL}://{SERVER_URL}/clients/register'

    # Fetch PROMETHEUS configuration files
    print(f'Register server at {SERVER_REGISTER_URL}')
    try:
        response = requests.get(SERVER_REGISTER_URL)
        response.raise_for_status()

        json = response.json()
        os.environ["UUID"] = json["uuid"]
        print(os.environ.get("UUID"))
        dotenv.set_key(dotenv.find_dotenv(), "UUID", json["uuid"])

    except Exception as err:
        raise Exception(f'Error occurred: {err}')

if __name__== "__main__" :
    register('localhost:8000')