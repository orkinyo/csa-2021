from Crypto.Cipher import ARC4
import itertools

key_checker_data = b"\xE0\x33\x70\x95\xA1\xE5\x03"

#flag == CSA{hEY_th@T_l5_thE_9RE4T_p[ZZL3}

def check_key(key, key_checker_data):
    """ returns True is the key is correct.
        Usage:
        check_key('[I_think_this_is_the_key]', key_checker_data)
    """
    return ARC4.new(("CSA" + key).encode()).decrypt(key_checker_data) == b'success'

def recurse(l1, l2):
    ret = [1] * (len(l1) * len(l2))
    for i1, c1 in enumerate(l1):
        for i2, c2 in enumerate(l2):
            ret[(i1 * len(l2) ) + i2] = c1 + c2
    return ret

options = [['E', '3'], ['Y', 'y'], ['_'], ['T', 't'], ['h', 'H'], ['4', '@', 'A'], ['T', 't'], ['_'],
           ['1', 'i', 'l'], ['5', 'S'], ['_'], ['T', 't'], ['h', 'H'], ['E', '3'], ['_'], ['9', 'g'], ['r', 'R'],
           ['E', '3'], ['4', '@', 'A'], ['T', 't'], ['_'], ['9', 'p'], ['[', 'u'], ['z', 'Z'], ['z', 'Z'], ['1', 'L'],
           ['E', '3']]

my = [['h','H']]
for i in range(1,len(options),1):
    my[0] = recurse(my[0], options[i])

for flag in my[0]:
    if check_key("{" + flag + "}", key_checker_data):
        print(f"{flag=}")

        
