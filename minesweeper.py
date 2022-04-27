# Steps:
# 1. Create the board and plant the bombs
# 2. Show user the board and ask for where they want to dig
# 3-a. if location is bomb show game over message
# 3-b. if location is not a bomb, dig recursively until each square is at least next to a bomb
# 4. Repeat steps 2 and 3(a,b) until there are no places to dig which means -----> VICTORY!

#create an object of the game
import random
import re


class Board():
    def __init__(self, board_size,bombs):
        # keep track of these parameters, they will be helpful later
        self.board_size= board_size
        self.bombs= bombs

        #creating the board
        #helper funtion

        self.board =self.new_board()  # plant the bombs
        self.assign_values()  #assigning values to board

        # initialize a set to keep track of which location we have uncovered
        # we will save (row, column) tuples into thus set

        self.dug= set()  #if we dig at 1,1 then self.dig={(1,1)}

    def new_board(self):
        # construct a new board based on the board size and the number of bombs
        # we should construct the list of lists here where each sublist is just a row of this board

        # generate a new board
        board =[[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        # this creates an array like this:
        #[ None, None,...., None],
        #[ None, None,...., None],
        #[ None, None,...., None],
        #[ ......               ],
        #[ None, None,...., None]
        # we can see how this represents the board!

        #plant the bombs
        bombs_planted=0
        while bombs_planted< self.bombs:
            location = random.randint(0, self.board_size**2 -1) # return a random integer N such that a<= N <=b
            row= location //self.board_size #to get row and column of that id we have chosen from this random selector
            col= location % self.board_size # we want the remainder to tell us what index in that row to look

            if board[row][col]=='*':
                # this means we have actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' #plant bombs
            bombs_planted += 1

        return board
    def assign_values(self):
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.neighbouring_bombs(r,c)

    def neighbouring_bombs(self, row, col):
        #let's iterate through each of the neighbouring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle : (row+1, col)
        # bottom right: (row+1, col+1)

        #make sure to not go out o bombs

        num_neigh_bombs= 0
        for r in range(max(0,row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1 ,col+1)+1):
                if r== row and c==col:
                    #our original location, don't check
                    continue

                if self.board[r][c] == '*':
                    num_neigh_bombs +=1

        return num_neigh_bombs


    def dig(self, row, col):
        #dig at that locatiom!
        #return True if successful dig, False is bomb dug
        self.dug.add((row,col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] >0:
            return True
        #self.board[row][col] ==0
        for r in range(max(0,row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1 ,col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)

        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.board_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.board_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep

def game(board_size=10, bombs=10):
    board = Board(board_size, bombs)
    safe= True

    while len(board.dug)  < board.board_size**2 - bombs:
        print(board)
        #0,0 or 0, 0 or 0,   0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int (user_input[0]), int(user_input[-1])
        if row<0 or row>=board.board_size or col<0 or col>=board.board_size:
            print("invalid location. Try agian")
            continue

        safe= board.dig(row,col)
        if not safe:
            break
    if safe:
        print(" CONGRATULATIONS")
    else:
        print("sorry game over")
        board.dug= [(r,c) for r in range(board.board_size) for c in range(board.board_size)]
        print(board)


if __name__ == '__main__':
    game()




