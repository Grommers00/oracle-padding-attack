# Python program to implement server side of chat room.
import socket
import select
import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.py3compat import bchr, bord
from threading import *
import _thread


def btnUnpad(padded_data, block_size, style):
    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError
    if style in ('btn710'):
        padding_len = bord(padded_data[-1]) + 1
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError
        padding = bytearray()
        for x in range(padding_len):
            padding += bchr(x)
        if padding_len>1 and padded_data[-padding_len:]!=padding:
            raise ValueError
    else:
        raise ValueError
    print (b'Unpadded Message: ' + padded_data[:-padding_len])
    return 1


"""The first argument AF_INET is the ad
dress domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(10)

list_of_clients = []

key = b'1234567891234567'
iv = b'0123456789012345'
cipher = AES.new(key, AES.MODE_CBC, iv=iv)


def clientthread(conn, addr):
    # sends a message to the client whose user object is conn

    while True:
        try:
            ciphertext = conn.recv(2048)
            if ciphertext:
                try:
                    message_to_send = bchr(btnUnpad(cipher.decrypt(ciphertext), 16, 'btn710'))
                except: 
                    message_to_send = bchr(0)                    
                finally:
                    print(addr[0], message_to_send)
                    broadcast(message_to_send, conn)
            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(conn)
        except:
            continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """


def broadcast(message, connection):
    for clients in list_of_clients:
        try:
            print('Broadcasting Messages')
            clients.send(message)
        except:
            clients.close()
            # if the link is broken, we remove the client
            remove(clients)


"""The following function simply removes the object
from the list that was created at the beginning of
the program"""


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:

    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()

    """Maintains a list of clients for ease of broadcasting 
	a message to all available people in the chatroom"""
    list_of_clients.append(conn)

    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    _thread.start_new_thread(clientthread, (conn, addr))

conn.close()
server.close()
