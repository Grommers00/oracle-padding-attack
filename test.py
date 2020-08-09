import sys
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad
from Crypto.Util.py3compat import bchr, bord
import random, string
from enum import Enum
def btnUnpad(padded_data, block_size, style):
    pdata_len = len(padded_data)
    if pdata_len % block_size:
        raise ValueError
    if style in ('btn710'):
        padding_len = bord(padded_data[-1]) + 1
        if padding_len<1 or padding_len>min(block_size, pdata_len):
            raise ValueError
        padding = bytearray()
        for x in range(padding_len):
            padding += bchr(x)
        if padding_len>1 and padded_data[-padding_len:]!=padding:
            raise ValueError
    else:
        raise ValueError
    return 1, padded_data[:-padding_len]
def test():
    print(b'00000000000000\x04\x043\xd6\x8f\x80\x8b\xbfm\x9d\xa9\x03\xde[(\x8c\xf4:'')
    print(btnUnpad())

test()