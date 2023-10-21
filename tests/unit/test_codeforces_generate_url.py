import requests

from etr.library.codeforces.utils.generate_url import generate_url


def test_generate_url_contest_standings():
    url = generate_url("contest.standings", contestId="1234", from_=1, count=5)
    
    response = requests.get(url)
    assert response.status_code == 200, "Status code is not 200. Check generate_url def or network connection."


def test_generate_url_user_info():
    url = generate_url("user.info", handles="tourist")
    
    response = requests.get(url)
    assert response.status_code == 200, "Status code is not 200. Check generate_url def or network connection."
