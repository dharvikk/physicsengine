from menus import *
from physics import Rect
import numpy as np

RECT_PIXEL_WIDTH = 50
RECT_PIXEL_HEIGHT = 70
OBJECTIVE_PIXEL_WIDTH = 40
OBJECTIVE_PIXEL_HEIGHT = 40
class AnimationFrame(Frame):
    def __init__(self,app,rectPhysPosition,obj1,obj2,obj3,bottom_left,bottom_right,equation,delta_t):
        super().__init__(app)
        rect_bottom_left = rectPhysPosition - np.array([RECT_PIXEL_WIDTH/(self.widthScaleFactorToScreen*2), RECT_PIXEL_HEIGHT/(2*self.heightScaleFactorToScreen)])
        rect_bottom_right = rectPhysPosition + np.array([RECT_PIXEL_WIDTH/(self.widthScaleFactorToScreen*2), RECT_PIXEL_HEIGHT/(2*self.heightScaleFactorToScreen)])
        rect = Rect(rect_bottom_left,rect_bottom_right,RECT_PIXEL_HEIGHT/self.heightScaleFactorToScreen,"assets/Snowboard.png",self)
        obj1 = Button(self,
        self.convertToScreen(obj1) - np.array([OBJECTIVE_PIXEL_WIDTH/2,OBJECTIVE_PIXEL_HEIGHT/2]),(OBJECTIVE_PIXEL_WIDTH,OBJECTIVE_PIXEL_HEIGHT),"assets/submit.png")
        obj2 = Button(self,
        self.convertToScreen(obj2) - np.array([OBJECTIVE_PIXEL_WIDTH/2,OBJECTIVE_PIXEL_HEIGHT/2]),(OBJECTIVE_PIXEL_WIDTH,OBJECTIVE_PIXEL_HEIGHT),"assets/submit.png")
        obj3 = Button(self,
        self.convertToScreen(obj3) - np.array([OBJECTIVE_PIXEL_WIDTH/2,OBJECTIVE_PIXEL_HEIGHT/2]),(OBJECTIVE_PIXEL_WIDTH,OBJECTIVE_PIXEL_HEIGHT),"assets/submit.png")
        self.elements.append(rect)
        self.elements.append(obj1)
        self.elements.append(obj2)
        self.elements.append(obj3)
        self.objectives = [obj1,obj2,obj3]
        self.rect = rect
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.equation = equation
        self.equationSurface
        self.delta_t = delta_t
    def draw(self):
        super().draw()

    def convertToScreen(self,coords):
        return
    
    def convertToPhysics(self,coords):
        return
    
    @property
    def widthScaleFactorToScreen(self):
        pass

    @property
    def heightScaleFactorToScreen(self):
        pass
    #creates equation surface ready to blit
    def updateEquation(self):
        self.equationSurface = pygame.surface.Surface(self.app.pygameScreen.get_width(),self.app.pygameScreen.get_height())
        self.equationSurface.fill('white')
        self.equationSurface.set_colorkey("white")
        for i in range(10):
            points = []
            for j in range(self.app.pygameScreen.get_width()):
                x = self.convertToScreen([j,0])[0]
                y = self.equation.eval(x)
                points.append([x,y])
    def updateSystem(self):
        self.rect.update(self.equation,self.delta_t)