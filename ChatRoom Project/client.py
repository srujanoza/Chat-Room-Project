import socket
import threading

# Choosing Name
name = input("Enter your Name: ")

if name == 'admin':
    password = input("Enter the passowrd for Admin: ") 

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

# Listening to Server and Sending Name
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive Message From Server
            # If 'CONNECT' Send Name
            message = client.recv(1024).decode('ascii')
            if message == 'CONNECT':
                client.send(name.encode('ascii'))
                next_msg = client.recv(1024).decode('ascii')
                if next_msg == 'PASSWORD':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('Connection not granted!! Wrong Password')
                        stop_thread = True

            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if stop_thread:
            break

        message = '{}: {}'.format(name, input(''))
        if message[len(name)+2 :].startswith('/'):
            if name == 'admin':
                if message[len(name)+2 :].startswith('/kick'):
                    client.send('KICK {}'.format(message[len(name)+2+6 :]).encode('ascii'))
            else:
                print("Commands can only be executed by the admin")
        else:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()