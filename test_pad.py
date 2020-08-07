from Crypto.Util.py3compat import bchr, bord

message = b"hello"


padding_len2 = 16-len(message)%16
print(padding_len2)
padding = bytearray()
for x in range(padding_len2):
    print(x)
    padding += bchr(x)
pad_data = message + padding
padding_len = bord(pad_data[-1])
print(pad_data)
print(padding_len)
print(pad_data[-padding_len:])


def generateForgedMsg ():
    cipherText = generateCipherText()
    lastBlock = cipherText[-16:]
    forgery = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    forgery = bytes(forgery, 'utf-8')
    forgedMsg = forgery + lastBlock
    print('Attack 3.1')
    print (b'Forgery: ' + forgery)
    print (b'Cipher Text: ' + cipherText)
    print (b'Last Block: ' + lastBlock)
    print (b'Forged message: ' + forgedMsg)
    return forgedMsg