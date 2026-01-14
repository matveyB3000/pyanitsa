from card_type import CardType, CardRank
from random import shuffle
from card import Card
from typing import Optional

ALL_RANKS = list(CardRank)
ALL_TYPES = list(CardType)


class Deck:
    def __init__(self,minimal:CardRank=CardRank.SIX):
        self._all_cards = [Card(t,r,minimal) for t in ALL_TYPES for r in ALL_RANKS if r >= minimal]
        self.current_cards = list(self._all_cards)

    def shuffle(self):
        shuffle(self.current_cards)

    def get_card(self) -> Optional[Card]:
        if self.current_cards.__len__() > 0:
            return self.current_cards.pop(0)
        return None


if __name__ == "__main__":
    deck = Deck()
    print(deck._all_cards.__len__())
