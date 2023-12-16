import os

from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv()
URL_PREFIX = os.getenv("URL_PREFIX", "")


def test_patch_user(client: TestClient):
    response = client.patch(f"{URL_PREFIX}/api/user/1", json={
        "first_name": "Evgeniy",
        "last_name": "Onegin",
        "city": "Moscow",
        "country": "Russia",
        "organization": "GSU",
        "rank": "master",
        "max_rank": "master",
        "email": "test@mail.com"
    })

    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["result"] is not None
    assert json["result"]["city"] == "Moscow"
    assert json["result"]["contribution"] is None
    assert json["result"]["country"] == "Russia"
    assert json["result"]["email"] == "test@mail.com"
    assert json["result"]["first_name"] == "Evgeniy"
    assert json["result"]["last_name"] == "Onegin"
    assert json["result"]["organization"] == "GSU"
    assert json["result"]["rank"] == "master"
    assert json["result"]["max_rank"] == "master"

    response = client.get(f"{URL_PREFIX}/api/user/?handles=Senior")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["users"] is not None
    assert len(json["users"]) == 1
    assert json["users"][0]["city"] == "Moscow"
    assert json["users"][0]["country"] == "Russia"
    assert json["users"][0]["email"] == "test@mail.com"


def test_get_users(client: TestClient):
    response = client.get(f"{URL_PREFIX}/api/user/")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["users"] is not None
    assert len(json["users"]) == 5


def test_get_users_by_handle(client: TestClient):
    response = client.get(f"{URL_PREFIX}/api/user/?handles=Senior")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["users"] is not None
    assert len(json["users"]) == 1
    user = response.json()["users"][0]
    assert user["avatar"] == "https://dl.gsu.by/avatars/senior.png"
    assert user["city"] == "Gomel"
    assert user["contribution"] is None
    assert user["country"] == "Belarus"
    assert user["email"] == "senior@mail.ru"
    assert user["first_name"] == "Senior"
    assert user["friend_of_count"] == 1
    assert user["handle"] == "Senior"
    assert user["id"] == 1
    assert user["last_name"] == "Senior"
    assert user["last_online_time_seconds"] == 1614552000
    assert user["max_rank"] == "master"
    assert user["max_rating"] is None
    assert user["open_id"] == "open_id0"
    assert user["organization"] == "GSU"
    assert user["rank"] == "master"
    assert user["rating"] is None
    assert user["registration_time_seconds"] == 12312314
    assert user["title_photo"] == "https://dl.gsu.by/title_photos/senior.png"
    assert user["vk_id"] == "vk.com/id0"


def test_get_users_by_city(client: TestClient):
    response = client.get(f"{URL_PREFIX}/api/user/?city=Gomel")
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["users"] is not None
    assert len(json["users"]) == 2

    users = response.json()["users"]
    assert len(users) == 2


def test_post_user(client: TestClient):
    response = client.post(f"{URL_PREFIX}/api/user/", json={
        "handle": "inaFSTream"
    })
    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"
    assert json["user"] is not None
    assert json["user"]["avatar"] == "https://userpic.codeforces.org/no-avatar.jpg"
    assert json["user"]["city"] is None
    assert json["user"]["country"] is None
    assert json["user"]["email"] is None
    assert json["user"]["first_name"] is None
    assert json["user"]["handle"] == "inaFSTream"
    assert json["user"]["id"] == 6
    assert json["user"]["last_name"] is None
    assert json["user"]["max_rank"] == "легендарный гроссмейстер"
    assert json["user"]["max_rating"] == 3478
    assert json["user"]["open_id"] is None
    assert json["user"]["organization"] == ""
    assert json["user"]["rank"] == "легендарный гроссмейстер"
    assert json["user"]["rating"] == 3478
    assert json["user"]["registration_time_seconds"] == 1515819239
    assert json["user"]["title_photo"] == "https://userpic.codeforces.org/no-title.jpg"
    assert json["user"]["vk_id"] is None
