import http.server
import socketserver
import os
import socket
import webbrowser
import sys

WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')


def start_mock_server(port):
    os.chdir(WEB_DIR)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at http://localhost:" + str(port), file=sys.stderr)
    webbrowser.open("http://localhost:" + str(port))
    httpd.serve_forever()
