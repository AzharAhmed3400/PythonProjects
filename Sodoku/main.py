board = [
        [8, 0, 2, 0, 0, 6, 0, 5, 0],
        [0, 4, 0, 0, 1, 8, 0, 0, 0],
        [0, 9, 0, 0, 0, 3, 0, 8, 4],
        [2, 0, 0, 0, 0, 9, 8, 0, 1],
        [0, 1, 0, 0, 0, 0, 5, 4, 9],
        [0, 8, 0, 0, 3, 0, 6, 0, 0],
        [0, 7, 8, 9, 0, 2, 4, 0, 5],
        [0, 2, 9, 0, 0, 5, 7, 0, 3],
        [5, 0, 1, 0, 7, 0, 9, 0, 8]
        ]

board_correct = [[8, 3, 2, 4, 9, 6, 1, 5, 7],
                [7, 4, 5, 2, 1, 8, 3, 9, 6],
                [1, 9, 6, 7, 5, 3, 2, 8, 4],
                [2, 5, 7, 6, 4, 9, 8, 3, 1],
                [6, 1, 3, 8, 2, 7, 5, 4, 9],
                [9, 8, 4, 5, 3, 1, 6, 7, 2],
                [3, 7, 8, 9, 6, 2, 4, 1, 5],
                [4, 2, 9, 1, 8, 5, 7, 6, 3],
                [5, 6, 1, 3, 7, 4, 9, 2, 8]
                ]


def isValid(bo, target, row, col):
    #check rows
    for i in range(len(bo[0])):
        if i != col and bo[row][i] == target:
            return False
    
    #check cols
    for i in range(len(bo)):
        if i != row and bo[i][col] == target:
            return False
    
    #check boxes
    r = row - row%3
    c = col - col%3
    for i in range(r, r+3):
        for j in range(c, c+3):
            if (i !=row and j!= col) and bo[i][j] == target:
                return False
    return True

def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i,j)
    return None

def solve(bo):
    f = find_empty(bo)
    if not f:
        return True
    else:
        row, col = f
    for i in range(1,10):
        if isValid(bo, i, row, col):
            bo[row][col] = i

            if solve(bo):
                return True
            else:
                bo[row][col] = 0
    return False


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if j % 3 == 0:
                print('|', end=" ")
            if j == len(board[i]) -1:
                print(board[i][j])
            else:
                print(board[i][j], end=" ")
        if (i + 1) % 3 == 0:
            print('-' * 23)
        
    
        
print_board(board)
solve(board)
print('_' * 30)
print_board(board)



