from card import Card


class Cascade:
    def __init__(self, cards):
        self.cards = cards
        self.stack_index = self.calc_stack_index()

    def show(self, window, founds):
        for card in self.cards:
            card.show(window, founds)

    # place given card or stack of cards onto self
    def accept(self, stack):
        if type(stack) is not list:
            stack = [stack]
        if not self.can_accept(stack[0]):
            raise Exception('Those cards cannot sit on this cascade.')
        self.cards.extend(stack)
        self.stack_index = self.calc_stack_index()

    # determine whether given card can be placed onto self
    def can_accept(self, card):
        if self.is_empty():
            return True
        return card.can_sit_on(self.cards[-1])

    # return the card at index in self to see if it can be moved
    def view(self, index=-1):
        if len(self.cards) == 0:
            raise IndexError('You cannot remove a card from an empty cascade.')
        if index == -1:
            return self.cards[-1]
        else:
            return self.cards[index:]

    # remove a card or stack of cards at index from self
    def remove(self, index=-1):
        self.view(index)
        self.cards = self.cards[:index]
        self.stack_index = self.calc_stack_index()

    def is_empty(self):
        return len(self.cards) == 0

    # return the index of the top of self's stack of cards that can sit on each other
    # example: AA8732 would return the index of 3 if 3 and 2 were alternating colors
    def calc_stack_index(self):
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
