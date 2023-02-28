import pygame

def drawRect(rect,screen,color):
    pygame.draw.polygon(screen,color,[rect.bottom_left,rect.bottom_right,rect.top_right,rect.top_left])

def drawEquation(equation,screen,color,width):
    points = []
    for i in range(equation.lower, equation.upper):
        points.append([i,equation.eval(i)])
    
    pygame.draw.lines(screen,color,False,points)
