import socket

def client():
    #1.create socket
    s = socket.socket()
    #2.connect
    HOST = '127.0.0.1'
    PORT = 6666
    s.connect((HOST,PORT))
    # 3.work
    s.send(b'Hello World!')
    msg = s.recv(1024)
    print('From server:%s' %msg)

if __name__ == '__main__':
    client()
