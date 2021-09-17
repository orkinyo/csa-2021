from subprocess import Popen, PIPE
import string
from time import perf_counter
from operator import itemgetter

alphabet = string.digits + string.ascii_letters + string.punctuation

process = Popen("./pass_it_on.exe", stdin=PIPE, stderr=PIPE, stdout=PIPE)

flag = b"CSA{"

time_arr = []

# BRUTE_FORCE_LENGTH
for i in range(1, 40):
    process.stdout.readline()
    test = flag + b"A" * i + b"\n"
    t1 = perf_counter()
    process.stdin.write(test)
    process.stdin.flush()
    process.stdout.readline()
    t2 = perf_counter()
    time_arr.append((t2-t1, i))

max_time_array = max(time_arr, key=itemgetter(0))
last_time = max_time_array[0]
flag_len = max_time_array[1]
print(f"flag length is {flag_len + len(flag)}")

process.terminate()
process = Popen("./pass_it_on.exe", stdin=PIPE, stderr=PIPE, stdout=PIPE)


for i in range(1, flag_len):
    time_arr = []
    for c in alphabet:
        process.stdout.readline()
        test = flag + c.encode() + b"?" * (flag_len - i - 1) + b"}" + b"\n"
        t1 = perf_counter()
        process.stdin.write(test)
        process.stdin.flush()
        process.stdout.readline()
        t2 = perf_counter()
        if (t2 - t1) - last_time >= 0.05:
            flag += c.encode()
            to_print = flag.decode() + "?" * (flag_len - i - 1) + "}"
            print(to_print)
            last_time = t2 - t1
            break
        else:
            last_time = t2 - t1
print(f"found the flag: {flag.decode() + '}'}")
