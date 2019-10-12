import curses


def display_game(window, board):

    # displays either the foundation bank or the cell bank
    # where a "bank" is a group of 4 spots for cards or
    # stacks of cards
    def show_bank(bank, bank_type):
        pos = window.getyx()
        for i, unit in enumerate(bank):
            window.move(pos[0] + i, pos[1])
            if i == 0:
                label = '0 ' if bank_type == 'cells' else '9 '
            elif i == 3:
                label = '┗ '
            else:
                label = '┃ '
            window.addstr(label)
            if bank_type == 'cells':
                show_cell(unit)
            else: # it's a foundation
                foundation = bank[unit]
                show_card(foundation.view_top_card())
        window.move(*pos)

    def show_cell(cell):
        if cell.card is None:
            window.addstr('•')
        else:
            show_card(cell.card)

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
    def show_cascade(cascade, board):
        for card in cascade.cards:
            show_card(card, board.should_foundations_accept_card(card))

    show_bank(board.cells, 'cells')
    window.move(4, 0)
    show_bank(board.foundations, 'foundations')
    for i, cascade in enumerate(board.cascades):
        window.move(i, 3)
        window.addstr('  {} '.format(i + 1))
        show_cascade(cascade, board)
    window.addstr('\n\nGame: {:6}\n'.format(board.seed))

# display, in a vertical line, a highlighted index (location)
# number for each cell
def show_cell_nums(window):
    pos = window.getyx()
    for i in range(4):
        window.addstr(i, 0, str(i + 1), curses.A_REVERSE)
    window.move(*pos)
