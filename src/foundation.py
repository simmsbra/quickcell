from card import Card
from game_exception import CompatibilityException


class Foundation:
    def __init__(self, suit):
        self.suit = suit
        self.card_stack = [Card(self.suit, 0)]

    def view_top_card(self):
        return self.card_stack[-1]

    # determine whether given card is in this foundation
    def contains(self, card):
        if self.suit is not card.suit:
            return False

        return self.card_stack[-1].rank >= card.rank

    # determine whether given card can be placed into this foundation
    def can_accept(self, card):
        return (card.suit == self.suit
                and card.rank == self.card_stack[-1].rank + 1)

    # place given card into this foundation
    def accept(self, card):
        if not self.can_accept(card):
            raise CompatibilityException('That card cannot move to this foundation yet.')
        self.card_stack.append(card)
