import curses
import sys
from copy import deepcopy

from board import Board
from game_exception import BoardException, LetterCommandException
from view import display, show_cell_nums


# set curses colors and run the main game loop
def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    msg_line = (13, 0)
    prev_cmd = '  '

    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
        deal = Board(seed)
    else:
        deal = Board()

    history = []
    history.append(deepcopy(deal))

    while True:
        stdscr.clear()
        deal.auto_move()
        display(stdscr, deal)

        stdscr.addstr("Press 'q' to quit.\n")
        stdscr.addstr("Press 'h' for help.\n")
        stdscr.addstr(">>{:>3} ".format(prev_cmd))

        stdscr.addstr('>')
        cmd = input_command(stdscr)
        if cmd == 'q':
            break
        if cmd == 'h':
            stdscr.move(*msg_line)
            try:
                show_help(stdscr)
            except curses.error:
                stdscr.move(*msg_line)
                stdscr.addstr('ERROR: Window is too small.', curses.A_REVERSE)
            stdscr.getkey()
            continue
        if cmd == 'u':
            if len(history) > 1:
                deal = deepcopy(history[-2])
                history.pop()
            continue

        try:
            perform_move(cmd, deal)
        except BoardException as problem:
            stdscr.move(*msg_line)
            stdscr.addstr(str(problem))
            stdscr.getkey()
        else:
            history.append(deepcopy(deal))
            prev_cmd = cmd


# get user input until a valid command is constructed; then return it
def input_command(window):
    try:
        cmd = input_char(window, 0, 8)
        if cmd == '0':
            cmd += input_char(window, 1, 4)
        cmd += input_char(window, 0, 9)
    except LetterCommandException as exc:
        cmd = exc.letter

    return cmd


# get valid characters (may include letters) from user; echoing them
def input_char(window, nmin, nmax):
    if nmin == 1 and nmax == 4:
        show_cell_nums(window)
    while True:
        try:
            char = window.getkey()
        except KeyboardInterrupt:
            sys.exit()
        if char in 'qhu':
            raise LetterCommandException(char)
        if char.isdecimal() and (nmin <= int(char) <= nmax):
            break
    window.addstr(char)
    return char


def show_help(window):
    window.addstr("Press 'u' to undo.\n")
    window.addstr('\nColor Groups:\n')
    window.addstr("\tClubs", curses.color_pair(1))
    window.addstr(" and ")
    window.addstr("spades\n", curses.color_pair(2))
    window.addstr("\tHearts", curses.color_pair(3))
    window.addstr(" and ")
    window.addstr("diamonds\n", curses.color_pair(4))

    window.addstr("\nTo move, type the number of the origin then the number of the destination.\n")
    window.addstr("Origins:      1-8 for cascades; 0 then 1-4 for cells\n")
    window.addstr("Destinations: 1-8 for cascades; 0 for the cells; 9 for the foundations\n")
    window.addstr("\nStacks of cards will be handled automatically. Note: If you do not want the largest moveable stack to move to an empty cascade, simply move the cards manually using the cells.\n")
    window.addstr('\nExample command line: "python3 quickcell.py 399677"')


def perform_move(cmd, board):
    if cmd[0] == '0':
        cell = int(cmd[1]) - 1
        if cmd[2] == '9':
            board.cell_to_foundations(cell)
        else:
            row = int(cmd[2]) - 1
            board.cell_to_row(cell, row)
    else:
        from_row = int(cmd[0]) - 1
        to_row = int(cmd[1]) - 1
        if cmd[1] == '9':
            board.row_to_foundations(from_row)
        elif cmd[1] == '0':
            board.row_to_cell(from_row)
        else:
            board.row_to_row(from_row, to_row)


curses.wrapper(main)
