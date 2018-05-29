from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import cgi
import socket
from threading import Thread

from utils import get_seq_obj


DATA = []
CIRCULAR_CHROMOSOME_SUPPORT = True


class MockServerRequestHandler(BaseHTTPRequestHandler):
    '''MockServerRequestHandler class extends BaseHTTPRequestHandler class.
    It contains all the required functions and methods to handle requests.
    '''

    '''Regex patterns for sequence api and metadata api. These regex pattern
    will be used in do_GET method to determine which API is being called.
    '''
    SEQUENCE_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/?$')
    METADATA_PATTERN = re.compile(r'/sequence/[a-z0-9A-Z]*/metadata/?$')

    '''This is the regex pattern for Range header. It is used to check if the
    value passed in the Range header is valid.
    Eg of invalid values:  units=9-10, bytes==1-20, bytes=-1-8
    Eg of valid values: bytes=1-10
    '''
    RANGE_HEADER_PATTERN = re.compile(r'bytes=[0-9]*-[0-9]*$')

    def handle_subsequence_query_range(self, seq_obj):
        '''handle_subsequence_query_range contains all the logic to handle a
        valid GET sub-sequence by ID using Range header API call. First it
        discards invalid values using regex. Then it checks different edge
        cases before sending the response. This function is called from do_GET
        method.
        '''

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
            self.send(416)
            return
        if fbs == 0 and lbs == seq_obj.size - 1:
            self.send(200, seq_obj.sequence.encode("ascii"))
            return
        self.send(206, seq_obj.sequence[fbs:lbs+1].encode("ascii"))
        return

    def handle_subsequence_query_start_end(self, seq_obj, args):
        '''handle_subsequence_query_start_end contains all the logic to handle a
        valid GET sub-sequence by ID using start end parameters API call. It
        checks different edge cases and valid inputs before sending the
        response. This function is called from do_GET method. It also considers
        the possibility of having only one (start or end) parameter.
        '''

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
                    self.send(501)
                    return
                else:
                    if seq_obj.is_circular == 0:
                        self.send(416)
                        return
                    else:
                        text = seq_obj.sequence[start:seq_obj.size] + \
                            seq_obj.sequence[0:end]
                        self.send(200, text.encode("ascii"), {})
            elif start < end:
                text = seq_obj.sequence[start:end]
                self.send(200, text.encode("ascii"), {"Accept-Ranges": "none"})
            else:
                self.send(200, "".encode("ascii"), {"Accept-Ranges": "none"})
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
            self.send(200, text.encode("ascii"), {"Accept-Ranges": "none"})
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
            self.send(200, text.encode("ascii"), {"Accept-Ranges": "none"})
            return

    def get_seq_obj(self):
        '''
        get_seq_obj is used to get the sequence object based on the checksum
        identifier passed in the URL. This function is called from do_GET
        '''

        seq_id = self.path.split('/')[2].split('?')[0]
        for seq in DATA:
            if seq.md5 == seq_id or seq.sha512 == seq_id:
                return seq
        return None

    def get_args(self):
        '''
        get_args is used to get the query parameters passed in the URL.
        This function is called from do_GET.
        '''

        args = {}
        idx = self.path.find('?')
        if idx >= 0:
            args = cgi.parse_qs(self.path[idx+1:])
        return args

    def send(self, status_code, content="".encode("ascii"), headers={}):
        '''send is a custom response function to remove repetitive code from
        the mock server. It takes three parameters as input i.e. status_code,
        content and  headers. This function is called from various functions
        such as do_GET, handle_subsequence_query_range and
        handle_subsequence_query_start_end
        '''

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

    def get_metadata(self, seq, checksum):
        '''get_metadata returns the metadata of a sequence in json format to be
        sent on a metadata API call. This function is called from do_GET
        '''

        response = {
            "metadata": {
                "id": checksum,
                "length": seq.size,
                "alias": []
            }
        }
        response["metadata"]["alias"].append({"alias": seq.md5})
        response["metadata"]["alias"].append({"alias": seq.sha512})
        return json.dumps(response)

    def do_GET(self):
        '''do_GET is the first function which gets called on a GET request. It
        then checks using regex patterns defined above whether its a sequence
        API call or Metdata API call. If its none then responds with a 404
        error.
        If its a sequence API:
            It first checks the checksum identifier to get the sequence object
            then 'Accept' header to check if its in SUPPORTED_ENCODINGS, then
            subsquently checks Range and start - end parameters for proper
            response
        If its a metadata API:
            It first checks the checksum identifier to get the sequence object
            then 'Accept' header to check if its in SUPPORTED_ENCODINGS. Note
            it doesn't call the send function on a successful response.
        '''

        if self.SEQUENCE_PATTERN.match((self.path).split('?')[0]):
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
                self.send(200, seq_obj.sequence.encode("ascii"))
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
                self.send(404, "ATGC".encode("ascii"))
                return

        elif self.METADATA_PATTERN.match(self.path):
            SUPPORTED_ENCODINGS = ['*/*', 'text/vnd.ga4gh.seq.v1.0.0+json']
            seq_obj = self.get_seq_obj()
            if seq_obj is None:
                self.send(404)
                return

            if self.headers['Accept'] not in SUPPORTED_ENCODINGS:
                self.send(415)
                return

            seq_id = self.path.split('/')[2].split('?')[0]
            metadata = self.get_metadata(seq_obj, seq_id)
            self.send_response(200)
            content_type = 'text/vnd.ga4gh.seq.v1.0.0+json'
            self.send_header(
                'Content-Type', content_type
            )
            self.end_headers()
            self.wfile.write(metadata.encode("ascii"))
            return

        else:
            print(self.path)
            self.send_response(404)


def set_data():
    '''set_data sets the global variable DATA which contains all the test
    sequence data. It uses get_seq_obj from utils.py
    '''

    DATA.append(get_seq_obj("I"))
    DATA.append(get_seq_obj("VI"))
    DATA.append(get_seq_obj("NC"))
    return


def get_free_port():
    ''' get_free_port function is used in conftest and the return of this
    is a free port available in the system on which the mock server will be
    run. This port will be passed to start_mock_server as a required parameter
    from conftest.py
    '''

    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port, circular_support, daemon=True):
    ''' start_mock_server used by test suite's conftest.py file to run the server
    on the fly. It gets circular_support (a boolean variable) from conftest.py
    to set the global variable CIRCULAR_CHROMOSOME_SUPPORT in the server.
    set_data is called to load all the test seqeunce data in a global variable
    DATA. daemon should be true so that server automatically closes after
    running all the tests.
    '''

    global CIRCULAR_CHROMOSOME_SUPPORT
    CIRCULAR_CHROMOSOME_SUPPORT = circular_support
    set_data()
    mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(daemon)
    mock_server_thread.start()
    return mock_server


if __name__ == '__main__':
    start_mock_server(5000, True, False)
