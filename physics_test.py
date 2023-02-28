
import pygame
from physics import Rect, PhysicsObject
import numpy as np
from physics_visual import drawRect, drawEquation
from vector_math import angle
from equations import GeneralEquation
from coordinates import AnimationScreen
from menus import *
from custom_menus import *
def quadratic(x,a,b,c):
    return a*x*x + b*x + c
def sine(x,a,b,c,d):
    return a*np.sin(b*(x+c)) + d
def vector_form(x,a,k,h):
    return a*(x-k)**2 + h
def absolute(x,a,b,c):
    return a*abs(x-b)+c
def linear(x,m,b):
    return m*x+b
def constant(x,a):
    return a
equation = GeneralEquation(vector_form,[0.8,0,-1],[-5,5])
rect = Rect(np.array([-1.0,0.0]),np.array([-0.5,0.0]),0.75)
physicsObj = PhysicsObject(rect,np.array([0.0,-0.1]),0.01)
#global variables for the project
WIDTH = 800
HEIGHT = 800
debug = False
BG_COLOR = pygame.Color(255,255,255,255)

coords = AnimationScreen(WIDTH,HEIGHT,10,-10,10,-10)
#all the pygame necessary set up
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(BG_COLOR)
running = True
clock = pygame.time.Clock()


default_font = pygame.font.SysFont("comicsans", 40)

myApp = App(screen)
myApp.current_frame = "Menu"
menuFrame = Frame(myApp,"Menu")
otherFrame = Frame(myApp,"Game")

print(myApp.frames.keys())
playButton = ScreenButton(menuFrame,(350,350),(100,100),"Game","assets/play.png")

submitButton = ScreenButton(otherFrame,(0,400),(120,50),"Menu","assets/submit.png")
slopeInput = TextInput(otherFrame,(50,100),(100,50),"Enter slope here","white",default_font,bg_color = "light gray",border_color ="black")
interceptInput = TextInput(otherFrame,(50,200),(100,50),"Enter y intercept here","white",default_font,bg_color = "light gray",border_color = "black")
while(running):
    #makes sure the game runs at 60 fps
    clock.tick(120)
    screen.fill(BG_COLOR)
    # for i in range(10):
    #     physicsObj.update(equation,0.15/10)
    # coords.drawEquation(equation,screen,"gray")
    # coords.drawRect(rect,screen,"gray")
    myApp.draw()
    if debug == True:
        try:
            pygame.draw.circle(screen,"red",coords.convToScreen(rect.pivot),10)
        except:
            pass
        try:
            pygame.draw.line(screen,"yellow",coords.convToScreen(physicsObj.rect.pivot),coords.convToScreen(physicsObj.rect.pivot+physicsObj.ideal_vector))
        except:
            pass

        try:
            pygame.draw.line(screen,"red",coords.convToScreen(physicsObj.rect.pivot),coords.convToScreen(physicsObj.rect.pivot+physicsObj.current_vector))
        except:
            pass
        try:
            pygame.draw.line(screen,"blue",physicsObj.rect.pivot,physicsObj.rect.pivot+physicsObj.velocity)
        except:
            pass

    #makes a bunch of calls to calculate all and update position
    #basically is supposed to make it more precise
    #checks if the user pressed the quit button
    for event in pygame.event.get():
        myApp.respond(event)
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()