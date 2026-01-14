import pygame as p
import spritePro as s

class BasePage():
    def __init__(self):
        self.sprites_group = p.sprite.Group()

    def set_active(self,state:bool):
        for i in self.sprites_group:
            i.active = state