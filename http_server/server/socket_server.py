import socket
import threading
class TCPServer:
    def __init__(self,server_address,handler_class):
        self.server_address = server_address
        self.HandlerClass = handler_class
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.is_shutdown = False

    #start
    def server_forever(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while not self.is_shutdown:
            request, client_address = self.get_request()
            try:
                #self.process_request(request, client_address)
                self.process_request_multithread(request, client_address)
            except Exception as e:
                print(e)

        pass

    def process_request_multithread(self, request, client_address):
        t = threading.Thread(target=self.process_request,
                             args=(request, client_address))
        t.start()

    #accept
    def get_request(self):
        return self.socket.accept()

    #process
    def process_request(self,request,client_address):
        handler = self.HandlerClass(self,request,client_address)
        handler.handle()
        self.close_request(request)

    #close
    def close_request(self,request):
        request.shutdown(socket.SHUT_WR)
        request.close()

    #shut down server
    def shotdown(self):
        self.is_shutdown = True

