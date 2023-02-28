import pygame
import numpy as np
from vector_math import angle
from images import Image
class AnimationScreen:
    def __init__(self,screen_width,screen_height, max_y,min_y,max_x,min_x):
        self.screen_width = screen_width
        self.screen_height= screen_height
        self.max_y = max_y
        self.min_y = min_y
        self.max_x = max_x
        self.min_x = min_x
        self.player_image = Image("assets/Snowboard.png")
        self.background = None
    def convToScreen(self,point):
        x = point[0]
        y = point[1]
        scale_factor = self.screen_height/(self.max_y - self.min_y)
        new_y = self.screen_height - (y - self.min_y) * scale_factor
        new_x = (x - self.min_x) * scale_factor
        return [new_x,new_y]
    
    def drawEquation(self,equation,screen,color):
        if self.background is None:
            background = pygame.Surface((screen.get_width(),screen.get_height()))
            image =  pygame.Surface((screen.get_width(),screen.get_height()))
            snow_block = pygame.image.load("assets/Snow_block.png")
            for i in range(0,image.get_width(),snow_block.get_width()):
                for j in range(0,image.get_height(), snow_block.get_height()):
                    image.blit(snow_block,(i,j))
            background.fill(pygame.Color(0,0,0,255))

            for k in range(10):
                points = []
                for j in range(800):
                    i = (equation.upper - equation.lower) /800 * j  + equation.lower
                    points.append(self.convToScreen([i,equation.eval(i)]) + np.array([0,k]))
                pygame.draw.lines(background,"white",False,points)
            background.blit(image,(0,0),None,pygame.BLEND_RGB_MULT)
            self.background = background
        self.background.set_colorkey("black")
        screen.blit(self.background,(0,0))
    def drawRect(self,rect,screen,color):
        pygame.draw.polygon(screen,color,[self.convToScreen(rect.bottom_left),self.convToScreen(rect.bottom_right),
        self.convToScreen(rect.top_right),self.convToScreen(rect.top_left)])
        Image.drawOntoRect(self.player_image,rect,screen,self)
    
    @property
    def widthScale(self):
        return self.screen_width/(self.max_x  - self.min_x)
    
    @property
    def heightScale(self):
        return self.screen_width/(self.max_x  - self.min_x)