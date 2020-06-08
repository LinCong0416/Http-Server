import json

from handler.base_http_handler import BaseHTTPRequestHandler
from urllib import parse
import os

RESOURCES_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)), '../resources')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, server, request, client_address):
        BaseHTTPRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        found, resource_path = self.get_resources(self.path)
        if not found:
            self.write_error(404)
            self.send()
        else:
            with open(resource_path, 'rb') as f:
                fs = os.fstat(f.fileno())
                # length of the file
                clength = str(fs[6])
                self.write_response(200)
                self.write_header('Content-Length', clength)
                self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                                  (self.server.server_address[0], self.server.server_address[1]))
                self.end_headers()
                while True:
                    buf = f.read(1024)
                    if not buf:
                        break
                    self.write_content(buf)
                # self.send()

    def do_POST(self):
        body = json.loads(self.body)
        print(body)
        username = body['username']
        password = body['password']
        if username == 'dongdongqiang' and password == '123456':
            response = {'message': 'success', 'code': 0}
        else:
            response = {'message': 'failed', 'code': -1}
        response = json.dumps(response)
        self.write_response(200)
        self.write_header('Content-Length', len(response))
        self.write_header('Access-Control-Allow-Origin', 'http://%s:%d' %
                          (self.server.server_address[0], self.server.server_address[1]))
        self.end_headers()
        self.write_content(response)

    def get_resource(self, path):
        url_result = parse.urlparse(path)
        resource_path = str(url_result[2])
        if resource_path.startswith('/'):
            resource_path = resource_path[1:]
        resource_path = os.path.join(RESOURCES_PATH, resource_path)
        if os.path.exists(resource_path) and os.path.isfile(resource_path):
            return True, resource_path
        else:
            return False, resource_path
