import operator
from Crypto.Util.number import long_to_bytes

with open('./flag', 'rb') as f:
    data = f.read()

reg = {0x1a: 0, 0x1b: 0, 0x1c: 0, 0x1d: 0, 0x1e: 0, 0x1f: 0}
ops = {0xab: operator.add, 0xba: operator.sub,
       0xcd: operator.mul, 0xdc: operator.ifloordiv}

for i in range(0, len(data), 2):
    if data[i] in reg:
        reg[data[i]] = data[i + 1]
    elif data[i] in ops:
        var1 = ((data[i + 1] >> 4) & 0xf) + 0x10
        var2 = (data[i + 1] & 0xf) + 0x10
        reg[var1] = ops[data[i]](reg[var1], reg[var2])
flag_len = len(hex(reg[0x1a])[2:]) // 2
flag = long_to_bytes(reg[0x1a]).decode()
print(flag)