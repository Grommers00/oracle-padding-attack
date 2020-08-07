import socket 
import select 
import sys 
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord



def btnPad(data_to_pad, block_size, style):
	padding_len = block_size-len(data_to_pad)%block_size
	padding = bytearray()
	if style == 'btn710':
		for x in range(padding_len):
			padding += bchr(x)
	else:
		raise ValueError("Unknown padding style")
	return data_to_pad + padding


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number")
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
key = b'1234567891234567'
iv = b'0123456789012345'
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048) 
			msg = int.from_bytes(message, byteorder='big')
			print(msg)
			print(message)
		else: 
			message = sys.stdin.readline() 
			plaintext = bytes(message, 'utf-8')
			ciphertext = cipher.encrypt(btnPad(plaintext,AES.block_size,'btn710'))
			server.sendall(ciphertext) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 

