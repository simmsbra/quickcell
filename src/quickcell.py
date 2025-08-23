import curses
import sys
from copy import deepcopy

from board import Board
from game_exception import BoardException, LetterCommandException, InvalidCommandException
from view import display_game, show_cell_nums


# prepare game and run the main loop
def main(stdscr):
    set_colors()

    if len(sys.argv) > 1:
        seed = int(sys.argv[1])
        deal = Board(seed)
    else:
        deal = Board()

    history = []
    history.append(deepcopy(deal))

    prev_cmd = ''

    while True:
        deal.auto_move()
        stdscr.clear()
        display_game(stdscr, deal)

        stdscr.addstr("Press 'q' to quit.\n")
        stdscr.addstr("Press 'h' for help.\n")
        # previous command displays with a fixed width of 3
        stdscr.addstr(">>{:>3} ".format(prev_cmd))
        stdscr.addstr('>')

        cmd = input_command(stdscr)
        if cmd == 'q':
            break

        if cmd == 'n':
            deal = Board()
            history = []
            history.append(deepcopy(deal))
            prev_cmd = ''
            continue

        if cmd == 'h':
            stdscr.clear()
            try:
                print_help(stdscr)
            except curses.error:
                stdscr.clear()
                stdscr.addstr('ERROR: Window is too small.', curses.A_REVERSE)
            stdscr.getkey()

        elif cmd == 'u':
            if len(history) > 1:
                deal = deepcopy(history[-2])
                history.pop()

        else:
            try:
                validate(cmd)
                attempt_move(cmd, deal)
            except (InvalidCommandException, BoardException) as problem:
                stdscr.addstr('\n' + str(problem), curses.A_REVERSE)
                stdscr.getkey()
            else:
                history.append(deepcopy(deal))
                prev_cmd = cmd


def set_colors():
    # card suit colors
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    # colors for move examples in help section
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)


# get user input until a valid command is constructed
# then return the valid command
def input_command(window):
    curses.curs_set(1) # show cursor
    try:
        cmd = input_char(window)
        if cmd == '0':
            show_cell_nums(window)
            cmd += input_char(window)
        cmd += input_char(window)
    except LetterCommandException as exc:
        cmd = exc.letter

    curses.curs_set(0) # hide cursor
    return cmd


# get valid characters (may include letters) from user; echoing them
def input_char(window):
    while True:
        try:
            char = window.getkey()
        except KeyboardInterrupt:
            sys.exit()
        if char in 'qhun':
            raise LetterCommandException(char)
        if char.isdecimal():
            break
    window.addstr(char)
    return char


# makes sure a move command (2-3 digits) respects the rules
def validate(cmd):
    if cmd[0] == '0':
        if not (1 <= int(cmd[1]) <= 4):
            raise InvalidCommandException(cmd[1] + ' is not a valid cell number.')
        if cmd[2] == '0':
            raise InvalidCommandException('You cannot move from a cell to a cell.')

    if cmd[0] == '9':
        raise InvalidCommandException('You cannot move from the foundations.')

    if cmd[0] == cmd[1]:
        raise InvalidCommandException('The rows entered must differ.')


def attempt_move(cmd, board):
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


def print_help(window):
    window.addstr("Press 'u' to undo a move.\n")
    window.addstr("Press 'n' to deal a new game.\n")
    window.addstr("\n")

    window.addstr("Dark", curses.color_pair(3))
    window.addstr(" Cards", curses.color_pair(4))
    window.addstr(" :: ")
    window.addstr("Light", curses.color_pair(1))
    window.addstr(" Cards\n\n", curses.color_pair(2))

    window.addstr(" 67", curses.color_pair(5))
    window.addstr(" -> ")
    window.addstr("cascade 6", curses.color_pair(5))
    window.addstr(" to ")
    window.addstr("cascade 7\n", curses.color_pair(5))
    window.addstr(" 3", curses.color_pair(5))
    window.addstr("0", curses.color_pair(6))
    window.addstr(" -> ")
    window.addstr("cascade 3", curses.color_pair(5))
    window.addstr(" to  ")
    window.addstr("cells\n", curses.color_pair(6))
    window.addstr("03", curses.color_pair(6))
    window.addstr("2", curses.color_pair(5))
    window.addstr(" ->  ")
    window.addstr("cell 3", curses.color_pair(6))
    window.addstr("   to ")
    window.addstr("cascade 2\n\n", curses.color_pair(5))

    window.addstr(" 5", curses.color_pair(5))
    window.addstr("9", curses.color_pair(7))
    window.addstr(" -> ")
    window.addstr("cascade 5", curses.color_pair(5))
    window.addstr(" to ")
    window.addstr("foundations\n", curses.color_pair(7))
    window.addstr("01", curses.color_pair(6))
    window.addstr("9", curses.color_pair(7))
    window.addstr(" ->  ")
    window.addstr("cell 1", curses.color_pair(6))
    window.addstr("   to ")
    window.addstr("foundations", curses.color_pair(7))


curses.wrapper(main)
