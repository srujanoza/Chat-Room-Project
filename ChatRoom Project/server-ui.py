import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Names
clients = []
names = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)                
        except:
            # Removing And Closing Clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast('{} left!'.format(name).encode('ascii'))
                names.remove(name)
                break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Name
        client.send('CONNECT'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        # Print And Broadcast Name
        print("Name is {}".format(name))
        broadcast("{} joined!\n".format(name).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is  listening")
receive()