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


def update_possibles(possibles, tile_no, tile):
    possibles[tile_no] = []
    row, col = floor(tile_no / 9), tile_no % 9
    row_head, box_start = row * 9, 9 * (row - (row % 3)) + (col - (col % 3))
    for n in range(9):
        if tile in possibles[row_head + n]:
            possibles[row_head + n].remove(tile)
        if tile in possibles[n * 9 + col]:
            possibles[n * 9 + col].remove(tile)
    for n in range(3):
        for m in range(3):
            if tile in possibles[box_start + 9 * n + m]:
                possibles[box_start + 9 * n + m].remove(tile)


def fill_in(board, possibles, tile_no, num):
    board[tile_no] = num
    possibles[tile_no] = []
    update_possibles(possibles, tile_no, num)
    update_sures_related(board, possibles, tile_no)


def update_sures_all(board, possibles):
    for tile_no in range(81):
        if len(possibles[tile_no]) == 1:
            fill_in(board, possibles, tile_no, possibles[tile_no][0])


def update_sures_related(board, possibles, tile_no):
    possibles[tile_no] = []
    row, col = floor(tile_no / 9), tile_no % 9
    row_head, box_start = row * 9, 9 * (row - (row % 3)) + (col - (col % 3))
    for n in range(9):
        if len(possibles[row_head + n]) == 1:
            fill_in(board, possibles, row_head + n, possibles[row_head + n][0])
        if len(possibles[n * 9 + col]) == 1:
            fill_in(board, possibles, n * 9 + col, possibles[n * 9 + col][0])
    for n in range(3):
        for m in range(3):
            if len(possibles[box_start + 9 * n + m]) == 1:
                fill_in(board, possibles, box_start + 9 * n + m, possibles[box_start + 9 * n + m][0])


def deterministic_solve(board):
    possibles = [[1,2,3,4,5,6,7,8,9] if tile == 0 else [] for tile in board]
    for tile_no in range(81):
        if board[tile_no] != 0:
            update_possibles(possibles, tile_no, board[tile_no])
    update_sures_all(board, possibles)
    return board


if __name__ == '__main__':
    #prb = [6,0,0,0,0,0,0,5,0,9,0,0,8,3,0,0,0,0,0,0,1,0,0,0,0,0,3,0,0,0,0,0,2,0,0,0,0,5,0,0,0,7,0,0,6,0,7,2,0,1,0,0,0,0,0,0,0,4,0,0,1,0,0,0,0,0,0,0,0,7,2,5,0,0,0,1,0,9,6,0,0]
    #print(len(prb))

    raw = input("puzzle? ")
    prb = [int(raw[i]) for i in range(81)]
    sol = deterministic_solve(prb)
    pretty = []
    for i in range(9):
        pretty.append(prb[9 * i:9 * i + 9])
    [print(i) for i in pretty]
    print()
    #pretty = []
    #for i in range(9):
    #    pretty.append(sol[9*i:9*i+9])
    #[print(i) for i in pretty]

    #print(len(prb))
    sol = brute_solve(prb)
    pretty = []
    for i in range(9):
        pretty.append(prb[9 * i:9 * i + 9])
    [print(i) for i in pretty]
