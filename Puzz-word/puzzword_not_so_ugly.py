import requests
import json

start_url = "https://puzzword.csa-challenge.com/puzzle"
url = "https://puzzword.csa-challenge.com/solve"

class PegSolitaireBoard:
    def __init__(self, table):
        self.table = table

    def move(self, y, x, d):
        if self.table[y][x] != 1:
            return False
        if d == 0 and x - 2 >= 0 and self.table[y][x - 1] == 1 and self.table[y][x - 2] == 0:
            self.table[y][x] = self.table[y][x - 1] = 0
            self.table[y][x - 2] = 1
            return True
        if d == 1 and x + 2 < len(self.table[0]) and self.table[y][x + 1] == 1 and self.table[y][x + 2] == 0:
            self.table[y][x] = self.table[y][x + 1] = 0
            self.table[y][x + 2] = 1
            return True
        if d == 2 and y - 2 >= 0 and self.table[y - 1][x] == 1 and self.table[y - 2][x] == 0:
            self.table[y][x] = self.table[y - 1][x] = 0
            self.table[y - 2][x] = 1
            return True
        if d == 3 and y + 2 < len(self.table) and self.table[y + 1][x] == 1 and self.table[y + 2][x] == 0:
            self.table[y][x] = self.table[y + 1][x] = 0
            self.table[y + 2][x] = 1
            return True
        return False

    def unmove(self, y, x, d):
        if d == 0:
            self.table[y][x] = self.table[y][x - 1] = 1
            self.table[y][x - 2] = 0
        elif d == 1:
            self.table[y][x] = self.table[y][x + 1] = 1
            self.table[y][x + 2] = 0
        elif d == 2:
            self.table[y][x] = self.table[y - 1][x] = 1
            self.table[y - 2][x] = 0
        elif d == 3:
            self.table[y][x] = self.table[y + 1][x] = 1
            self.table[y + 2][x] = 0


class PegSolitaireSolver:
    def __init__(self, board, target):
        self.board = board

        tmp = 0
        for row in self.board.table:
            for elem in row:
                if elem == 0:
                    tmp += 1

        self.center_row = len(self.board.table) / 2
        self.center_column = len(self.board.table[0]) / 2

        self.solution = []
        self.target = target

        self.num_pegs = -tmp
        for row in self.target:
            for elem in row:
                if elem == 0:
                    self.num_pegs += 1

    def back_track(self, move):
        if move == self.num_pegs:
            if self.board.table == self.target:
                return True
            else:
                return False

        for r in range(len(self.board.table)):
            for c in range(len(self.board.table[0])):
                for d in range(4):
                    if self.board.move(r, c, d):
                        if self.back_track(move + 1):
                            self.solution.append((r, c, d))
                            return True
                        self.board.unmove(r, c, d)

        return False

    def solve(self):
        self.solution = []
        self.back_track(0)
        self.solution.reverse()

        return self.solution

    def get_solution(self, ):

        p_sol = []
        dir_map = {
            0: '<',
            1: '>',
            2: '^',
            3: 'v'
        }

        for step in self.solution:
            r, c, d = step
            p_sol.append([c, r, dir_map[d]])

            self.board.move(*step)
        return p_sol


def trans(table):
    board = []
    for i, row in enumerate(table):
        board.append([])
        for cell in row:
            if cell == 'O':
                board[i].append(1)
            elif cell == ' ':
                board[i].append(2)
            elif cell == '.':
                board[i].append(0)

    return board


def solve(board, target):
    answer = PegSolitaireSolver(PegSolitaireBoard(board), target)
    answer.solve()
    return answer.get_solution()


if __name__ == '__main__':
    res = requests.get(start_url)
    msg = json.loads(json.loads(res.text)["message"])
    while True:
        puzzle_id = msg["puzzle_id"]
        b = trans(msg["source_board"])
        t = trans(msg["destination_board"])
        sol = solve(b, t)
        data = {
            "puzzle_id": puzzle_id,
            "solution": sol
        }
        res = requests.post(url, json=data)
        msg = json.loads(json.loads(res.text)["message"])
        print(msg["message"])
        if "puzzle_id" not in msg:
            break
