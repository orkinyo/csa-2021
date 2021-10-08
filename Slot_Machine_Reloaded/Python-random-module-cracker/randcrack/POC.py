import random
from pwn import *
import randcrack

big_num = 6277101735386680763835789423207666416102355444464034512895

rc = randcrack.RandCrack()

gen = random.Random("seed")

for i in range(104):
    rng = format(gen._randbelow(big_num), '#0194b')[2:]
    lst_rng = []
    for i in range(0, 192, 32):
        lst_rng.append(int(rng[i:i + 32],2))
    lst_rng = lst_rng[::-1]
    for rng_num in lst_rng:
        rc.submit(rng_num)

print(rc.predict_getrandbits(32))
print(gen.getrandbits(32))