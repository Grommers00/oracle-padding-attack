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
