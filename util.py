import requests
from datetime import datetime

from cachetools import cached, LRUCache

cache = LRUCache(maxsize=100)


def get_local_time(timestamp: int):
    return datetime.fromtimestamp(timestamp / 1000)


def check_valid_response(responses) -> None:
    if responses.status_code != 200:
        print('Error : response status code =', responses.status_code)


def check_list_length(data: list) -> None:
    if len(data) == 0:
        print('Error: No data')


def print_as_at(timestamp: int) -> None:
    print("Data is got at : ",
          get_local_time(timestamp)
          )


@cached(cache)
def get_data_from_API(url: str) -> list:
    responses = requests.get(url)
    check_valid_response(responses)
    data = responses.json()
    check_list_length(data['data'])
    print_as_at(data['timestamp'])
    return data['data']
