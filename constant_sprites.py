from card import CardRank, CardType
import os

PATH = os.getcwd()
IMAGE_PATH = os.path.join(PATH, "images")
TYPE = {
    CardType.HEARTS: "0",
    CardType.SPADES: "1",
    CardType.DIAMONDS: "2",
    CardType.CLUBS: "3",
}
RANK = {
    CardRank.ACE: "0",
    CardRank.TWO: "1",
    CardRank.THREE: "2",
    CardRank.FOUR: "3",
    CardRank.FIVE: "4",
    CardRank.SIX: "5",
    CardRank.SEVEN: "6",
    CardRank.EIGHT: "7",
    CardRank.NINE: "8",
    CardRank.TEN: "9",
    CardRank.JACK: "10",
    CardRank.QUEEN: "11",
    CardRank.KING: "12",
}
RUBASHKA = "images/rubashka.png"

files = os.listdir(IMAGE_PATH)
file_images = {i: i for i in files}
file_images = {i: i.replace(".png", "").split("_") for i in file_images}
file_images = {
    tuple(file_images[i][2:]): i for i in file_images if file_images[i].__len__() == 4
}


def get_sprite(rank: CardRank, type: CardType) -> str:
    """привязывает нужную картинку к карте"""

    r = RANK[rank]
    t = TYPE[type]
    return "images/" + file_images[(t, r)]
