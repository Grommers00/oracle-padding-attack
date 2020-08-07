import socket 
import select 
import sys 
import time
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string
import time

def generateCipherText() :
    realMsg = b'HelloWorld!aaaa'
    key = b'1234567891234567'
    iv = b'0123456789012345'
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    cipherText = cipher.encrypt(btnPad(realMsg, AES.block_size, 'btn710'))
    print('Generating Cipher Text')
    print (b'Real message: ' + realMsg)
    print (b'Padded message: ' + btnPad(realMsg, AES.block_size, 'btn710'))
    print (b'Encrypted message: ' + cipherText)
    return cipherText
    
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

cipherText = generateCipherText()
lastBlock = cipherText[-16:]
forgery = b'0000000000000000'
forgeLastByte = bytes(forgery[-1])
forgedMsg = forgery + lastBlock
print('Attack 3.1')
print (b'Forgery: ' + forgery)
print (b'Cipher Text: ' + cipherText)
print (b'Last Block: ' + lastBlock)

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
            waitingForResponse = True
            forgery = forgery[:-1] + bchr(forgeLastByte[-1] ^ i)
            forgedMsg = forgery + lastBlock
            print (b'Forgery: ' + forgery)
            print (b'Last Block: ' + lastBlock)
            print (b'Forged message: ' + forgedMsg)
            server.sendall(forgedMsg) 
            sys.stdout.flush() 
        elif(padResponse):
            print("The padding is correct now")
            count = 0
            waitingForResponse = False
            while(padResponse): # once padding is broken exit
                print('do i keep going?')
                if socks == server: 
                    message = socks.recv(2048) 
                    padResponse = int.from_bytes(message, byteorder='big')
                    print(padResponse)
                    waitingForResponse = False
                elif(not waitingForResponse and padResponse): # there is no response waiting and padresponse is still true
                    waitingForResponse = True
                    modifyForge = forgery.decode('utf-8')
                    modify = list(modifyForge)
                    modify[count] = chr(ord(modify[count]) + 1)
                    modifyForge = bytes(''.join(modify), 'utf-8')
                    forgedMsg = modifyForge + lastBlock
                    print (b'Forgery: ' + modifyForge)
                    server.sendall(forgedMsg) 
                    sys.stdout.flush() 
            print("The padding is now wrong again")
            time.sleep(1000)
            #while loop send messages agin to the server, changing the byte from beginning to end one at a time
            #stop when we get server message 0
server.close() 

#1. pick a few random words r1, . . . , rb and take i = 0
#2. pick r = r1 . . . rb−1(rb ⊕ i)
#3. if O(r|y) = 0 then increment i and go back to the previous step
#4. replace rb by rb ⊕ i
#5. for n = b down to 2 do
#(a) take r = r1 . . . rb−n(rb−n+1 ⊕ 1)rb−n+2 . . . rb
#(b) if O(r|y) = 0 then stop and output (rb−n+1 ⊕ n). . .(rb ⊕ n)
#6. output rb ⊕ 1 (We do not need to do this, we xor with value 0)