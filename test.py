import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string

def byteTesting():

    forgedMsg = b"hello"
    print(forgedMsg[:-1])
    x = 10
    for i in range(10):
        forgedMsg = forgedMsg[:-1] + bchr(forgedMsg[-1] ^ i)
        print(type(forgedMsg))

byteTesting()