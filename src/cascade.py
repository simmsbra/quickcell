from game_exception import EmptyOriginException, CompatibilityException
from card import Card


class Cascade:
    def __init__(self, cards):
        self.cards = cards

    # place given card or stack of cards onto self
    def accept(self, stack):
        if not isinstance(stack, list):
            stack = [stack]
        if not self.can_accept(stack[0]):
            raise CompatibilityException('Those cards cannot sit on this cascade.')
        self.cards.extend(stack)

    # determine whether given card can be placed onto self
    def can_accept(self, card):
        return self.is_empty() or card.can_sit_on(self.cards[-1])

    # return the card at index in self to see if it can be moved
    def view(self, index=-1):
        if not self.cards:
            raise EmptyOriginException('You cannot remove a card from an empty cascade.')
        if index == -1:
            return self.cards[-1]
        return self.cards[index:]

    # remove a card or stack of cards at index from self
    def remove(self, index=-1):
        self.view(index)
        self.cards = self.cards[:index]

    def is_empty(self):
        return len(self.cards) == 0

    # return the index of the top of self's stack of cards that can sit on each other
    # example: AA8732 would return the index of 3 if 3 and 2 were alternating colors
    def stack_index(self):
        if self.is_empty():
            return None
        last = len(self.cards) - 1
        index = last
        for i in range(last - 1, -1, -1):
            if self.cards[i + 1].can_sit_on(self.cards[i]):
                index = i
            else:
                break
        return index

# returns the cards (either 0 or 2 of them) that can be moved
# onto the given card
# for example: 4 of clubs returns 3 of hearts and 3 of diamonds
def get_dependent_cards(card):
    if card.rank <= 1:
        return []
    else:
        if card.color == 'black':
            opposite_colored_suits = ['hearts', 'diamonds']
        else:
            opposite_colored_suits = ['clubs', 'spades']

        return [Card(opposite_colored_suits[0], card.rank - 1),
                Card(opposite_colored_suits[1], card.rank - 1)]
