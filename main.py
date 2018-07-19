import curses
import itertools


class PositionOccupiedError(Exception):
    """Position on board is already occupied"""
    pass


class Player(object):
    def __init__(self, number, symbol):
        self.number = number
        self.symbol = symbol


class TicTacToe(object):

    def __init__(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self._players = itertools.cycle([Player(1, 'X'), Player(2, '0')])
        self.current_player = self._players.__next__()
    
    def next_player(self):
        self.current_player = self._players.__next__()

    def print(self):
        for row in self.board:
            for col in row:
                if col is None:
                    col = ' '
                print(col, end=' ')
            print('\n')

    def make_move(self, x, y):
        x -= 1
        y -= 1
        if self.board[y][x] is None:
            self.board[y][x] = self.current_player
        else:
            raise PositionOccupiedError

        self.next_player()

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] and b[i][1] == b[i][2]:
                return b[i][0]
            if b[0][i] == b[1][i] and b[1][i] == b[2][i]:
                return b[0][i]
        if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
            return b[0][2]
        return None

    def screen(self, stdscr):
        def print_board():
            for y, row in enumerate(self.board):
                for x, sq in enumerate(row):
                    sq = sq.symbol if sq else ' '
                    stdscr.addch(y * 2 + 1, x * 2 + 1, sq)

        def print_player():
            stdscr.addstr(
                0, 0, f' PLAYER {self.current_player.number}', curses.A_REVERSE
            )
            stdscr.chgat(-1, curses.A_REVERSE)

        def print_winner(winner):
            msg = f'PLAYER {winner.number} WINS!'
            x = (curses.COLS // 2) - (len(msg) // 2)
            y = (curses.LINES // 2)
            stdscr.move(y, 0)
            stdscr.chgat(-1, curses.A_REVERSE)
            stdscr.addstr(y, x, msg, curses.A_REVERSE)
            
            stdscr.getch()

        def print_warning(msg):
            stdscr.addstr(10, 1, msg, curses.A_BOLD | curses.color_pair(1))
            stdscr.getch()
            stdscr.move(10, 0)
            stdscr.clrtoeol()

        def ask_for_move(axis):
            curses.curs_set(0)
            pos = None

            while True:
                msg = 'Choose a {} position: {}'.format(axis, (pos or ' '))
                stdscr.addstr(10, 1, msg)

                c = chr(stdscr.getch())
                if '\n' in c and pos:
                    return int(pos)

                pos = c if (c in {'1', '2', '3'}) else None
                stdscr.refresh()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        winner = None
        while not winner:
            print_player()
            print_board()
            stdscr.refresh()
            x = ask_for_move('X')
            y = ask_for_move('Y')
            try:
                self.make_move(x, y)
            except PositionOccupiedError:
                print_warning("Position already occupied - try again!")
                continue
            winner = self.check_winner()

        stdscr.clear()
        print_winner(winner)
        stdscr.refresh()

    def play(self):
        curses.wrapper(self.screen)


def play_game():
    board = TicTacToe()
    board.print()
    while True:
        board.make_move()
        board.print()
        winner = board.check_winner()
        if winner:
            player = 'Player 1' if winner == 'X' else 'Player 2'
            print(f'{player} wins!!!')
            break


if __name__ == "__main__":
    game = TicTacToe()
    game.play()