from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

key = b'1234567891234567'
iv = b'0123456789012345'

def btnPad(data_to_pad, block_size, style):
	padding_len = block_size-len(data_to_pad)%block_size
	padding = bytearray()
	if style == 'btn710':
		for x in range(padding_len):
			padding += bchr(x)
	else:
		raise ValueError('Unknown padding style')
	return data_to_pad + padding

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

def encrypt(plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return iv + cipher.encrypt(btnPad(plaintext, AES.block_size, 'btn710'))

def decrypt(cipherText):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return btnUnpad(cipher.decrypt(cipherText), AES.block_size, 'btn710')[1]
  
