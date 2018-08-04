import http.server
import socketserver
import os

WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')


def start_mock_server(port=7878):
    os.chdir(WEB_DIR)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)
    httpd.serve_forever()
