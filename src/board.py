from random import randrange, Random

from card import Card
from cell import Cell
from cascade import Cascade
from foundations import Foundations
from game_exception import EmptyOriginException, FullDestinationException, CompatibilityException, TooFewSlotsException


class Board:
    def __init__(self, seed=randrange(1000000)):
        self.seed = seed
        deck = []
        for suit in ['clubs', 'spades', 'hearts', 'diamonds']:
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

        self.founds = Foundations()
        self.cells = []
        for i in range(4):
            self.cells.append(Cell())

    def move(self, origin, destination):
        tmp = origin.view()
        destination.accept(tmp)
        origin.remove()

    def cell_to_foundations(self, index):
        self.move(self.cells[index], self.founds)

    def cell_to_row(self, cell_index, row_index):
        self.move(self.cells[cell_index], self.cascades[row_index])

    def row_to_foundations(self, index):
        self.move(self.cascades[index], self.founds)

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

        stack_index = from_row.stack_index()
        if to_row.is_empty():
            for i in range(stack_index, len(from_row.cards)):
                if (len(from_row.cards) - i) <= self.calc_move_capacity(to_row):
                    stack_index = i
                    break
        else:
            for i in range(stack_index, len(from_row.cards)):
                if from_row.cards[i].can_sit_on(to_row.cards[-1]):
                    stack_index = i
                    break
            else:
                raise CompatibilityException('The card(s) in the origin row cannot sit on the destination row.')
            if self.calc_move_capacity(to_row) < (len(from_row.cards) - stack_index):
                raise TooFewSlotsException('There are not enough open slots to move that stack.')
        tmp = from_row.view(stack_index)
        to_row.accept(tmp)
        from_row.remove(stack_index)

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

    # automatically move cards to the foundations that should move there
    def auto_move(self):
        while True:
            has_moved = False
            for i in range(len(self.cells)):
                try:
                    if self.founds.should_accept(self.cells[i].view()):
                        self.cell_to_foundations(i)
                        has_moved = True
                except EmptyOriginException:
                    pass
            for i in range(len(self.cascades)):
                try:
                    if self.founds.should_accept(self.cascades[i].view()):
                        self.row_to_foundations(i)
                        has_moved = True
                except EmptyOriginException:
                    pass
            if not has_moved:
                break
