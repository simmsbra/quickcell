from game_exception import EmptyOriginException, FullDestinationException


class Cell:
    def __init__(self):
        self.card = None

    def accept(self, card):
        if self.card is None:
            self.card = card
        else:
            raise FullDestinationException('This cell is occupied.')

    # return the card in self to see if it can be moved
    def view(self):
        if self.card is None:
            raise EmptyOriginException('This cell is empty.')
        return self.card

    def remove(self):
        self.view()
        self.card = None
