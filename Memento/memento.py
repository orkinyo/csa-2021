import base64
import string
import random
import requests

def create_board(level, index):
    card = random.randint(1, 20)
    pool = [card, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0]
    pool[index] = card
    board = [[], [], [], [], []]
    for i in range(5):
        for j in range(8):
            board[i].append(pool[i * 8 + j])
    board64 = base64.b64encode(board.__str__().replace(' ', '').encode()).decode()
    while True:
        try:
            r = requests.get(f"http://memento.csa-challenge.com:7777/verifygame?level={level}&board={board64}")
            break
        except:
            pass
    return r.text, board

def possible_char(path):
    pos = []
    for i in string.ascii_lowercase + "_":
        if ord(i[0]) % 9 + 1 == path:
            pos.append(i)
    return pos

def main():
    for level in range(4, 25):
        index = 36
        is_valid = '0'
        while is_valid == '0':
            index += 1
            is_valid, board = create_board(level, index)
            index = index % 39
        path = index % 8 + int(index / 8)
        print(possible_char(path))

if __name__ == "__main__":
    main()
