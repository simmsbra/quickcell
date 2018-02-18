import curses

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if suit in ['hearts', 'diamonds']:
            self.color = 'red'
        else:
            self.color = 'black'

    # display to screen; highlight if can move to foundations
    def show(self, window, founds=None):
        suits = ['clubs', 'spades', 'hearts', 'diamonds']
        color = curses.color_pair(suits.index(self.suit) + 1)
        if self.rank == 0:
            symbols = '♣♠♥♦'
            char = symbols[suits.index(self.suit)]
        else:
            faces = 'A234567890JQK'
            char = faces[self.rank - 1]
        attr = color
        if (founds != None) and (founds.should_accept(self)):
            attr = attr | curses.A_REVERSE
        window.addstr(char, attr)

    # check suit and value to determine whether can move onto given card
    def can_sit_on(self, card):
        if self.rank != card.rank - 1:
            return False
        if self.color == card.color:
            return False
        return True
