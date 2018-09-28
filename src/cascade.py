from board_error import EmptyOriginError, CompatibilityError


class Cascade:
    def __init__(self, cards):
        self.cards = cards

    # place given card or stack of cards onto self
    def accept(self, stack):
        if not isinstance(stack, list):
            stack = [stack]
        if not self.can_accept(stack[0]):
            raise CompatibilityError('Those cards cannot sit on this cascade.')
        self.cards.extend(stack)

    # determine whether given card can be placed onto self
    def can_accept(self, card):
        return self.is_empty() or card.can_sit_on(self.cards[-1])

    # return the card at index in self to see if it can be moved
    def view(self, index=-1):
        if not self.cards:
            raise EmptyOriginError('You cannot remove a card from an empty cascade.')
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
