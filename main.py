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
# a is the last block, k is the position of an element in that block, b is the index of the last element
#1. take rk = ak ⊕ (b − j + 2) for k = j, . . . , b
#2. pick r1, . . . , rj−1 at random and take i = 0
#3. take r = r1 . . . rj−2(rj−1 ⊕ i)rj . . . rb
#4. if O(r|y) = 0 then increment i and go back to the previous step
#5. output rj−1 ⊕ i ⊕ (b − j + 2)

from btn710.oracle import btnPad, btnUnpad, encrypt, decrypt
from btn710.attack import generateForgedMsg, lastByteForgery, elementForgery, secLastByteForgery, sequenceXor, positionalByteForgery
from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

if __name__ =='__main__':
    plainText = b'HelloWorld!aaaa'
    #Normal server-client messages
    cipherText = encrypt(plainText)
    print(b'Cipher Text: ' + cipherText)
    print(b'Plain Text: ' + decrypt(cipherText))
    
    # Finding last byte correct padding
    intermediateValue = []
    iv = cipherText[:16]
    forgedMsg, forgery, forgedLastByte, lastBlock = generateForgedMsg(cipherText) 
    correctPadding = False
    count = 0 #I
    while(not correctPadding):
        try: 
            decryptedMsg = decrypt(forgedMsg) #0000000000 + $&!($^^00x01x00x3 
            correctPadding = True
        except ValueError:
            forgedMsg, forgery = lastByteForgery(forgery, forgedLastByte, lastBlock, count)
            count += 1
    tempLastIV = forgery.decode('utf-8')[-1] #5 for now, last character of the IV

    # Modify each element until we know the padding length - part 5 -  section A
    count = 0
    print(forgedMsg)
    while(correctPadding):
        try: 
            decrypt(forgedMsg)
            forgedMsg = elementForgery(forgedMsg, count)
            count += 1
        except ValueError:
            correctPadding = False
            

    correctPaddingLength = 17 - count #16
    if(correctPaddingLength == 1): 
        intermediateValue.insert(0, tempLastIV) #5 

    # find byte that xor with last byte to 1
    # set last byte to that new byte
    # loop through second last byte with xor 0-255 to find write padding
    # modify each element up til but not including the second last byte and test each to see what is the padding length
    
    # Step 1 Ak is every single character before the last one
    # cot last byte - minus current position + 2
    #take rk = ak ⊕ (b − j + 2) for k = j, . . . , b

    position = 14
    value = 0

    while(position >= 0): #goes backwards, not forwards. it should be while position > 0 but we only want it to b-j(-1)
        forgery = sequenceXor(forgery,intermediateValue, value) #not correct, because we are just 
        # try and decrypt this msg, and if not good then keep changing forgery[position]
        # if we get bad padding then xor with i 0 - 255
        correctPadding = False
        forgeryCounter = 0
        while (not correctPadding):
            try:
                decrypt(forgery + lastBlock) #
                correctPadding = True
                temp = [forgery[i] for i in range(0, len(forgery))]
                intermediateValue.insert(0, chr(temp[position]))   
            except ValueError:
                forgery = positionalByteForgery(forgery, forgeryCounter, position)     #gets executed until finding right character
                forgeryCounter += 1
        position -= 1
        value += 1
    #3 and #4 has to be done in its in own loop 
    #5 replace their step with ours based on our padding scheme
    #lastly XOR the a with the cipher text to retrieve the plain text
    print(intermediateValue) 
    intermediateValue = ''.join(intermediateValue)
    intermediateValue = bytes(intermediateValue,'utf-8')
    print(iv)
    print(intermediateValue)
