import select
import socket

clients = dict()
# client: {"addr": "127.0.0.1", "name": "Anton"}
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 9898))
server.listen(5)
print('PUM Chat: Server started')

def broadcast(msg, sock):
    author = "PUM Chat" if sock is server else clients[sock]['name']
    msg = author + ': ' + msg
    for s in clients.keys():
        s.send(bytes(msg.encode()))
    print(msg.strip())


while True:
    inputs, _, _ = select.select(list(clients.keys()) + [server], [], [])
    for sock in inputs:
        if sock is server:
            conn, addr = server.accept()
            clients[conn] = dict(addr=addr, name=None)
            conn.send("Welcome to PUM Chat! Enter your name:\n")
        else:
            msg = sock.recv(1024)
            if not msg:
                sock.close()
                name = clients[sock]["name"]
                clients.pop(sock)
                if name:
                    broadcast("{} left PUM Chat\n".format(name), server)
            else:
                msg = msg.decode('utf-8')
                if not clients[sock]['name']:
                    clients[sock]['name'] = msg.strip()
                    sock.send(bytes('Hi, {}, now you can write to chat!\n'.format(clients[sock]['name']).encode()))
                    broadcast("{} joined PUM Chat\n".format(clients[sock]['name']), server)
                else:
                    broadcast(msg, sock)
