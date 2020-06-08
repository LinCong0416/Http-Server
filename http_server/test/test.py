import time
import socket
import threading
from server.socket_server import TCPServer
from server.base_http_server import BaseHttPServer
from handler.base_handler import StreamRequestHandler
from handler.base_http_handler import BaseHTTPRequestHandler

class TestBaseRequestHandler(StreamRequestHandler):
    def handle(self):
        msg = self.readline()
        print('Server recv msg: ' + msg)
        time.sleep(1)
        self.write_content(msg)
        self.send()
        pass

class SocketServerTest:
    def run_server(self):
        tcp_server = TCPServer(('127.0.0.1', 8888), TestBaseRequestHandler)
        tcp_server.serve_forever()

    def client_connect(self):
        client = socket.socket()
        client.connect(('127.0.0.1', 8888))
        client.send(b'Hello TCPServer\r\n')
        msg = client.recv(1024)
        print('Client recv msg: ' + msg.decode())

    def gen_clients(self, num):
        clients = []
        for i in range(num):
            client_thread = threading.Thread(target=self.client_connect)
            clients.append(client_thread)
        return clients

    def run(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        clients = self.gen_clients(1)
        for client in clients:
            client.start()

        server_thread.join()
        for client in clients:
            client.join()

class BaseHTTPRequestHandlerTest:
    def run_server(self):
        BaseHttPServer(('127.0.0.1', 9999), BaseHTTPRequestHandler).server_forever()

    def run(self):
        self.run_server()

if __name__ == '__main__':
    #SocketServerTest().run()
    BaseHTTPRequestHandlerTest().run()