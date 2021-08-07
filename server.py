import socket, threading, random

class main_server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = random.randint(10000, 65535)
        self.modname = "SERVER"
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.client_list = []
        self.users_list = []
        print(f"host: {self.host}\nport: {self.port}")
    def acception(self):
        while True:
            client, add = self.server.accept()
            self.client_list.append(client)
            get_user = client.recv(1024).decode("utf-8")
            if get_user in self.users_list:
                used = True
                while used == True:
                    client.send(f"[{self.modname}]: {get_user} is used please enter a new user".encode('utf-8'))
                    get_user = client.recv(1024).decode("utf-8")
                    if get_user not in self.users_list:
                        used = False
            new_user = get_user
            self.users_list.append(new_user)
            print(f"connection from {add} connection user {new_user}")
            for clients in self.client_list:
                clients.send((f"{new_user}'s joined the server").encode('utf-8'))
            threading.Thread(target=main_server.cast, args=[self, client, new_user]).start()
    def cast(self, client, new_user):
        auther = new_user
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if f"{message}" == "lsm":
                    threading.Thread(target=main_server.list_members, args=[self, client]).start()
                else:
                    threading.Thread(target=main_server.to_all_clients, args=[self, auther, message]).start()
            except:
                threading.Thread(target=main_server.left, args=[self, client, auther]).start()
                client.close()
                break
    def to_all_clients(self, auther, message):
        for clients in self.client_list:
            clients.send(f"[{auther}]: {message}".encode('utf-8'))
    def left(self, client, auther):
        self.client_list.remove(client)
        self.users_list.remove(auther)
        for clients in self.client_list:
            clients.send((f"[{self.modname}]: {auther}'s left server").encode('utf-8'))
        print(f"Disconnected client: {client} | auth: {auther}")
    def list_members(self, client):
        for users in self.users_list:
            client.send(f"[{self.modname}]: {users}'s online\n".encode('utf-8'))

if __name__ == "__main__":
    ai = main_server()
    ai.acception()