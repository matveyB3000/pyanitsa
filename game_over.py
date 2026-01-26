import pygame as p
import spritePro as s
from page_type import PageType

def change_scene_menu():
    s.debug_log("MENU",[255,255,255])
    s.scene.set_scene_by_name(PageType.MENU)

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
        self.menu_button.on_click(change_scene_menu)
        self.menu_button.set_rect_shape((200, 100), border_radius=12)
