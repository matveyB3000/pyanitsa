import spritePro as s
import constant_sprites
from game import Game
from pages import PageSwitcher

s.get_screen((1000, 1000), "пьяница", "icon.jpg")
page_switcher = PageSwitcher()
# s.enable_debug(True)
while True:
    s.update(fill_color=(85, 89, 145))
    page_switcher.update()
