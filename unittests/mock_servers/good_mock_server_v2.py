from flask import Flask
from unittests.constants import GOOD_SERVER_V2_URL
from unittests.mock_servers.servers import GoodRefgetServerV2

good_server_host = GOOD_SERVER_V2_URL.split("://")[1].split(":")[0]
good_server_port = GOOD_SERVER_V2_URL.split("://")[1].split(":")[1].replace("/", "")

app = Flask(__name__)


server = GoodRefgetServerV2()


@app.route('/sequence/service-info', methods=['GET'])
def get_service_info():
    return server.get_service_info()


@app.route('/sequence/<seq_id>/metadata', methods=['GET'])
def get_metadata(seq_id):
    return server.get_metadata(seq_id)


@app.route('/sequence/<seq_id>', methods=['GET'])
def get_sequence(seq_id):
    return server.get_sequence(seq_id)


if __name__ == "__main__":
    app.run(host=good_server_host, port=good_server_port)