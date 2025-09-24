import requests

def test_health():
    res = requests.get('http://localhost:5000/api/health')
    assert res.status_code == 200
    assert res.json().get('status') == 'ok'
