import requests


def test_request_response(server):
    test_url = server + 'sequence/2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785'
    response = requests.get(test_url)
    assert response.status_code == 200
