from pwn import *
import randcrack
import requests
import json
import time

big_num = 6277101735386680763835789423207666416102355444464034512895
PRINTABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+-/:.;<=>?@[]^_`{}"

s = requests.Session()
url = "http://slot-machine-reloaded.csa-challenge.com/"
url_spin = f"{url}spin/?coins=1"

s.get(url)

rc = randcrack.RandCrack()

def get_32_bit_outputs_from_num(num):
    rng = format(num, '#0194b')[2:]
    lst_rng = []
    for i in range(0, 192, 32):
        lst_rng.append(int(rng[i:i + 32],2))
    lst_rng = lst_rng[::-1]
    return lst_rng

def get_rand_output(spin_output):
    r = []
    start = 0
    for out in spin_output:
        out_int = PRINTABLE.find(out)
        start = start << 6
        start += out_int
    return start

def get_flag_char_indexes(num):
    """return list of indexes that randbelow returned zero for"""
    l = []
    for i in range(0,192,6):
        predict = format(num, '#0194b')[2:][i:i+6]
        if int(predict,2) == 0: #flag character will be at this index
            l.append(i // 6)
    return l

def main():
    for _ in range(104):
        result = s.get(url_spin).text
        time.sleep(0.05)
        spin_output = json.loads(result)["result"]
        num = get_rand_output(spin_output)
        outputs = get_32_bit_outputs_from_num(num)
        for out in outputs:
            rc.submit(out)

    print("finished predicting!")
    for _ in range(200-104):
        s.get(url_spin)
        time.sleep(0.05)
        rc.predict_randbelow(big_num)
    print("fininshed stalling")
    flag = ["?"] * 32
    while True:
        if "?" not in flag:
            print("wooho found flag!")
            print(f"flag = {''.join(flag)}")
            exit(0)
        result = s.get(url_spin).text
        spin_output = json.loads(result)["result"]

        next_result = rc.predict_randbelow(big_num)
        flag_char_indexes = get_flag_char_indexes(next_result)
        for flag_char_index in flag_char_indexes:
            if flag[flag_char_index] == '?':
                flag[flag_char_index] = spin_output[flag_char_index]
                print(f"flag = {''.join(flag)}")
if __name__ == '__main__':
    main()