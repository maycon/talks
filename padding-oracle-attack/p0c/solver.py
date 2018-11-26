#!/usr/bin/env python

import socket, os
from pwn import *
from Crypto.Cipher import AES

# pip install --user paddingoracle
from paddingoracle import BadPaddingException, PaddingOracle

pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

HOST = "127.0.0.1"
PORT = 1043


# Encrypted data
encdata = [
  0xf3, 0x6a, 0xcf, 0xc4, 0x43, 0x9f, 0xf5, 0xa8, 0x7d, 0x53, 0x8e, 0x24, 0x58, 0x91, 0x18, 0x4b,
  0x58, 0x0d, 0x10, 0x40, 0x15, 0x99, 0x3d, 0xa1, 0x21, 0x5b, 0x38, 0x3e, 0x29, 0x73, 0xbf, 0x23,
  0x0e, 0x6c, 0x11, 0x24, 0xa5, 0x89, 0x11, 0x08, 0x98, 0xc2, 0x74, 0xdc, 0x52, 0x50, 0x3d, 0x99,
  0x79, 0xcb, 0xae, 0x31, 0x8b, 0x6b, 0xa9, 0xd1, 0x4f, 0xbf, 0x62, 0xb8, 0xe1, 0xe8, 0x26, 0xba,
  0x70, 0x67, 0x61, 0xa5, 0x7a, 0x99, 0xaa, 0x12, 0x41, 0x82, 0xa2, 0x02, 0xb4, 0xf6, 0x0a, 0x3d
]


# Split between the IV (first BS bytes) and the encrypted data
iv = encdata[:AES.block_size]
encdata_s = ''.join(chr(c) for c in encdata[AES.block_size:])


# A function that check if a given data returns a padding error from the Oracle system
def check_paddind_error(data):
    rem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rem.connect((HOST, PORT))
    rem.sendall("".join(chr(x) for x in data))
    line = rem.recv(5)
    rem.close()
    del rem
    return "bad" in line


class Attack(PaddingOracle):
    def __init__(self, **kwargs):
        super(Attack, self).__init__(**kwargs)

    def oracle(self, data, logger):
        logger.status(hexdump(data))

        if check_paddind_error(data):
            raise BadPaddingException()

l = log.progress('')
attack = Attack()
data = attack.decrypt(encdata_s, block_size=AES.block_size, iv=iv, logger=l)
l.success("The data was decrypted to '{}'".format(unpad(str(data))))
