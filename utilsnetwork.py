#https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a
import socket

_port = 8080
class Endpoint:
    def __init__(self, is_server: bool) -> None:
        self.is_server = is_server    
    def server():
        host = socket.gethostname()   # get local machine name
        port = _port  # Make sure it's within the > 1024 $$ <65535 range
        
        s = socket.socket()
        s.bind((host, port))
        
        s.listen(1)
        c, addr = s.accept()
        print("Connection from: " + str(addr))
        while True:
            data = c.recv(1024).decode('utf-8')
            if not data:
                break
            print('From online user: ' + data)
            data = data.upper()
            c.send(data.encode('utf-8'))
        c.close()

if __name__ == '__main__':
    server()