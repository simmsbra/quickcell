import curses
from card import Card

class Foundations:
    def __init__(self):
        self.founds = []
        for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
            self.founds.append(Card(suit, 0))

    def show(self, window):
        pos = window.getyx()
        for i, found in enumerate(self.founds):
            window.move(pos[0] + i, pos[1])
            label = '9 ' if i == 0 else '| '
            window.addstr(label)
            found.show(window)
        window.move(*pos)

    # determine whether given card can be placed into self
    def can_accept(self, card):
        for found in self.founds:
            if found.suit == card.suit:
                return found.rank == card.rank - 1
        return False

    # determine whether given card should be placed into self
    # if it is needed in the game board then this returns false
    def should_accept(self, card):
        if not self.can_accept(card):
            return False
        for found in self.founds:
            if found.color != card.color:
                if found.rank < card.rank - 2:
                    return False
            # I wrote this same-color, opposite-suit check after reading
            # http://solitairelaboratory.com/fcfaq.html
            # last question of section 2, about cards automatically moving home
            # Thank you Michael Keller
            elif found.suit != card.suit:
                if found.rank < card.rank - 3:
                    return False
        return True

    # place given card into self
    def accept(self, card):
        if not self.can_accept(card):
            raise Exception('That card cannot move to the foundations yet.')
        for i, found in enumerate(self.founds):
            if found.suit == card.suit:
                self.founds[i] = card
