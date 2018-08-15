# -*- coding:utf-8 -*-
import struct

data = b"\xaa\xae\x00\x00'\x1c\xff\xff\xf6\xdd?\xa5G\x11"

print(data)
(_,_,x,y,value) = struct.unpack('>BBiif',data)

print(struct.unpack('>BBiif',data))