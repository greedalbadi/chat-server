import socket, threading, os
class main_client:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_client.clear(self)
        self.user = input('user: ')
        main_client.clear(self)
        self.breaked = None
        self.host = input('host: ')
        self.port = int(input('port: '))
        self.server.connect((self.host, self.port))
        self.server.send(self.user.encode('utf-8'))
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    def get(self):
        while True:
            message = self.server.recv(1024).decode("utf-8")
            if len(message) == 0:
                self.breaked = True
                break
            else:
                print(message)
    def sends(self):
        while True:
            self.server.send(f"{input('')}".encode('utf-8'))
            if self.breaked == True:
                break
if __name__ == "__main__":
    am = main_client()
    threading.Thread(target=am.get).start()
    threading.Thread(target=am.sends).start()