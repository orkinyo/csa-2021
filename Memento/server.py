import flag, shortest_path
import random, json, base64

def verify_game(board, level):
    card_number = random.randint(1, 20)
    board_obj = base64.b64decode(json.loads(board))
    indexes = []
    for i in range(5):
        for j in range(8):
            if board_obj[i][j] == card_number:
                indexes.append([i, j])
    
    shortest = shortest_path(indexes[0], indexes[1], board, "UP|DOWN|LEFT|RIGHT")
    shortest = shortest.length - 1
    result = 0
    if shortest == (flag[level] % 9) + 1:
        result = 1
    return result