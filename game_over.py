import pygame as p
import spritePro as s
from base_page import BasePage
from message_bus import page_change
from page_type import PageType


class Game_over(s.Scene):
    def __init__(self):
        super().__init__()
        self.end_label = s.TextSprite(
            "ИГРА ОКОНЧЕНА",
            128,
            pos=(s.WH_C.x, 20),
            anchor=s.Anchor.MID_TOP,
            scene=self,
        )
        self.menu_button = s.Button("", (200, 100), s.WH_C, "В МЕНЮ", scene=self)
        self.menu_button.set_rect_shape((200, 100), border_radius=12)
