from math import floor

def valid(board, i):
    row, col = floor(i / 9), i % 9
    row_head, box_start = row * 9, 9 * (row - (row % 3)) + (col - (col % 3))
    for n in range(9):
        if board[i] == board[row_head + n] and row_head + n != i:
            return False
        if board[i] == board[n * 9 + col] and n * 9 + col != i:
            return False
    for n in range(3):
        for m in range(3):
            if board[i] == board[box_start + 9 * n + m] and box_start + 9 * n + m != i:
                return False
    return True


def brute_solve(board):
    unlocked = [tile == 0 for tile in board]
    i, f = 0, True  # i = counter, f = direction (forward)
    while i != 81:
        if unlocked[i]:
            while True:
                board[i] += 1
                if board[i] == 10:
                    board[i], f = 0, False
                    i -= 1
                    break
                if valid(board, i):
                    f = True
                    i += 1
                    break
        else:
            i += 1 if f else -1
    return board


if __name__ == '__main__':
    raw = input("puzzle? ")
    prb = [int(raw[i]) for i in range(81)]
    sol = brute_solve(prb)
    pretty = []
    for i in range(9):
        pretty.append(prb[9 * i:9 * i + 9])
    [print(i) for i in pretty]
    print()
    pretty = []
    for i in range(9):
        pretty.append(sol[9*i:9*i+9])
    [print(i) for i in pretty]
