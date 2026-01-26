import spritePro as s
import pygame as p
from game import Game
from menu import Menu
from game_over import Game_over
from page_type import PageType

def create_scenes():
    s.scene.add_scene(PageType.GAME,Game)
    s.scene.add_scene(PageType.MENU,Menu)
    s.scene.add_scene(PageType.GAME_OVER,Game_over)
    s.scene.set_scene_by_name(PageType.MENU)




