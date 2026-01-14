from card_type import CardRank, CardType
from rx.subject import BehaviorSubject


class Card:
    def __init__(self, type, rank, minimal):
        self.type: CardType = type
        self.rank: CardRank = rank
        self._visibility: BehaviorSubject = BehaviorSubject(False)
        self.minimal_rank: CardRank = minimal

    @property
    def visibility(self):
        return self._visibility.value

    @visibility.setter
    def visibility(self, value):
        self._visibility.value = value
        self._visibility.on_next(self._visibility.value)

    def __eq__(self, value):
        return self.rank == value.rank

    def __ne__(self, value):
        return self.rank != value.rank

    def __gt__(self, value):
        if self._is_min_max(value):
            return self.rank < value.rank
        return self.rank > value.rank

    def __lt__(self, value):
        if self._is_min_max(value):
            return self.rank > value.rank
        return self.rank < value.rank

    def __str__(self):
        return f"Card({self.type.name}, {self.rank.name})"

    def __repr__(self):
        return self.__str__()

    def _is_min_max(self, value) -> bool:
        min_max = [self.minimal_rank, CardRank.ACE]
        if value.rank != self.rank:
            if value.rank in min_max and self.rank in min_max:
                return True
        return False


if __name__ == "__main__":
    card = Card(CardType.CLUBS, CardRank.ACE)
    card2 = Card(CardType.CLUBS, CardRank.KING)
    card3 = Card(CardType.HEARTS, CardRank.ACE)
    print(card == card3)
    print(card == card2)
    print(card > card2)
    print(card < card2)
    print(card)
