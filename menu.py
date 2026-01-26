import pygame as p
import spritePro as s
from page_type import PageType

def change_scene_game():
    s.debug_log("GAME",[255,255,255])
    s.scene.set_scene_by_name(PageType.GAME)

class Menu(s.Scene):
    def __init__(self):
        super().__init__()
        self.title_text = s.TextSprite(
            "Пьяница", 128, pos=(s.WH_C.x, 20), anchor=s.Anchor.MID_TOP,scene = self
        )
        self.author_text = s.TextSprite(
            "сделал Матвей Бабак", 32, pos=(s.WH_C.x,s.WH.y -20 ), anchor=s.Anchor.MID_BOTTOM,scene = self
        )

        self.play_button = s.Button("", (200, 100), s.WH_C, "Играть",scene = self)
        self.play_button.set_rect_shape((200, 100), border_radius=12)

        self.min_card_buttons = {}

        self.play_button.on_click(
            change_scene_game
        )

    def update(self,dt):
        pass
