import os

import pytest
from flask import Flask
from flask.testing import FlaskClient
from dotenv import load_dotenv

load_dotenv()
URL_PREFIX = os.getenv("URL_PREFIX", "")


def test_get_users(client: FlaskClient):
    response = client.get(f"{URL_PREFIX}/api/user/")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["users"] is not None
    assert len(response.json["users"]) == 5
    assert response.json == {
        "status": "ok",
        "users": [
            {
                "avatar": "https://dl.gsu.by/avatars/senior.png",
                "city": "Gomel",
                "contribution": None,
                "country": "Belarus",
                "email": "senior@mail.ru",
                "first_name": "Senior",
                "friend_of_count": 1,
                "handle": "Senior",
                "id": 1,
                "last_name": "Senior",
                "last_online_time_seconds": 1614552000,
                "max_rank": "master",
                "max_rating": None,
                "open_id": "open_id0",
                "organization": "GSU",
                "rank": "master",
                "rating": None,
                "registration_time_seconds": 12312314,
                "title_photo": "https://dl.gsu.by/title_photos/senior.png",
                "vk_id": "vk.com/id0"
            },
            {
                "avatar": None,
                "city": None,
                "contribution": None,
                "country": None,
                "email": None,
                "first_name": None,
                "friend_of_count": None,
                "handle": "chelovek_secret",
                "id": 2,
                "last_name": None,
                "last_online_time_seconds": None,
                "max_rank": None,
                "max_rating": None,
                "open_id": None,
                "organization": None,
                "rank": None,
                "rating": None,
                "registration_time_seconds": None,
                "title_photo": None,
                "vk_id": None
            },
            {
                "avatar": None,
                "city": "Moscow",
                "contribution": None,
                "country": "Russia",
                "email": None,
                "first_name": "Petr",
                "friend_of_count": None,
                "handle": "Petr",
                "id": 3,
                "last_name": "Mitrichev",
                "last_online_time_seconds": None,
                "max_rank": "legendary grandmaster",
                "max_rating": None,
                "open_id": None,
                "organization": "MIPT",
                "rank": "legendary grandmaster",
                "rating": None,
                "registration_time_seconds": None,
                "title_photo": None,
                "vk_id": None
            },
            {
                "avatar": None,
                "city": "St. Petersburg",
                "contribution": None,
                "country": "Russia",
                "email": None,
                "first_name": "Nikita",
                "friend_of_count": None,
                "handle": "Um_nik",
                "id": 4,
                "last_name": "Belyh",
                "last_online_time_seconds": None,
                "max_rank": "legendary grandmaster",
                "max_rating": None,
                "open_id": None,
                "organization": "ITMO",
                "rank": "legendary grandmaster",
                "rating": None,
                "registration_time_seconds": None,
                "title_photo": None,
                "vk_id": None
            },
            {
                "avatar": None,
                "city": "Gomel",
                "contribution": None,
                "country": "Belarus",
                "email": None,
                "first_name": "Gennady",
                "friend_of_count": None,
                "handle": "tourist",
                "id": 5,
                "last_name": "Korotkevich",
                "last_online_time_seconds": None,
                "max_rank": "legendary grandmaster",
                "max_rating": None,
                "open_id": None,
                "organization": "ITMO",
                "rank": "legendary grandmaster",
                "rating": None,
                "registration_time_seconds": None,
                "title_photo": None,
                "vk_id": "vk.com/id0"
            }
        ]
    }


def test_get_users_by_handle(client: FlaskClient):
    response = client.get(f"{URL_PREFIX}/api/user/?handles=Senior")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["users"] is not None
    assert len(response.json["users"]) == 1
    assert response.json == {
        "status": "ok",
        "users": [
            {
                "avatar": "https://dl.gsu.by/avatars/senior.png",
                "city": "Gomel",
                "contribution": None,
                "country": "Belarus",
                "email": "senior@mail.ru",
                "first_name": "Senior",
                "friend_of_count": 1,
                "handle": "Senior",
                "id": 1,
                "last_name": "Senior",
                "last_online_time_seconds": 1614552000,
                "max_rank": "master",
                "max_rating": None,
                "open_id": "open_id0",
                "organization": "GSU",
                "rank": "master",
                "rating": None,
                "registration_time_seconds": 12312314,
                "title_photo": "https://dl.gsu.by/title_photos/senior.png",
                "vk_id": "vk.com/id0"
            }
        ]
    }


def test_get_users_by_city(client: FlaskClient):
    response = client.get(f"{URL_PREFIX}/api/user/?city=Gomel")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["users"] is not None
    assert len(response.json["users"]) == 2

    users = response.json["users"]
    assert len(users) == 2
    if users[0]["handle"] == "Senior":
        assert users[0] == {
            "avatar": "https://dl.gsu.by/avatars/senior.png",
            "city": "Gomel",
            "contribution": None,
            "country": "Belarus",
            "email": "senior@mail.ru",
            "first_name": "Senior",
            "friend_of_count": 1,
            "handle": "Senior",
            "id": 1,
            "last_name": "Senior",
            "last_online_time_seconds": 1614552000,
            "max_rank": "master",
            "max_rating": None,
            "open_id": "open_id0",
            "organization": "GSU",
            "rank": "master",
            "rating": None,
            "registration_time_seconds": 12312314,
            "title_photo": "https://dl.gsu.by/title_photos/senior.png",
            "vk_id": "vk.com/id0"
        }
        assert users[1] == {
            "avatar": None,
            "city": "Gomel",
            "contribution": None,
            "country": "Belarus",
            "email": None,
            "first_name": "Gennady",
            "friend_of_count": None,
            "handle": "tourist",
            "id": 5,
            "last_name": "Korotkevich",
            "last_online_time_seconds": None,
            "max_rank": "legendary grandmaster",
            "max_rating": None,
            "open_id": None,
            "organization": "ITMO",
            "rank": "legendary grandmaster",
            "rating": None,
            "registration_time_seconds": None,
            "title_photo": None,
            "vk_id": "vk.com/id0"
        }
    else:
        assert users[1] == {
            "avatar": "https://dl.gsu.by/avatars/senior.png",
            "city": "Gomel",
            "contribution": None,
            "country": "Belarus",
            "email": "senior@mail.ru",
            "first_name": "Senior",
            "friend_of_count": 1,
            "handle": "Senior",
            "id": 1,
            "last_name": "Senior",
            "last_online_time_seconds": 1614552000,
            "max_rank": "master",
            "max_rating": None,
            "open_id": "open_id0",
            "organization": "GSU",
            "rank": "master",
            "rating": None,
            "registration_time_seconds": 12312314,
            "title_photo": "https://dl.gsu.by/title_photos/senior.png",
            "vk_id": "vk.com/id0"
        }
        assert users[0] == {
            "avatar": None,
            "city": "Gomel",
            "contribution": None,
            "country": "Belarus",
            "email": None,
            "first_name": "Gennady",
            "friend_of_count": None,
            "handle": "tourist",
            "id": 5,
            "last_name": "Korotkevich",
            "last_online_time_seconds": None,
            "max_rank": "legendary grandmaster",
            "max_rating": None,
            "open_id": None,
            "organization": "ITMO",
            "rank": "legendary grandmaster",
            "rating": None,
            "registration_time_seconds": None,
            "title_photo": None,
            "vk_id": "vk.com/id0"
        }


def test_post_user(client: FlaskClient):
    response = client.post(f"{URL_PREFIX}/api/user/", json={
        "handle": "inaFSTream"
    })
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["user"] is not None
    assert response.json["user"]["avatar"] == "https://userpic.codeforces.org/no-avatar.jpg"
    assert response.json["user"]["city"] is None
    assert response.json["user"]["contribution"] == 0
    assert response.json["user"]["country"] is None
    assert response.json["user"]["email"] is None
    assert response.json["user"]["first_name"] is None
    assert response.json["user"]["friend_of_count"] == 371
    assert response.json["user"]["handle"] == "inaFSTream"
    assert response.json["user"]["id"] is None
    assert response.json["user"]["last_name"] is None
    assert response.json["user"]["max_rank"] == "legendary grandmaster"
    assert response.json["user"]["max_rating"] == 3478
    assert response.json["user"]["open_id"] is None
    assert response.json["user"]["organization"] == ""
    assert response.json["user"]["rank"] == "legendary grandmaster"
    assert response.json["user"]["rating"] == 3478
    assert response.json["user"]["registration_time_seconds"] == 1515819239
    assert response.json["user"]["title_photo"] == "https://userpic.codeforces.org/no-title.jpg"
    assert response.json["user"]["vk_id"] is None


def test_patch_user(client: FlaskClient):
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
    assert response.json["status"] == "ok"
    assert response.json["result"] is not None
    assert response.json["result"]["city"] == "Moscow"
    assert response.json["result"]["contribution"] is None
    assert response.json["result"]["country"] == "Russia"
    assert response.json["result"]["email"] == "test@mail.com"
    assert response.json["result"]["first_name"] == "Evgeniy"
    assert response.json["result"]["last_name"] == "Onegin"
    assert response.json["result"]["organization"] == "GSU"
    assert response.json["result"]["rank"] == "master"
    assert response.json["result"]["max_rank"] == "master"

    response = client.get(f"{URL_PREFIX}/api/user/?handles=Senior")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["users"] is not None
    assert len(response.json["users"]) == 1
    assert response.json["users"][0]["city"] == "Moscow"
    assert response.json["users"][0]["country"] == "Russia"
    assert response.json["users"][0]["email"] == "test@mail.com"
