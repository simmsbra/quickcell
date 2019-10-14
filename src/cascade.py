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
        return self.is_empty() or is_dependent_card_of(card, self.view())

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

    # return the index of the top of self's stack of cards that can sit on
    # each other and be moved as one unit
    # example: (bottom)AA8432(top) would return the index of 3 if 4, 3, and 2
    #                  012345
    # had alternating colors
    def movable_stack_index(self):
        if self.is_empty():
            return None

        if len(self.cards) == 1:
            return 0

        top_index = len(self.cards) - 1
        movable_stack_index = top_index
        # the child card is the card sitting on the parent card
        for parent_index in range(top_index - 1, -1, -1):
            child_index = parent_index + 1
            if is_dependent_card_of(self.cards[child_index],
                                    self.cards[parent_index]):
                movable_stack_index = parent_index
            else:
                break
        return movable_stack_index

def is_dependent_card_of(child_card, parent_card):
    for dependent_card in get_dependent_cards(parent_card):
        if dependent_card == child_card:
            return True

    return False

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
