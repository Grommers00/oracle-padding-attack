from Crypto.Util.py3compat import bchr, bord

def generateForgedMsg (cipherText):
    lastBlock = cipherText[-16:]
    forgery = b'0000000000000000'
    forgedMsg = forgery + lastBlock
    forgedLastByte = bytes(forgery[-1])
    print (b'Forgery: ' + forgery)
    #print (b'Cipher Text: ' + cipherText)
    #print (b'Last Block: ' + lastBlock)
    #print (b'Forged message: ' + forgedMsg)
    return forgedMsg, forgery, forgedLastByte, lastBlock

def lastByteForgery(forgery, forgedLastByte, lastBlock, count):
    forgery = forgery[:-1] + bchr(forgedLastByte[-1] ^ count)
    forgedMsg = forgery + lastBlock
    print (b'Forgery: ' + forgery)
    #print (b'Last Block: ' + lastBlock)
    #print (b'Forged message: ' + forgedMsg)
    return forgedMsg, forgery

def elementForgery(forgery, lastBlock, count):
    modifyForge = forgery.decode('utf-8')
    modify = list(modifyForge)
    modify[count] = chr(ord(modify[count]) + 1)
    modifyForge = bytes(''.join(modify), 'utf-8')
    print (b'Modified Forgery: ' + modifyForge)
    forgedMsg = modifyForge + lastBlock
    return forgedMsg

def findXorByte(testByte, value):
    count = 0
    byte = int(testByte)
    while( byte ^ count != value):
        count += 1
    return count

def secLastByteForgery(forgery, forgedLastByte, lastBlock, count, tempLastIV):
    forgery = forgery[:-2] + bchr(forgedLastByte[-1] ^ count) + bytes(tempLastIV,'utf-8')
    forgedMsg = forgery + lastBlock
    print (b'Forgery: ' + forgery)
    #print (b'Last Block: ' + lastBlock)
    #print (b'Forged message: ' + forgedMsg)
    return forgedMsg, forgery