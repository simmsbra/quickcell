import curses


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = 'black' if suit in ['clubs', 'spades'] else 'red'

    # display to screen; highlight if can move to foundations
    def show(self, window, highlight=False):
        suits = ['clubs', 'spades', 'hearts', 'diamonds']
        color = curses.color_pair(suits.index(self.suit) + 1)

        if self.rank == 0:
            symbols = '♣♠♥♦'
            char = symbols[suits.index(self.suit)]
        else:
            faces = 'A234567890JQK'
            char = faces[self.rank - 1]

        attr = color
        if highlight:
            attr = attr | curses.A_REVERSE

        window.addstr(char, attr)

    # check suit and value to determine whether can move onto given card
    def can_sit_on(self, card):
        return (card.rank == self.rank + 1
                and card.color != self.color)
