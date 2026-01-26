from menu import Menu
from game import Game
import spritePro as s
import pygame as p
from enum import Enum, IntEnum
from typing import Dict
from base_page import BasePage
from message_bus import page_change
from page_type import PageType
from game_over import Game_over

class PageSwitcher:
    def __init__(self):
        page_change.connect(self.on_change)
        self.pages: Dict[PageType, BasePage] = {
            PageType.MENU: Menu(),
            PageType.GAME: Game(),
            PageType.GAME_OVER : Game_over()
        }
        self.switch(PageType.MENU)

    def switch(self,page:PageType):
        for i in self.pages :
            self.pages[i].set_active(False)
        self.pages[page].set_active(True)
        self.current = self.pages[page]
    
    def update(self):
        self.current.update()
    
    def on_change(self,sender,page):
        self.switch(page)



