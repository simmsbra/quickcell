from random import randrange, Random

from card import Card
from cell import Cell
from cascade import Cascade, get_dependent_cards, is_dependent_card_of
from foundation import Foundation
from game_exception import EmptyOriginException, FullDestinationException, CompatibilityException, TooFewSlotsException


class Board:
    def __init__(self, seed=None):
        if seed is None:
            self.seed = randrange(1000000)
        else:
            self.seed = seed

        suits = ['clubs', 'spades', 'hearts', 'diamonds']
        deck = []
        for suit in suits:
            for rank in range(1, 14):
                deck.append(Card(suit, rank))
        Random(self.seed).shuffle(deck)

        # Fill the cascades with the shuffled deck of cards
        self.cascades = []
        place = 0
        for c in range(8):
            if c <= 3:
                end = place + 7
            else:
                end = place + 6
            self.cascades.append(Cascade(deck[place:end]))
            place = end

        self.foundations = {}
        for suit in suits:
            self.foundations[suit] = (Foundation(suit))

        self.cells = []
        for i in range(4):
            self.cells.append(Cell())

    def move(self, origin, destination):
        tmp = origin.view()
        destination.accept(tmp)
        origin.remove()

    def cell_to_foundations(self, index):
        card = self.cells[index].view()
        self.move(self.cells[index], self.foundations[card.suit])

    def cell_to_row(self, cell_index, row_index):
        self.move(self.cells[cell_index], self.cascades[row_index])

    def row_to_foundations(self, index):
        card = self.cascades[index].view()
        self.move(self.cascades[index], self.foundations[card.suit])

    def row_to_cell(self, index):
        for i, cell in enumerate(self.cells):
            try:
                self.move(self.cascades[index], self.cells[i])
                break
            except EmptyOriginException:
                raise
            except FullDestinationException:
                continue
        else:
            raise FullDestinationException('The cells are full.')

    def row_to_row(self, orig, dest):
        from_row = self.cascades[orig]
        to_row = self.cascades[dest]

        from_row.view()  # makes sure it's not empty

        movable_stack_index = from_row.movable_stack_index()
        if to_row.is_empty():
            for i in range(movable_stack_index, len(from_row.cards)):
                if (len(from_row.cards) - i) <= self.calc_move_capacity(to_row):
                    movable_stack_index = i
                    break
        else:
            for i in range(movable_stack_index, len(from_row.cards)):
                if is_dependent_card_of(from_row.cards[i], to_row.cards[-1]):
                    movable_stack_index = i
                    break
            else:
                raise CompatibilityException('The card(s) in the origin row cannot sit on the destination row.')
            if self.calc_move_capacity(to_row) < (len(from_row.cards) - movable_stack_index):
                raise TooFewSlotsException('There are not enough open slots to move that stack.')
        tmp = from_row.view(movable_stack_index)
        to_row.accept(tmp)
        from_row.remove(movable_stack_index)

    # return how big of a stack of cards can be moved to given cascade
    def calc_move_capacity(self, to_row):
        empty_cells = 0
        for cell in self.cells:
            if cell.card is None:
                empty_cells += 1
        empty_cascades = 0
        for cascade in self.cascades:
            if cascade.is_empty():
                empty_cascades += 1
        if to_row.is_empty():
            empty_cascades -= 1

        return (empty_cells + 1) * 2**empty_cascades

    def should_foundations_accept_card(self, card):
        # should not accept if cannot accept
        if not self.foundations[card.suit].can_accept(card):
            return False

        # accept only if none of the dependent cards may need to sit
        # in the cascades on the given card
        for dependent_card in get_dependent_cards(card):
            if (not self.foundations[dependent_card.suit].contains(dependent_card)
                and not self.should_foundations_accept_card(dependent_card)):
                return False
        return True

    # automatically move cards to the foundations that should move there
    def auto_move(self):
        while True:
            has_moved = False
            for i in range(len(self.cells)):
                try:
                    if self.should_foundations_accept_card(self.cells[i].view()):
                        self.cell_to_foundations(i)
                        has_moved = True
                except EmptyOriginException:
                    pass
            for i in range(len(self.cascades)):
                try:
                    if self.should_foundations_accept_card(self.cascades[i].view()):
                        self.row_to_foundations(i)
                        has_moved = True
                except EmptyOriginException:
                    pass
            if not has_moved:
                break
