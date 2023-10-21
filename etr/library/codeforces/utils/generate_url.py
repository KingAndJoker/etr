import os
import time
import random
import string
import hashlib
from dotenv import load_dotenv


load_dotenv()
CODEFORCES_API_KEY = os.getenv("CODEFORCES_API_KEY", None)
CODEFORCES_API_SECRET = os.getenv("CODEFORCES_API_SECRET", None)


def generate_url(method: str, **kwargs) -> str:
    apiKey = CODEFORCES_API_KEY
    time_ = int(time.time())
    rand = _random_str()
    params = _make_params(**kwargs, apiKey=apiKey, time=time_)

    apiSig = hashlib.sha512(f"{rand}/{method}?{params}#{CODEFORCES_API_SECRET}".encode()).hexdigest()

    url = f"https://codeforces.com/api/{method}?{params}&apiSig={rand}{apiSig}"

    return url


def _make_params(**kwargs) -> str:
    """ Make params for url """
    params = ""
    for key, value in sorted(kwargs.items()):
        if value is not None:
            params += _pair_key_value(key, value)
    return params[:-1]


def _pair_key_value(key: str, value) -> str:
    """ Pair key and value """
    if key == "from_":
        key = "from"
    if key == "count_":
        key = "count"
    return f"{key}={value}&"


def _random_str(length: int = 6, symbols: str = string.ascii_letters):
    """ Generate random string """
    return ''.join(random.choice(symbols) for i in range(length))
