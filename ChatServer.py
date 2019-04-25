import socket
import select

HEADER = 10
HOST = 'localhost'
PORT = 9876

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen()

socket_list = [server]
client_list = {}


def recv_msg(client_socket):
    try:
        header = client_socket.recv(HEADER)

        if not len(header):
            return False

        msg_length = int(header.decode("utf-8"))

        return {"header": header, "data": client_socket.recv(msg_length)}
    except:
        return False


while True:
    read_sockets, write, exception_sockets = select.select(socket_list, [], socket_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client_socket, client_address = server.accept()

            user = recv_msg(client_socket)

            if user is False:
                continue

            socket_list.append(client_socket)

            client_list[client_socket] = user

            print("New connection from", client_address[0], ":", client_address[1], "Username:",
                  user['data'].decode("utf-8"))
        else:
            message = recv_msg(notified_socket)

            if message is False:
                print("Closed connection from", client_list[notified_socket]['data'].decode("utf-8"))
                socket_list.remove(notified_socket)
                del client_list[notified_socket]
                continue
            user = client_list[notified_socket]
            print("Received message from", user['data'].decode("utf-8"))

            for client_socket in client_list:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del client_list[notified_socket]
