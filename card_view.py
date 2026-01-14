import spritePro as s
from card import Card
from constant_sprites import RUBASHKA , get_sprite

class CardView(s.Sprite):
    def __init__(self,card:Card,pos = (0,0)):
        self.card = card
        self.image_rubashka = RUBASHKA
        self.image_card = get_sprite(card.rank,card.type)
        super().__init__(RUBASHKA,(102,154),pos)
        card._visibility.subscribe(self.set_visible)
        self.scale = 2
        

    def set_visible(self,value:bool):
        image = self.image_card if value else self.image_rubashka
        self.set_image(image)
            

    