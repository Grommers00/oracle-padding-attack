import socket 
import select 
import sys 
from Crypto.Cipher import AES
from Crypto.Util import Counter

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number")
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 
nonce = b'abcd'
ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
key = b'1234567891234567'
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

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
			message.decode("utf8")
			print(message)
		else: 
			message = sys.stdin.readline() 
			plaintext = bytes(message, 'utf-8')
			ciphertext = cipher.encrypt(plaintext)
			server.sendall(ciphertext) 
			sys.stdout.write("<You>") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 
