from Crypto.Util.py3compat import bchr, bord

def generateForgedMsg (cipherText):
    lastBlock = cipherText[-16:]
    forgery = b'0000000000000000' #0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 #RANDOM WORDS    
    forgedMsg = forgery + lastBlock #0000000000 + $&!($^^00x01x00x3
    forgedLastByte = bytes(forgery[-1]) #x00           
    #print (b'Forgery: ' + forgery)  #0000000000
    #print (b'Cipher Text: ' + cipherText)
    #print (b'Last Block: ' + lastBlock)
    #print (b'Forged message: ' + forgedMsg)
    return forgedMsg, forgery, forgedLastByte, lastBlock       ##0000000000 + $&!($^^00x01x00x3, 00000000000000, x00, #jordanx00x01x002

def lastByteForgery(forgery, forgedLastByte, lastBlock, count):
    forgery = forgery[:-1] + bchr(forgedLastByte[-1] ^ count) #00000000000000 + 0^ (etc) # Goes until final IV letter, is correct padding) #step number 2
    forgedMsg = forgery + lastBlock # 00000000000000+(0^x10) + jordanx00x01x002x03
    #print (b'Forgery: ' + forgery) #
    #print (b'Last Block: ' + lastBlock)
    #print (b'Forged message: ' + forgedMsg)
    return forgedMsg, forgery      # 00000000000000+(0^x10) + jordanx00x01x002x03 , #00000000000000+(0^x10)

def elementForgery(forgedMsg, count):
    info = [forgedMsg[i] for i in range(0, len(forgedMsg))]
    info[count] = info[count] ^ 1
    forgedMsg = bytes(info)
    return forgedMsg

def findXorByte(testByte, value):
    return testByte ^ value  #should return an int

def secLastByteForgery(forgery, forgedLastByte, lastBlock, count, tempLastIV):
    forgery = forgery[:-2] + bchr(forgedLastByte[-1] ^ count) + bytes(tempLastIV,'utf-8')
    forgedMsg = forgery + lastBlock
    #print (b'Forgery: ' + forgery)
    return forgedMsg, forgery

def sequenceXor(forgery, intermediateValue, value): 
    info = [forgery[i] for i in range(0, len(forgery))] 
    #for loop, from positions j to b or to position to 15
    counter = 1
    for i in intermediateValue: #if value s equal to 3
        info[14 - value + counter] = findXorByte(ord(i), counter) 
        counter += 1
    return bytes(info)

def positionalByteForgery(forgery, count, position):
    info = [forgery[i] for i in range(0, len(forgery))] # switches forgery to byte mode
    info[position] = 0 ^ count # a position is passed and we change the byte "0" because our initial forgedMsg = '00000000' is xor'd to count
    forgery = bytes(info) # this puts together back forgery 
    #print (b'pBF - Forgery: ' + forgery)
    return forgery
