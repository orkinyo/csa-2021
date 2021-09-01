from pwn import *
r = remote("strange-game.csa-challenge.com", 4444)

BoardTranslate = [[8,1,6], [3,5,7], [4,9,2]]
Board = [['','',''], ['','',''], ['','','']]

I_START = False

def menu():
    r.recvuntil("Press any key...")
    r.sendline()
    print(r.recvline().decode())
    r.recvuntil("New game\n")
    line = r.recvline().decode()
    if "You" in line:
        I_START = True
    else:
        I_START = False
        
def parseInfoMove():
    pass
menu()



r.interactive()
