import pygame as p
import spritePro as s
from page_type import PageType
from message_bus import min_card_change
from config import MIN_CARD


def change_scene_game():
    s.debug_log("GAME", [255, 255, 255])
    s.scene.set_scene_by_name(PageType.GAME)


def test(**kwargs):
    s.debug_log("нажал", kwargs)


class Menu(s.Scene):
    def __init__(self):
        super().__init__()
        min_card_change.connect(self.min_card_change)
        min_card_change.connect(test)
        self.title_text = s.TextSprite(
            "Пьяница", 128, pos=(s.WH_C.x, 20), anchor=s.Anchor.MID_TOP, scene=self
        )
        self.author_text = s.TextSprite(
            "сделал Матвей Бабак",
            32,
            pos=(s.WH_C.x, s.WH.y - 20),
            anchor=s.Anchor.MID_BOTTOM,
            scene=self,
        )

        self.play_button = s.Button("", (200, 100), s.WH_C, "Играть", scene=self)
        self.play_button.set_rect_shape((200, 100), border_radius=12)

        self.min_card_buttons = [
            s.Button(
                "",
                (100, 50),
                (s.WH_C.x, s.WH_C.y + 200),
                "выше",
                scene=self,
                on_click=lambda: min_card_change.send(is_up=True),
            ),
            s.Button(
                "",
                (100, 50),
                (s.WH_C.x, s.WH_C.y + 300),
                "ниже",
                scene=self,
                on_click=lambda: min_card_change.send(is_up=False),
            ),
        ]
        self.min_card_text = s.TextSprite(
            "туз", 24, (255, 255, 255), (s.WH_C.x, s.WH_C.y + 250), scene=self
        )

        self.play_button.on_click(change_scene_game)

    def update(self, dt):
        self.min_card_text.text = f"{MIN_CARD.name}"

    def min_card_change(self, **kwargs):
        is_up = kwargs.get("is_up")
        s.debug_log(f"было {MIN_CARD.name}")
        MIN_CARD += 1 if is_up else -1
        s.debug_log(f"стало {MIN_CARD.name}")

    # def min_card_change(self, is_up: bool):
    #     s.debug_log(f"было {MIN_CARD.name}")
    #     MIN_CARD += 1 if is_up else -1
    #     s.debug_log(f"стало {MIN_CARD.name}")
