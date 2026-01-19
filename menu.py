import pygame as p
import spritePro as s
from base_page import BasePage
from message_bus import page_change
from page_type import PageType


class Menu(BasePage):
    def __init__(self):
        super().__init__()
        self.title_text = s.TextSprite(
            "Пьяница", 128, pos=(s.WH_C.x, 20), anchor=s.Anchor.MID_TOP
        )
        self.sprites_group.add(self.title_text)
        self.play_button = s.Button("", (200, 100), s.WH_C, "Играть")
        self.sprites_group.add(self.play_button)
        self.play_button.on_click(lambda: page_change.send("ANY", page=PageType.GAME))

    def update(self):
        pass
