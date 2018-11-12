class GameException(Exception):
    pass


class LetterCommandException(GameException):
    pass


class BoardException(GameException):
    pass


class EmptyOriginException(BoardException):
    pass


class FullDestinationException(BoardException):
    pass


class CompatibilityException(BoardException):
    pass


class TooFewSlotsException(BoardException):
    pass
