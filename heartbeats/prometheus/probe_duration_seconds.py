import requests
import json
import datetime


def query(url, type, id, start, duration=600)  :
    response = requests.get(f'{url}/api/v1/query_range?query=probe_duration_seconds%7B{type}="{id}"%7D&step=60&start={str(start-duration)}&end={str(start)}')
    response.raise_for_status()
    content = json.loads(response.content)

    response = {}
    # For each data set we introduice an empty title value which will be orverided by clients
    for service in content['data']['result']:
        service_id = int(service['metric']['service'])
        service['metric']['title'] = ''
        response[service_id] = {
            'duration_seconds': service['values'],
        }

        # We fill the beginnign of the array with 0 value to avoid out of sync data
        expected_length = int(duration / 60) + 1
        length = len(response[service_id]['duration_seconds'])

        if length < expected_length:
            for index in range(expected_length - length):
                date = (start-(60*index)-60*length)
                response[service_id]['duration_seconds'].insert(0, [date, 0])


    # Transform service['values'] array for each value 1 from string to float 
    for service_id in response:

        for i in range(len(response[service_id]['duration_seconds'])):
            response[service_id]['duration_seconds'][i][0] = int(response[service_id]['duration_seconds'][i][0])
            # From timestamp to datetime in python
            response[service_id]['duration_seconds'][i][0] = datetime.datetime.fromtimestamp(int(response[service_id]['duration_seconds'][i][0]))
            response[service_id]['duration_seconds'][i][1] = round(float(response[service_id]['duration_seconds'][i][1])*100, 2)

    return response

def get_probe_duration_seconds(url, id, start, duration=600):
    """
        Fetch prometheus probe duration seconds data
    """
    return query(url, 'project', id, start, duration)


def get_probe_duration_seconds_user(url, id, start, duration=600):
    """
        Fetch prometheus probe duration seconds data
    """
    return query(url, 'user', id, start, duration)
