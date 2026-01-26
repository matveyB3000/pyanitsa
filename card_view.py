import spritePro as s
from card import Card
from constant_sprites import RUBASHKA , get_sprite

class CardView(s.Sprite):
    def __init__(self,card:Card,pos = (0,0),scene:s.Scene = None):
        self.card = card
        self.image_rubashka = RUBASHKA
        self.image_card = get_sprite(card.rank,card.type)
        super().__init__(RUBASHKA,(102,154),pos,scene=scene)
        card._visibility.subscribe(self.set_visible)
        self.set_visible(False)
    
    def move(
        self, final_pos, delay: float = 0, visible_card: bool = True
    ):
        start_pos = self.position
        tween_move = s.Tween(
            start_pos,
            final_pos,
            0.7,
            s.EasingType.EASE_OUT,
            on_update=lambda pos: self.set_position(pos),
            delay=delay,
            on_complete=lambda: self.set_visible(visible_card),
        )

    def set_visible(self,value:bool):
        image = self.image_card if value else self.image_rubashka
        self.set_image(image)
        self.scale = 2 if value else 2.5
            

    