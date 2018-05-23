from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import cgi
import socket
from threading import Thread

from utils import get_seq_obj


DATA = []


class MockServerRequestHandler(BaseHTTPRequestHandler):
    URL = 'http://localhost:5000/'
    SEQUENCE_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/?$')
    METADATA_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/metadata/?$')

    def get_args(self):
        args = {}
        idx = self.path.find('?')
        if idx >= 0:
            args = cgi.parse_qs(self.path[idx+1:])
        return args

    def send(self, status_code, content, headers={}):
        self.send_response(status_code)
        for key in headers:
            self.send_header(key, headers[key])
        self.send_header(
            'Content-Type', 'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
        )
        self.end_headers()
        self.wfile.write(content)
        return

    def do_GET(self):
        if self.SEQUENCE_PATTERN.match((self.path).split('?')[0]):
            SUPPORTED_ENCODINGS = ['*/*', 'text/vnd.ga4gh.seq.v1.0.0+plain']

            args = self.get_args()
            self.send(200, bytes('ATGC', "utf-8"))

            return

        elif self.SEQUENCE_PATTERN.match(self.path):
            print('metdata')

        else:
            self.send_response(404)


def set_data():
    DATA.append(get_seq_obj("I"))
    DATA.append(get_seq_obj("VI"))
    DATA.append(get_seq_obj("NC"))
    print(DATA[2].sequence)
    return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, daemon=True):
    set_data()
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(daemon)
    mock_server_thread.start()
    return mock_server


if __name__ == '__main__':
    start_mock_server(5000, False)
