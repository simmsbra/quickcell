from board_error import EmptyOriginError, FullDestinationError


class Cell:
    def __init__(self):
        self.card = None

    def show(self, window):
        if self.card is None:
            window.addstr('•')
        else:
            self.card.show(window)

    def accept(self, card):
        if self.card is None:
            self.card = card
        else:
            raise FullDestinationError('This cell is occupied.')

    # return the card in self to see if it can be moved
    def view(self):
        if self.card is None:
            raise EmptyOriginError('This cell is empty.')
        return self.card

    def remove(self):
        self.view()
        self.card = None
