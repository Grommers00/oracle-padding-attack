from Crypto.Util.py3compat import bchr, bord

def positionalByteForgery(forgery, count, position):
    info = [forgery[i] for i in range(0, len(forgery))]
    info[position] = 0 ^ count
    forgery = bytes(info)
    return forgery

def elementForgery(forgery, count):
    info = [forgery[i] for i in range(0, len(forgery))]
    info[count] = info[count] ^ 1
    return bytes(info)

def findXorByte(testByte, value):
    return testByte ^ value

def sequenceXor(forgery, intermediateValue, value): 
    info = [forgery[i] for i in range(0, len(forgery))] 
    counter = 1
    for i in intermediateValue: 
        info[14 - value + counter] = findXorByte(ord(i), counter) 
        counter += 1
    return bytes(info)
