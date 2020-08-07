import socket 
import select 
import sys 
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string

def generateCipherText() :
    realMsg = b'HelloWorld!'
    nonce = b'abcd'
    ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
    key = b'1234567891234567'
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    cipherText = cipher.encrypt(btnPad(realMsg, 16, 'btn710'))
    print('Generating Cipher Text')
    print (b'Real message: ' + realMsg)
    print (b'Padded message: ' + btnPad(realMsg, 16, 'btn710'))
    print (b'Encrypted message: ' + cipherText)
    return cipherText

def generateForgedMsg ():
    cipherText = generateCipherText()
    lastBlock = cipherText[-16:]
    forgery = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    forgery = bytes(forgery, 'utf-8')
    forgedMsg = forgery + cipherText
    print('Attack 3.1')
    print (b'Forgery: ' + forgery)
    print (b'Cipher Text: ' + cipherText)
    print (b'Last Block: ' + lastBlock)
    print (b'Forged message: ' + forgedMsg)
    return forgedMsg
    
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

i = 0
padResponse = 0
forgedMsg = generateForgedMsg()
waitingForResponse = False
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
            padResponse = int.from_bytes(message, byteorder='big')
            print(padResponse)
            waitingForResponse = False
            if(not padResponse):
                i += 1
        elif(not waitingForResponse and not padResponse):
            forgedMsg = forgedMsg[15] + bchr(forgedMsg[-1] ^ i)
            waitingForResponse = True
            print(forgedMsg)
            server.sendall(forgedMsg) 
            sys.stdout.flush() 
server.close() 

#1. pick a few random words r1, . . . , rb and take i = 0
#2. pick r = r1 . . . rb−1(rb ⊕ i)
#3. if O(r|y) = 0 then increment i and go back to the previous step
#4. replace rb by rb ⊕ i
#5. for n = b down to 2 do
#(a) take r = r1 . . . rb−n(rb−n+1 ⊕ 1)rb−n+2 . . . rb
#(b) if O(r|y) = 0 then stop and output (rb−n+1 ⊕ n). . .(rb ⊕ n)
#6. output rb ⊕ 1