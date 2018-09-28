import curses
from cell import Cell


def display(window, board):

    # displays either the foundation bank or the cell bank
    def show_bank(bank):
        pos = window.getyx()
        for i, unit in enumerate(bank):
            window.move(pos[0] + i, pos[1])
            if i == 0:
                label = '0 ' if isinstance(unit, Cell) else '9 '
            elif i == 3:
                label = '┗ '
            else:
                label = '┃ '
            window.addstr(label)
            if isinstance(unit, Cell):
                show_cell(unit)
            else: # it's a foundation card
                show_card(unit)
        window.move(*pos)

    def show_cell(cell):
        if cell.card is None:
            window.addstr('•')
        else:
            show_card(cell.card)

    # display to screen; highlight if can move to foundations
    def show_card(card, highlight=False):
        suits = ['clubs', 'spades', 'hearts', 'diamonds']
        color = curses.color_pair(suits.index(card.suit) + 1)

        if card.rank == 0:
            symbols = '♣♠♥♦'
            char = symbols[suits.index(card.suit)]
        else:
            faces = 'A234567890JQK'
            char = faces[card.rank - 1]

        attr = color
        if highlight:
            attr = attr | curses.A_REVERSE

        window.addstr(char, attr)

    # show cascade, highlight cards that can move to foundations
    def show_cascade(cascade, founds):
        for card in cascade.cards:
            show_card(card, founds.should_accept(card))

    show_bank(board.cells)
    window.move(4, 0)
    show_bank(board.founds.founds)
    for i, cascade in enumerate(board.cascades):
        window.move(i, 3)
        window.addstr('  {} '.format(i + 1))
        show_cascade(cascade, board.founds)
    window.addstr('\n\nGame: {:6}\n'.format(board.seed))

# display a highlighted index (location) number for each cell
def show_cell_nums(window):
    pos = window.getyx()
    for i in range(4):
        window.addstr(i, 0, str(i + 1), curses.A_REVERSE)
    window.move(*pos)
