import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string
from enum import Enum

def findXorByte(testByte, value):
    return testByte ^ value 

def test():
   for i in range(0):
       print(i)

test()