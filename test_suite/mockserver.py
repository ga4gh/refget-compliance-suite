from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
import re
import cgi
import socket
from threading import Thread

from utils import get_seq_obj


DATA = []
CIRCULAR_CHROMOSOME_SUPPORT = True


class MockServerRequestHandler(BaseHTTPRequestHandler):
    SEQUENCE_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/?$')
    METADATA_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/metadata/?$')
    RANGE_HEADER_PATTERN = re.compile(r'bytes=[0-9]*-[0-9]*$')

    def handle_subsequence_query_range(self, seq_obj):
        if not self.RANGE_HEADER_PATTERN.match(self.headers['Range']):
            self.send(400)
            return
        fbs = int(self.headers['Range'].split('=')[1].split('-')[0])
        lbs = int(self.headers['Range'].split('=')[1].split('-')[1])
        if lbs >= seq_obj.size:
            lbs = seq_obj.size - 1
        if fbs >= seq_obj.size:
            self.send(400)
            return
        if fbs > lbs:
            self.send(400)
            return
        if fbs == 0 and lbs == seq_obj.size - 1:
            self.send(200, bytes(seq_obj.sequence, "utf-8"))
            return
        self.send(206, bytes(seq_obj.sequence[fbs:lbs+1], "utf-8"))
        return

    def handle_subsequence_query_start_end(self, seq_obj, args):
        if 'start' in args and 'end' in args and len(args) == 2:
            start = args['start'][0]
            end = args['end'][0]
            if not start.isdigit() or not end.isdigit():
                self.send(400)
                return
            start = int(start)
            end = int(end)
            if start >= seq_obj.size or end > seq_obj.size:
                self.send(416)
                return
            if start > end:
                if CIRCULAR_CHROMOSOME_SUPPORT is not True:
                    print('woohoo')
                    self.send(501)
                    return
                else:
                    if seq_obj.is_circular == 0:
                        self.send(416)
                        return
                    else:
                        text = seq_obj.sequence[start:seq_obj.size] + \
                            seq_obj.sequence[0:end]
                        self.send(200, bytes(text, "utf-8"), {})
            elif start < end:
                text = seq_obj.sequence[start:end]
                self.send(200, bytes(text, "utf-8"), {"Accept-Ranges": "none"})
            else:
                self.send(200, bytes('', "utf-8"), {"Accept-Ranges": "none"})
        if 'start' in args and len(args) == 1:
            start = args['start'][0]
            if not start.isdigit():
                self.send(400)
                return
            start = int(start)
            if start >= seq_obj.size:
                self.send(400)
                return
            text = seq_obj.sequence[start:]
            self.send(200, bytes(text, "utf-8"), {"Accept-Ranges": "none"})
            return

        if 'end' in args and len(args) == 1:
            end = args['end'][0]
            if not end.isdigit():
                self.send(400)
                return
            end = int(end)
            if end > seq_obj.size:
                self.send(400)
                return
            text = seq_obj.sequence[:end]
            self.send(200, bytes(text, "utf-8"), {"Accept-Ranges": "none"})
            return

    def get_seq_obj(self):
        seq_id = self.path.split('/')[2].split('?')[0]
        for seq in DATA:
            if seq.md5 == seq_id or seq.sha512 == seq_id:
                return seq
        return None

    def get_args(self):
        args = {}
        idx = self.path.find('?')
        if idx >= 0:
            args = cgi.parse_qs(self.path[idx+1:])
        return args

    def send(self, status_code, content=bytes('', "utf-8"), headers={}):
        self.send_response(status_code)
        for key in headers:
            self.send_header(key, headers[key])
        if status_code is 200 or status_code is 206:
            self.send_header('Content-Length', len(content))
            content_type = 'text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii'
            self.send_header(
                'Content-Type', content_type
            )
        self.end_headers()
        self.wfile.write(content)
        return

    def do_GET(self):
        if self.SEQUENCE_PATTERN.match((self.path).split('?')[0]):
            print(CIRCULAR_CHROMOSOME_SUPPORT)
            args = self.get_args()
            SUPPORTED_ENCODINGS = ['*/*', 'text/vnd.ga4gh.seq.v1.0.0+plain']
            seq_obj = self.get_seq_obj()
            if seq_obj is None:
                self.send(404)
                return

            if self.headers['Accept'] not in SUPPORTED_ENCODINGS:
                self.send(415)
                return

            if 'Range' not in self.headers and args == {}:
                self.send(200, bytes(seq_obj.sequence, "utf-8"))
                return

            if 'Range' in self.headers and args != {}:
                self.send(400)
                return

            if args != {}:
                self.handle_subsequence_query_start_end(seq_obj, args)
                return

            if 'Range' in self.headers:
                self.handle_subsequence_query_range(seq_obj)
                return

            else:
                self.send(404, bytes('ATGC', "utf-8"))
                return

        elif self.SEQUENCE_PATTERN.match(self.path):
            print('metdata')

        else:
            print(self.path)
            self.send_response(404)


def set_data():
    DATA.append(get_seq_obj("I"))
    DATA.append(get_seq_obj("VI"))
    DATA.append(get_seq_obj("NC"))
    return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, circular_support, daemon=True):
    global CIRCULAR_CHROMOSOME_SUPPORT
    CIRCULAR_CHROMOSOME_SUPPORT = circular_support
    set_data()
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(daemon)
    mock_server_thread.start()
    return mock_server


if __name__ == '__main__':
    start_mock_server(5000, False, False)
