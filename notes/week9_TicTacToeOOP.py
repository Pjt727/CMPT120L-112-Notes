# Tic-Tac-Toe Game Object Programming

## This is an example of using OOP to make Tic-Tac-Toe
## At this point in the class, we have not gone over classes and whatnot
## Feel to make improvements to the code and submit pull requests!

## The idea of OOP in this instance is that we can have a class structure that broadly represents any connecting game
##  Then we can make objects from that class structure to make objects of connecting games which would be things such as
##  TikTacToe and Gomuku. This allows us to create a variety of different connecting games utilizing much of the same code.
## I also use a Player class for some added functionality
##  This allows for things in the game such as teaming, dynamic win message depending on who wins, and names

import string

class Player:
    def __init__(self, mark: str, win_message: str = "I Won", name: str = None):
        self.mark = mark
        self.win_message = win_message
        if name is None:
            self.name = mark
        else:
            self.name = name

class ConnectGame:
    def __init__(self, players: tuple[Player], size: int = 3, win_con: int = 3, cell_sep: str = '   ', is_row_alpha: bool = True):
        self.players = players
        self.player_gen = gentr_fn(players)
        self.player: Player = next(self.player_gen)
        self.size = size
        self.win_con = win_con
        self.cell_sep = cell_sep
        self.is_row_alpha = is_row_alpha

        self.col_inputs = list(range(1, size + 1))
        # Could fairly easily make this possible by starting making 27 AA and so on
        # I remeber a problem like this on leetcode but I don't think it really makes sense to
        #   implement it here because games that contain over 26 rows/columns would be hard to read on the command line anyways
        if is_row_alpha and (size > 26):
            raise ValueError("Alpha format is not supported for sizes over 26.")
        elif is_row_alpha:
            self.row_inputs =string.ascii_uppercase[0:size]
        else:
            self.row_inputs = list(range(1, size + 1))

        self.board: list[list[Player, None]] = []
        for i in range(size):
            self.board.append([None]*size)
        self.last_move = None

    def game_loop(self) -> None:
        while True:
            self.display_board()
            self.move()
            if self.check_win():
                self.display_board()
                print(f"{self.player.name} wins!")
                print(f"{self.player.name}: {self.player.win_message}")
                return
            if self.check_tie():
                self.display_board()
                print("The game ends in a tie.")
                return
            self.player = next(self.player_gen)

    def display_board(self) -> None:
        # lining it up well only for 1-100

        print(self.cell_sep, end = '')
        for col_name in self.col_inputs:
            if col_name < 10:
                print(f'{col_name}{self.cell_sep}', end='')
            else:
                print(f'{col_name}{self.cell_sep[0:-1]}', end='')

        print()
        for row, row_name in zip(self.board, self.row_inputs):
            print(f'{row_name}: ', end = '')
            for player in row:
                if player:
                    print(player.mark, end = self.cell_sep)
                else:
                    print('-', end = self.cell_sep)
            print()

        return
        

    def move(self) -> None:
        print(f"Player {self.player.name} with mark {self.player.mark} has the move.")
        if self.is_row_alpha:
            row = ask_for_input(information='row letter', accepted = self.row_inputs, type_req = str)
            row = self.row_inputs.index(row)
        else:
            row = ask_for_input(information='row number', accepted=self.row_inputs, type_req = int) - 1

        col = ask_for_input(information='column number', accepted=self.col_inputs, type_req = int) - 1

        row_i = row
        col_i = col

        if self.board[row_i][col_i] is not None:
            print(f"Row {row}, Column {col} is invalid because a mark already exists there.")
            self.move()
        
        self.board[row_i][col_i] = self.player
        self.last_move = (row_i, col_i)
        return
    
    def check_tie(self) -> bool:
        for row in self.board:
            # faster to use in because inbuilt looping is almost always faster bc of how python works
            if None in row:
                return False
        return True

    # These checks use the marks instead of the player object
    # This allows for multiple players to have the functionality of
    #   being on the same team
    def check_win(self) -> bool:
        if not self.last_move: return False

        if self.check_row(): return True
        if self.check_col(): return True
        if self.check_diag(): return True

        return False

    # amount of connecting can never be more than (2*win_con - 1)
    #   Therefore I think checking in the while if connecting >= win_con
    #   does not make the code more efficient
    # 1 needs to be added to include the connection of mark the player just put down
    def check_row(self) -> bool:
        # Counts how many connect to the last point left and right
        return self.conn_check(i_col = 1) + self.conn_check(i_col = -1) + 1 >= self.win_con
    
    def check_col(self) -> bool:
        # Counts how many connect to the last point up and down
        return self.conn_check(i_row = 1) + self.conn_check(i_row = -1) + 1 >= self.win_con
    
    def check_diag(self) -> bool:
        conn_left_right = self.conn_check(i_row=1, i_col=-1) + self.conn_check(i_row=-1, i_col=1)
        conn_right_left = self.conn_check(i_row=-1, i_col=-1) + self.conn_check(i_row=1, i_col=1)
        return (conn_left_right + 1 >= self.win_con) or (conn_right_left + 1 >= self.win_con)

    # takes iterators and iterates adding 1 to connecting if the mark is the same as the current player's marker
    def conn_check(self, i_row: int = 0, i_col: int = 0) -> int:
        row_num_s, col_num_s = self.last_move

        # the first iteration is done here
        row_num = row_num_s + i_row
        col_num = col_num_s + i_col

        connecting: int = 0

        while (0 <= row_num < self.size) and (0 <= col_num < self.size):
            if self.board[row_num][col_num] is None: break
            elif self.board[row_num][col_num].mark is not self.player.mark: break
            connecting += 1
            row_num += i_row
            col_num += i_col
        
        return connecting

# Returns type of input that is required and keeps asking until it gets a value that is in the accepted list
## I am stumped as to why this lets you input nothing for letter rows
## It treats nothing as A which is the first index of the accepted list
def ask_for_input(information, accepted: list, type_req = int):
    while True:
        usr_input = input(f"Give a {information} ({accepted[0]}-{accepted[-1]}): ")
        try:
            usr_input = type_req(usr_input)
            
        except ValueError:
            print(f"That was invalid type for a {information}")
            continue
        if usr_input not in accepted:
            print(f"That was invalid input for a {information}")
            continue
        return usr_input

# generator (look up python generators for more info)
def gentr_fn(loopable):
    while True:
        for j in loopable:
            yield j

def main():
    player1 = Player(mark='X',win_message='I am the very best!', name='Patrick')
    player2 = Player(mark='O', win_message='Well, that was easy!', name='Lex')
    player3 = Player(mark='X', win_message='Well, that was easy!', name='Ryann')
    player4 = Player(mark='O', win_message='Well, that was easy!', name='Isabella')
    
    # Example of different connect games you can play
    
    TicTacToe = ConnectGame((player1, player2, player3, player4), size=3, win_con=3)
    Gomoku = ConnectGame((player1, player2),size=15, win_con=5)

    TicTacToe.game_loop()
    Gomoku.game_loop()


main()