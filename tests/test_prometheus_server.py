from requests import get


def test_prometheus_server(client):
    response = get("http://localhost:8080/metrics")
    assert response.status_code == 200
