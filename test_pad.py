from Crypto.Util.py3compat import bchr, bord

message = b"hello"

padding = bytearray()
for x in range(11):
    padding += bchr(x)
pad_data = message + padding
padding_len = bord(pad_data[-1]) + 1
print(pad_data)
print(padding_len)
print(pad_data[-padding_len:])
