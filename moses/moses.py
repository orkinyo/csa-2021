import morse_talk as mtalk
import re

enc_msg = "x.xx...x.xxx..-xx-.xxxx.-.-xxx.-.x..x.xxxx..x.xxx.-.-.xx-.-xxx..-.xx.x.x.--x.xxx"

with open('files/book.txt') as f:
    words = re.findall(r"[a-zA-Z']+", f.read())

flag = []
tmp_enc_msg = enc_msg
for word in words:
    morse_word = mtalk.encode(word).replace("   ", "")  # remove spaces
    enc_word = tmp_enc_msg[:len(morse_word)]
    if all(enc_word[i] == 'x' or enc_word[i] == morse_word[i] for i in range(len(enc_word))):
        flag.append(word)
        tmp_enc_msg = tmp_enc_msg[len(morse_word):]
        if not tmp_enc_msg:
            print("CSA{" + "_".join(flag) + "}")
            break
    else:
        flag = []
        tmp_enc_msg = enc_msg