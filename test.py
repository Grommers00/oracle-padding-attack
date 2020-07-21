import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter


nonce = b'abcd'
ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
key = b'1234567891234567'
plaintext = b'James'
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
ciphertext = cipher.encrypt(plaintext)
print(ciphertext)
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)