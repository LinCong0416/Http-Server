import socket
def server():
    #1.creat socket
    s = socket.socket()
    #2.bind
    HOST = '127.0.0.1'
    PORT = 6666
    s.bind((HOST,PORT))
    #3.listen
    s.listen(5)
    #4.work
    while True:
        c,addr = s.accept()
        print('Connected Client:',addr)
        msg = c.recv(1024)
        c.send(msg)
    pass

if __name__ == '__main__':
    server()