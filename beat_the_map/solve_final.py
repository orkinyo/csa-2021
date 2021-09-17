with open("files/challenge.bmp", "rb") as file:
    data = file.read()
triangular = [n * (n + 1) / 2 for n in range(350)]
data = data[0x436:]  # offset
bits_list = [d & 0x1 for i, d in enumerate(data) if i in triangular]
bytes_list = [int("".join(map(str, bits_list[i:i + 8])), 2) for i in range(0, len(bits_list), 8)]
print("".join([chr(b) for b in bytes_list]))