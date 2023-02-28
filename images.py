import pygame as py
from vector_math import angle
import numpy as np
class Image:
    def __init__(self, image):
        self.image = py.image.load(image)
    
    def drawOntoRect(self,rect,screen,game):
        new_image = py.transform.scale(self.image,(rect.width*game.widthScale,rect.height*game.heightScale))
        new_image = py.transform.rotate(new_image,-180/np.pi * angle(np.array([0,1]),rect.normal))
        screen.blit(new_image,game.convToScreen(rect.center) - np.array([new_image.get_width()/2,new_image.get_height()/2]))