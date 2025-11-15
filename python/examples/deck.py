from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(i) for i in range(2,11)] + list('JQKA')
    suites = 'hearts diamonds clover spades'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in FrenchDeck.suites for rank in FrenchDeck.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __repr__(self):
        return f'Ranks: {self.ranks}, Suites: {self.suites}, Total Cards: {len(self._cards)}'



suit_values = dict(spades=3, hearts=2, diamonds=1, clover=0)

def spades_high(card: Card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

def print_sorted_deck(deck: FrenchDeck):
    for card in sorted(deck, key=spades_high):
        print(card)