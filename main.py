from btn710.oracle import btnUnpad, encrypt, decrypt
from btn710.attack import elementForgery, sequenceXor, positionalByteForgery
from Crypto.Util.py3compat import bchr

if __name__ =='__main__':
    # Normal Client
    plainText = b'Hello world!'
    cipherText = encrypt(plainText)
    print(b'Cipher Text: ' + cipherText)
    print(b'Plain Text: ' + decrypt(cipherText))
    
    # Attack Client
    iv = cipherText[:16]
    lastBlock = cipherText[-16:]
    forgery = b'0000000000000000'
    intermediateValue = []

    # Finding last byte correct padding
    correctPadding = False
    count = 0 #I
    while(not correctPadding):
        try: 
            decrypt(forgery + lastBlock)
            correctPadding = True
        except ValueError:
            forgery = positionalByteForgery(forgery, count, 15)
            count += 1
    tempLastIV = forgery.decode('utf-8')[-1]

    # Modify each element until we know the padding length
    count = 0
    while(correctPadding):
        try: 
            decrypt(forgery + lastBlock)
            forgery = elementForgery(forgery, count)
            count += 1
        except ValueError:
            correctPadding = False

    # Save last correct byte into intermediate value
    correctPaddingLength = 17 - count
    if(correctPaddingLength == 1): 
        intermediateValue.insert(0, tempLastIV)

    # Creating correct padding for full block size
    position = 14
    value = 0
    while(position >= 0):
        forgery = sequenceXor(forgery,intermediateValue, value)
        correctPadding = False
        forgeryCounter = 0
        while (not correctPadding):
            try:
                decrypt(forgery + lastBlock)
                correctPadding = True
                temp = [forgery[i] for i in range(0, len(forgery))]
                intermediateValue.insert(0, chr(temp[position]))   
            except ValueError:
                forgery = positionalByteForgery(forgery, forgeryCounter, position)
                forgeryCounter += 1
        position -= 1
        value += 1

    # Crack plaintext by xoring intermediate value and IV
    seperateIV = list(iv)
    crackedPlainText = []
    for i in range(16):
        crackedPlainText.append( bchr(seperateIV[i] ^ int.from_bytes(bytes(intermediateValue[i], 'utf-8'),"big")))
    crackedPlainText = b''.join(crackedPlainText)
    crackedPlainText = btnUnpad(crackedPlainText, 16, 'btn710')[1]
    print(crackedPlainText)