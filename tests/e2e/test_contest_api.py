import os

from fastapi.testclient import TestClient
from dotenv import load_dotenv

load_dotenv()
URL_PREFIX = os.getenv("URL_PREFIX", "")


def test_get_contest(client: TestClient):
    """Test GET {URL_PREFIX}/api/contests/{contest_id}."""

    response = client.get(f"{URL_PREFIX}/api/contest")

    assert response.status_code == 200
    json = response.json()
    assert json["status"] == "ok"

    contest = json["contests"]
    assert len(contest) == 4
