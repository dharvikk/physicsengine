import pygame

class App:
    def __init__(self,pygameScreen):
        self.frames = {}
        self.current_frame = None
        self.pygameScreen = pygameScreen
    def draw(self):
        self.frames[self.current_frame].draw()
    
    def respond(self,event):
        self.frames[self.current_frame].respond(event)

class Frame:
    def __init__(self,app,name):
        self.elements =[]
        self.app = app
        self.app.frames[name] = self
    
    def draw(self):
        for element in self.elements:
            element.draw()
    
    def respond(self,event):
        for element in self.elements:
            element.respond(event)


class Button:
    def __init__(self,frame,position,dimensions,image = None):
        self.frame = frame
        self.position = position
        self.w = dimensions[0]
        self.h = dimensions[1]
        self.clicked = False
        self.frame.elements.append(self)

        if image is not None:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image,(self.w,self.h))
        else:
            self.image = None
    def draw(self):
        if self.image is not None:
            self.frame.app.pygameScreen.blit(self.image,self.position)

    def respond(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.position[0] < event.pos[0] and event.pos[0] < self.position[0] + self.w) and (self.position[1] < event.pos[1] and event.pos[1] < self.position[1] + self.h):
                self.clicked = True
            
                

class Text:
    def __init__(self,frame,position,dimensions,text,text_color,font,image = None,bg_color = None):
        self.frame = frame
        self.frame.elements.append(self)
        self.position = position
        self.dimensions = dimensions
        self.text = text
        self.font = font
        self.text_color = text_color
        self.clicked = False
        if image is not None:
            self.image = pygame.image.load(image)
            self.original_image = self.image
        else:
            if bg_color is not None:
                self.bg_color = bg_color
            else:
                self.bg_color = "white"
            self.image = None
        self.updateText()
    def updateText(self):
        if self.image is not None:
            text = self.font.render(self.text,None,self.text_color)
            if text.get_width() > self.dimensions[0]:
                self.image = pygame.transform.scale(self.original_image,(text.get_width(),text.get_height()))
            else:
                self.image = pygame.transform.scale(self.original_image,self.dimensions)
            self.surface_object = self.image.copy()
            self.surface_object.blit(text,(0,0))
        else:
            if self.bg_color is not None:
                self.surface_object = self.font.render(self.text,None,self.text_color,self.bg_color)
            else:
                self.surface_object = self.font.render(self.text,None,self.text_color)
            if self.surface_object.get_width() < self.dimensions[0]:
                background = pygame.surface.Surface(self.dimensions)
                background.fill(self.bg_color)
                background.blit(self.surface_object,(0,0))
                self.surface_object = background
    def draw(self):
        self.frame.app.pygameScreen.blit(self.surface_object,self.position)
    
    def respond(self,event):
        pass

class TextInput(Text):
    def __init__(self,frame,position,dimensions,text,text_color,font,image = None,bg_color = None,border_color = "black"):
        super().__init__(frame,position,dimensions,text,text_color,font,image,bg_color)
        self.border_color = border_color

    def respond(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.position[0] < event.pos[0] and event.pos[0] < self.position[0] + self.surface_object.get_width()) and (self.position[1] < event.pos[1] and event.pos[1] < self.position[1] + self.surface_object.get_height()):
                self.clicked = True
            
            else:
                self.clicked = False

        if event.type == pygame.KEYDOWN and self.clicked:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.updateText()
            
            elif event.key == pygame.K_RETURN:
                self.clicked = False
            else:
                self.text += event.unicode
                self.updateText()
    
    def draw(self):
        super().draw()
        if self.clicked:
            pygame.draw.rect(self.frame.app.pygameScreen,self.border_color,pygame.Rect(self.position[0],self.position[1],
            self.surface_object.get_width(),self.surface_object.get_height()),width = 2)

