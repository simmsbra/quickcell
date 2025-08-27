class GameException(Exception):
    """Base class for exceptions relating to the game"""
    pass


class InvalidCommandException(GameException):
    """Raised when a move command does not conform to the game rules or command structure"""
    pass


class BoardException(GameException):
    """Base class for exceptions relating to the board"""
    pass


class EmptyOriginException(BoardException):
    """Raised when trying to remove a card from an empty row or cell"""
    pass


class FullDestinationException(BoardException):
    """Raised when trying to place a card into a full cell (or set of 4 full cells)"""
    pass


class CompatibilityException(BoardException):
    """Raised when trying to move a card or stack onto a cascade whose last card's value and suit do not allow it
       or when trying to move a card to the foundations too early
    """
    pass


class TooFewSlotsException(BoardException):
    """Raised when trying to move a stack that has too many cards to move given the number of empty cells and rows"""
    pass
