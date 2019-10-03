class Card:
    # rank :: integer with range [0, 13]
    #         Ace is 1; Jack, Queen, King are 11, 12, 13
    #         0 rank is for the base card of each foundation
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = 'black' if suit in ['clubs', 'spades'] else 'red'

    # check suit and value to determine whether can move onto given card
    def can_sit_on(self, card):
        return (card.rank == self.rank + 1
                and card.color != self.color)
