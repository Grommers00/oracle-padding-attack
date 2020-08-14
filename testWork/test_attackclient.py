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
from enum import Enum

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

class padState(Enum):
    wrongPad = 1
    correctPad = 2
    lengthPad = 3
    exit = 4

padRes = padState.wrongPad


i = 0
padResponse = 0
count = 0
correctPadLength = -1
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
        if socks == server: # recieve message regardless of state
            message = socks.recv(2048) 
            padResponse = int.from_bytes(message, byteorder='big')
            if(padResponse and padRes == padState.wrongPad):
                padRes = padState.correctPad
            elif(not padResponse and padRes == padState.correctPad):
                padRes = padState.lengthPad
                correctPadLength = 17 - count
            waitingForResponse = False
            if(not padResponse):
                i += 1
        elif(not waitingForResponse and padRes == padState.wrongPad): #send message to figure out a correct padding
            waitingForResponse = True
            forgery = forgery[:-1] + bchr(forgeLastByte[-1] ^ i)
            forgedMsg = forgery + lastBlock
            print (b'Forgery: ' + forgery)
            print (b'Last Block: ' + lastBlock)
            print (b'Forged message: ' + forgedMsg)
            server.sendall(forgedMsg) 
            sys.stdout.flush() 
        elif(not waitingForResponse and padRes == padState.correctPad): #send message to figure out correct padding length
            print("We have correct padding and need to find correct padding length now")
            waitingForResponse = True
            #Modifying Forgery
            modifyForge = forgery.decode('utf-8')
            modify = list(modifyForge)
            modify[count] = chr(ord(modify[count]) + 1)
            modifyForge = bytes(''.join(modify), 'utf-8')
            print (b'Modified Forgery: ' + modifyForge)
            #Send new forged message
            forgedMsg = modifyForge + lastBlock
            count += 1
            server.sendall(forgedMsg) 
            sys.stdout.flush() 
        elif(padRes == padState.lengthPad):
            print("The correct padding length is " + str(correctPadLength))
            padRes = padState.exit
            #todo: gracefully exit for loop

server.close() 


#3.1 COMPLETED
#1. pick a few random words r1, . . . , rb and take i = 0
#2. pick r = r1 . . . rb−1(rb ⊕ i)
#3. if O(r|y) = 0 then increment i and go back to the previous step
#4. replace rb by rb ⊕ i
#5. for n = b down to 2 do
#(a) take r = r1 . . . rb−n(rb−n+1 ⊕ 1)rb−n+2 . . . rb
#(b) if O(r|y) = 0 then stop and output (rb−n+1 ⊕ n). . .(rb ⊕ n)
#6. output rb ⊕ 1 (We do not need to do this, we xor with value 0)

#3.2  - TO DO
#1. take rk = ak ⊕ (b − j + 2) for k = j, . . . , b
#2. pick r1, . . . , rj−1 at random and take i = 0
#3. take r = r1 . . . rj−2(rj−1 ⊕ i)rj . . . rb
#4. if O(r|y) = 0 then increment i and go back to the previous step
#5. output rj−1 ⊕ i ⊕ (b − j + 2)