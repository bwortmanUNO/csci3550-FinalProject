import socket
import select
import sys
import errno

HEADER = 10
HOST = 'localhost'
PORT = 9876

my_username = input("Username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))
client.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER}}".encode("utf-8")
client.send(username_header + username)

while True:
    message = ""

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER}}".encode("utf-8")
        client.send(message_header+message)
    try:
        while True:
            username_header = client.recv(HEADER)

            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8"))
            username = client.recv(username_length).decode("utf-8")

            message_header = client.recv(HEADER)
            message_length = int(message_header.decode("utf-8"))
            message = client.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('Error:', str(e))
        sys.exit()
