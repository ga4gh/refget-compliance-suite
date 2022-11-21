from flask import Flask
from unittests.constants import BAD_SERVER_V2_URL
from unittests.mock_servers.servers import BadRefgetServerV2

bad_server_host = BAD_SERVER_V2_URL.split("://")[1].split(":")[0]
bad_server_port = BAD_SERVER_V2_URL.split("://")[1].split(":")[1].replace("/", "")

app = Flask(__name__)


server = BadRefgetServerV2()


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
    app.run(bad_server_host, port=bad_server_port)
