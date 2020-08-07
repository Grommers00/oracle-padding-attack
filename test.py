import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string
from enum import Enum

def test():
    class resState(Enum):
        lastState = 1
        secondState = 2
        thirdState = 3

    jordan = resState.lastState

    if(jordan == resState.lastState):
        print('hello')
    
test()