class BoardError(Exception):
    pass


class EmptyOriginError(BoardError):
    pass


class FullDestinationError(BoardError):
    pass


class CompatibilityError(BoardError):
    pass


class TooFewSlotsError(BoardError):
    pass
