import copy
SODOKU_SIZE = 3
def getSet(board, i ,j, s = None):
    """
    Take in an SODOKU_SIZE*SODOKU_SIZE sided square, and return a set of possibilities of i, j
    :param board:
    :param i:
    :param j:
    :return:
    """
    if s:
        out = set(s)
    else:
        out = set(range(1,SODOKU_SIZE**2+1))
    flooredPos = ((i//SODOKU_SIZE)*SODOKU_SIZE,(j//SODOKU_SIZE)*SODOKU_SIZE)
    for pos in range(SODOKU_SIZE):
        pair1 = (i,pos)
        pair2 = (pos, j)
        pair3 = (flooredPos[0] +pos//SODOKU_SIZE, flooredPos[1] + pos%SODOKU_SIZE)
        for pair in (pair1, pair2, pair3):
            if pair[0] != i or pair[1] !=j:
                num = board[pair[0]][pair[1]]
                if isinstance(num,int) and num!=0 and num in out:
                    out.remove(num)
                elif isinstance(num,set) and len(num) == 1 and next(iter(num)) in out:
                    out.remove(next(iter(num)))
    return out

def solve(board):
    """
    Takes in a board
    :param board: a two dimensional, well formed, matrix which contains the board, un-filled spaces have zero
    :return: None, if the board is unsolvable, or one possible solution if the board is solvable
    """
    # print(board)
    if all(len(board[i//(SODOKU_SIZE**2)][i%(SODOKU_SIZE**2)])==1 for i in range(SODOKU_SIZE**4)):
        return board
    if any(not len(board[i//(SODOKU_SIZE**2)][i%(SODOKU_SIZE**2)])for i in range(SODOKU_SIZE**4)):
        return None

    for i in range(SODOKU_SIZE**2):
        for j in range(SODOKU_SIZE**2):
            if len(board[i][j])!=1:
                for e in board[i][j]:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = {e}
                    remove_proc(new_board, i , j, e)
                    output = solve(new_board)
                    if output:
                        return output
    return None

def remove_proc(new_board, i, j, e):
    flooredPos = ((i // SODOKU_SIZE) * SODOKU_SIZE, (j // SODOKU_SIZE) * SODOKU_SIZE)
    for pos in range(SODOKU_SIZE**2):
        pair1 = (i, pos)
        pair2 = (pos, j)
        pair3 = (flooredPos[0] + pos // SODOKU_SIZE, flooredPos[1] + pos % SODOKU_SIZE)
        for pair in (pair1, pair2, pair3):
            i1 = pair[0]
            j1 = pair[1]
            if i1 != i or j1 != j:
                if e in new_board[i1][j1]:
                    new_board[i1][j1].remove(e)
                    if len(new_board[i1][j1]) ==1 :
                        remove_proc(new_board, i1, j1, next(iter(new_board[i1][j1])))


def do_rec_solve(board):
    """
    Takes in a board, which consists of a matrix of sets, and outputs, a board consisting of numbers, and only numbers if it is solvable
    otherwise returns none
    :param board:
    :return: a solution
    """
    board2 = [[{board[i][j]} if board[i][j] else getSet(board,i,j) for j in range(SODOKU_SIZE**2)] for i in range(SODOKU_SIZE**2)]
    return solve(board2)
def get_board1(board):
    board[0][1] = 2
    board[0][3] = 1
    board[1][2] = 6
    board[2][0] = 5
    board[2][2] = 3
    board[3][1] = 3
test_board = [[0 for i in range(SODOKU_SIZE**2)] for j in range(SODOKU_SIZE**2)]
get_board1(test_board)
solved = do_rec_solve(test_board)
#print(solved)
for y in range(SODOKU_SIZE**2):
    print("".join([str(solved[x][y]) for x in range(SODOKU_SIZE**2)]))
