import solve
from random import choice, randrange

def gen_root():
    board, remaining = [0]*81, [[1, 2, 3, 4, 5, 6, 7, 8, 9] for n in range(81)]
    i, f = 0, True
    while i != 81:
        while True:
            if remaining[i]:
                board[i] = choice(remaining[i])
                remaining[i].remove(board[i])
                if solve.valid(board, i):
                    i += 1
                    break
                elif not remaining[i]:
                    board[i], remaining[i] = 0, [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    i -= 1
                    break
            else:
                board[i], remaining[i] = 0, [1, 2, 3, 4, 5, 6, 7, 8, 9]
                i -= 1
                break
    return board


def det_solvable(board):
    return 0 in solve.deterministic_solve(board)


def is_unique(board):
    unlocked = [tile == 0 for tile in board]
    i, f, c, u, last_unlocked = 0, True, unlocked.count(True), 0, 80  # i = counter, f = direction (forward)
    while not unlocked[last_unlocked]:
        last_unlocked -= 1
    while i >= 0:
        if unlocked[i]:
            while True:
                board[i] += 1
                if board[i] == 10:
                    board[i], f = 0, False
                    i -= 1
                    break
                if solve.valid(board, i):
                    f = True
                    if i == last_unlocked:
                        u += 1
                        if u == 2:
                            return False
                    else:
                        i += 1
                        break
        else:
            i += 1 if f else -1
    return True


def generate(diff):
    while True:
        root = gen_root()
        c = 0
        while c < 20000:
            board = root.copy()
            used = []
            for n in range(diff):
                i = randrange(81)
                while i in used:
                    i = randrange(81)
                used.append(i)
                board[i] = 0
            sol = solve.deterministic_solve(board.copy())
            if 0 not in sol:
                print(f'0 not in sol? {0 not in sol}')
                print(f'is unique? {is_unique(board.copy())}')
                print(c)
                return board
            c += 1
        print(c)


def print_prb(board):
    pretty = board.copy()
    for i in range(81):
        if pretty[i] == 0:
            pretty[i] = ' '
        else:
            pretty[i] = str(pretty[i])
    for n in range(9):
        if n % 3 == 0: print('----------------------')
        string = '|'
        for m in range(9):
            string = string + pretty[9*n+m] + ' '
            if m % 3 == 2:
                string = string + '|'
        print(string)
    print('----------------------')


if __name__ == '__main__':
    prb = generate(int(input('missing? ')))
    solve.print_board(prb)
    print_prb(prb)
