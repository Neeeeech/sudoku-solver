from math import floor

box_arr = [[0,1,2,9,10,11,18,19,20],
           [3,4,5,12,13,14,21,22,23],
           [6,7,8,15,16,17,24,25,26],
           [27,28,29,36,37,38,45,46,47],
           [30,31,32,39,40,41,48,49,50],
           [33,34,35,42,43,44,51,52,53],
           [54,55,56,63,64,65,72,73,74],
           [57,58,59,66,67,68,75,76,77],
           [60,61,62,69,70,71,78,79,80]]

def col_iter(n, col_no):
    return 9*n + col_no

def row_iter(n, row_no):
    return 9*row_no + n

def box_iter(n, box_no):
    return 3*(box_no % 3) + 27*floor(box_no / 3) + n % 3 + 9*floor(n / 3)


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
    change = 0
    for tile_no in range(81):
        if len(possibles[tile_no]) == 1:
            fill_in(board, possibles, tile_no, possibles[tile_no][0])
            change = 1
    return change


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
    check_group(board, possibles, col, col_iter)
    check_group(board, possibles, row, row_iter)
    check_group(board, possibles, 3*(floor(row/3)) + floor(col/3), box_iter)


def check_group(board, possibles, line_no, iterator):
    line_poss, change = [], 0
    for n in range(9):
        line_poss = line_poss + possibles[iterator(n, line_no)]
    for m in range(1,10):
        if line_poss.count(m) == 1:
            for n in range(9):
                if m in possibles[iterator(n, line_no)]:
                    fill_in(board, possibles, iterator(n, line_no), m)
                    change = 1
    return change


def check_dup(possibles, line_no, iterator):
    tiles_poss, change = [], 0
    for n in range(9):
        tiles_poss.append(possibles[iterator(n, line_no)])
    for tile_poss in tiles_poss:
        if tiles_poss.count(tile_poss) > 1 and tiles_poss.count(tile_poss) == len(tile_poss):
            for n in range(9):
                target = possibles[iterator(n, line_no)]
                if target != tile_poss:
                    for possibility in tile_poss:
                        if possibility in target:
                            target.remove(possibility)
                            change = 1
    return change


def check_box_must_line(board, possibles, box_no):
    """if all possibles of 1 num of box are in the same line, remove other possibles of this num in same line outside box"""
    remaining, change = [1,2,3,4,5,6,7,8,9], 0
    for n in range(9):
        if board[box_iter(n, box_no)] != 0:
            remaining.remove(board[box_iter(n, box_no)])
    for num in remaining:
        rows, cols = [], []
        for n in range(9):
            if num in possibles[box_iter(n, box_no)]:
                rows.append(3*floor(box_no/3) + floor(n/3))
                cols.append(3*(box_no%3) + n%3)
        rows, cols = set(rows), set(cols)
        if len(rows) == 1:
            row = rows.pop()
            for n in range(9):
                if row_iter(n, row) not in box_arr[box_no] and num in possibles[row_iter(n, row)]:
                    possibles[row_iter(n, row)].remove(num)
        if len(cols) == 1:
            col = cols.pop()
            for n in range(9):
                if col_iter(n, col) not in box_arr[box_no] and num in possibles[col_iter(n, col)]:
                    possibles[col_iter(n, col)].remove(num)
                    change = 1
    return change


def check_line_must_box(board, possibles, line_no, iter):
    remaining, change = [1,2,3,4,5,6,7,8,9], 0
    for n in range(9):
        if board[iter(n, line_no)] != 0:
            remaining.remove(board[iter(n, line_no)])
    for num in remaining:
        boxes, tiles = [], []
        for n in range(9):
            if num in possibles[iter(n, line_no)]:
                tiles.insert(0, iter(n,line_no))
                boxes.append(3*floor(tiles[0]/27) + floor((tiles[0] % 9)/3))
        boxes = set(boxes)
        if len(boxes) == 1:
            box = boxes.pop()
            for n in range(9):
                if box_iter(n, box) not in tiles and num in possibles[box_iter(n, box)]:
                    possibles[box_iter(n, box)].remove(num)
                    change = 1
    return change


def deterministic_solve(board):
    possibles = [[1,2,3,4,5,6,7,8,9] if tile == 0 else [] for tile in board]
    for tile_no in range(81):
        if board[tile_no] != 0:
            update_possibles(possibles, tile_no, board[tile_no])
    update_sures_all(board, possibles)
    change_outer = 1
    while change_outer != 0:
        change = 1
        while change != 0:
            change = 0
            for n in range(9):
                for iter in [col_iter, row_iter, box_iter]:
                    change += check_group(board, possibles, n, iter)
                    change += check_dup(possibles, n, iter)
                change += update_sures_all(board, possibles)
        change_outer = 0
        for n in range(9):
            change_outer += check_box_must_line(board, possibles, n)
            change_outer += check_line_must_box(board, possibles, n, row_iter)
            change_outer += check_line_must_box(board, possibles, n, col_iter)
    return board


def print_board(board):
    pretty = []
    print()
    for i in range(9):
        pretty.append(board[9*i:9*i+9])
    [print(i) for i in pretty]
    print()


if __name__ == '__main__':
    raw = input("puzzle? ")
    prb = [int(raw[i]) for i in range(81)]
    print_board(prb)
    print('\n\nDeterministic Solve:')
    sol = deterministic_solve(prb.copy())
    print_board(sol)
    print('\n\nBrute Solve:')
    sol = brute_solve(prb.copy())
    print_board(sol)
