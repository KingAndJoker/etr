import time

import requests

from etr.utils.singletonmeta import SingletonMeta


# TODO: переписать под очередь
class Request(metaclass=SingletonMeta):
    last_request_time: float

    def __init__(self) -> None:
        self.last_request_time = time.time()

    def handle(self, url, method):
        delay = max(0., self.last_request_time + 2. - time.time())
        self.last_request_time = time.time() + delay
        time.sleep(delay)
        if method == "GET":
            return self.get(url)
        

    def get(self, url):
        return requests.get(url)
