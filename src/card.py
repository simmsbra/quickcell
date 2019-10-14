class Card:
    # rank :: integer with range [0, 13]
    #         Ace is 1; Jack, Queen, King are 11, 12, 13
    #         0 rank is for the base card of each foundation
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = 'black' if suit in ['clubs', 'spades'] else 'red'

    def __eq__(self, other):
        return (other.suit == self.suit
                and other.rank == self.rank
                and other.color == self.color)
