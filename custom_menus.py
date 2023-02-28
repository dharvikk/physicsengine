from menus import *

class ScreenButton(Button):
    def __init__(self,frame,position,dimensions,next_screen,image = None):
        super().__init__(frame,position,dimensions,image)
        self.next_frame = next_screen

    def respond(self,event):
        super().respond(event)
        if self.clicked: 
            
            self.frame.app.current_frame = self.next_frame

            self.clicked = False


