import base64

enFlag = b"WFKZLTABVKWVLXGMASVPYVP2ZRTKVHKV6XGBJKVEKX44YCVKXBK4XTBDVKSVL2WMACVLOVPEZQJ2VHCV"
b32Flag = base64.b32decode(enFlag)

key = "\xcc\x55\xaa"
#key = "CC55AA"

r = ""
for i in range(len(b32Flag)):
    r += chr(ord(key[i % len(key)]) ^ b32Flag[i])

print(r)