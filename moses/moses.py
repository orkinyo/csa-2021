import morse_talk as mtalk
import re

enc_msg = "x.xx...x.xxx..-xx-.xxxx.-.-xxx.-.x..x.xxxx..x.xxx.-.-.xx-.-xxx..-.xx.x.x.--x.xxx"

with open('book.txt') as f:
    words = re.findall(r"[a-zA-Z']+", f.read())

msg = []
tmp_enc_msg = enc_msg


def match(msg, morse):
    for i in range(len(msg)):
        if msg[i] != 'x' and msg[i] != morse[i]:
            return False
    return True


for word in words:
    morse = mtalk.encode(word)
    morse = morse.replace("   ", "")
    if match(tmp_enc_msg[:len(morse)], morse):
        msg.append(word)
        tmp_enc_msg = tmp_enc_msg[len(morse):]
        if not tmp_enc_msg:
            print("_".join(msg))
            break
    else:
        msg = []
        tmp_enc_msg = enc_msg