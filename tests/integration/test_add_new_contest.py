from fastapi.testclient import TestClient


def test_add_new_contest(client: TestClient):
    response = client.post("/etr/contest/new", data={"contest_url": "https://codeforces.com/contest/403/"})
    assert response.status_code == 200
    
    response = client.get("/etr/rpc/submission/403")
    assert response.status_code == 200
    
    response = client.get("/etr/api/user/Petr/contests")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
