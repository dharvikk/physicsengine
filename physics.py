import numpy as np
import sys
from vector_math import rotate,signof,angle
from images import Image
RIGHT = 1
LEFT = 2
class Rect:
    def __init__(self,bottom_left,bottom_right,height,image,frame):
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.pivot = None
        self.height = height
        self.width = np.linalg.norm(bottom_left - bottom_right)
        self.pivot_side = None
        self.image = Image(image)
        self.frame = frame
    def move_newpivot(self,new_pivot):
        self.bottom_left = self.bottom_left - self.pivot + new_pivot
        self.bottom_right = self.bottom_right - self.pivot + new_pivot
        self.pivot = new_pivot
    
    def rotate(self,angle):
        self.bottom_left = rotate(self.bottom_left - self.pivot,angle) + self.pivot
        self.bottom_right = rotate(self.bottom_right - self.pivot,angle) + self.pivot
    
    def move_vector(self,vector):
        self.bottom_left += vector
        self.bottom_right += vector
        # if self.pivot is not None:
        #     self.pivot += vector

    def draw(self):
        self.image.drawOntoRect(self,self.frame.app.pygameScreen,self.frame)
    @property
    def lower_center(self):
        return  (self.bottom_left + self.bottom_right)/2
    @property
    def tangent(self):
        return (self.bottom_right - self.bottom_left)/self.width
    @property
    def normal(self):
        return -np.array([self.tangent[1],-self.tangent[0]])
    @property
    def top_right(self):
        return self.lower_center + self.normal*self.height + self.tangent*self.width/2
    @property
    def top_left(self):
        return self.lower_center + self.normal*self.height - self.tangent*self.width/2

    @property
    def center(self):
        return (self.top_right + self.top_left + self.bottom_left + self.bottom_right)/4

class PhysicsObject:
    def __init__(self,rect,gravity,tolerance):
        self.gravity = gravity
        self.tolerance = tolerance
        self.rect = rect
        self.velocity = np.array([0.0,0.0])
        self.freefall = True
        self.sliding = False
        self.stuck = False
        self.locked = False
    def update(self,equation,delta_t):
        self.updateState(equation)

        if (self.stuck):
            return

        if (self.freefall):
            self.updateFreefall(equation,delta_t)
        
        elif (self.sliding):
            self.updateSliding(equation,delta_t)
    

    def updateState(self,equation):
        if equation.top_collision(self.rect,self.tolerance) == True:
            self.stuck = True

        collisionPoint = equation.collision(self.rect,self.tolerance)

        if collisionPoint is None:
            if self.sliding:
                self.sliding = False
                self.freefall = True
                print("BADF THINGS HAPPENING")
        else:
            if self.freefall:

                self.sliding = True
                self.rect.pivot = collisionPoint
    
                if np.linalg.norm(self.rect.bottom_left - self.rect.pivot) < np.linalg.norm(self.rect.bottom_right - self.rect.pivot):
                    self.rect.pivot_side = LEFT
                elif np.linalg.norm(self.rect.bottom_left - self.rect.pivot) > np.linalg.norm(self.rect.bottom_right - self.rect.pivot):
                    self.rect.pivot_side = RIGHT
                else:
                    self.rect.pivot_side = None

                self.sliding = True
                self.freefall = False
                #we need to also adjust the velocity so it doesnt look unrealistic
                tangent_pivot = equation.tangent_vector(self.rect.lower_center)
                self.velocity = tangent_pivot * np.dot(self.velocity,tangent_pivot)
    def updateVelocity(self,equation,delta_t):
        if self.freefall:
            self.velocity += self.gravity * delta_t
        
        else:
            tangent_pivot = equation.tangent_vector(self.rect.pivot)
            tangent_center = equation.tangent_vector(self.rect.lower_center)
            self.velocity = np.linalg.norm(self.velocity) * tangent_center * signof(np.dot(self.velocity,tangent_center))
            self.velocity += np.dot(self.gravity,tangent_center) * tangent_center * delta_t
    
    def slidePivot(self,equation,delta_t):
        #addition factor
        delta_x = self.velocity[0] * delta_t
        normal_shift = np.linalg.norm(delta_x * self.rect.tangent / self.rect.tangent[0])
        if self.rect.pivot_side  == LEFT:
            #now we just create the vector by which we want to shift by
            unit_shift = self.rect.pivot - self.rect.bottom_left
        elif self.rect.pivot_side == RIGHT:
            unit_shift = self.rect.pivot - self.rect.bottom_right 
        
        else:
            return
        radius = np.linalg.norm(unit_shift)
        if radius == 0:
            return
        unit_shift = unit_shift /radius
        self.rect.move_vector(min(normal_shift,radius) * unit_shift)
    def rotateBlock(self,equation,delta_t):
        # now we just have to write the code to make the block rotate smoothly
        # should be fairly easy, we first need to figure out the vector we are trying to match
        if (self.rect.pivot_side== LEFT):
            current_vector = self.rect.bottom_right - self.rect.pivot
            ideal_vector = equation.find_ideal_vector(self.rect.pivot,self.rect.bottom_right) - self.rect.pivot
            radius = np.linalg.norm(current_vector)

        if (self.rect.pivot_side == RIGHT):
            current_vector = self.rect.bottom_left - self.rect.pivot
            ideal_vector = equation.find_ideal_vector(self.rect.pivot,self.rect.bottom_left) - self.rect.pivot
            radius = np.linalg.norm(current_vector)
        self.ideal_vector = ideal_vector
        # we also very quickly calculate the delta theta
        delta_theta = np.linalg.norm(self.velocity) * delta_t/radius
        self.current_vector=  current_vector
        snap_angle = angle(-current_vector,ideal_vector)
        # we decide whether to rotate by delta theta, or to snap in place

        if (abs(snap_angle) < abs(delta_theta)):
            if (self.rect.pivot_side == RIGHT):
                self.rect.bottom_left = ideal_vector + self.rect.pivot
            elif self.rect.pivot_side == LEFT:
                self.rect.bottom_right = ideal_vector + self.rect.pivot
        elif (snap_angle < 0 and self.rect.pivot_side == RIGHT):
            self.rect.bottom_left = ideal_vector + self.rect.pivot
        elif (snap_angle>0 and self.rect.pivot_side == LEFT):
            self.rect.bottom_right = ideal_vector + self.rect.pivot
        else:
            self.rect.rotate(-abs(delta_theta) * signof(snap_angle))
    def updateFreefall(self,equation,delta_t):
        self.updateVelocity(equation,delta_t)
        self.rect.move_vector(self.velocity*delta_t)

    def updateSliding(self,equation,delta_t):
        self.updateVelocity(equation,delta_t)
        delta_x = self.velocity[0] * delta_t
        new_pivot = np.array([self.rect.pivot[0] + delta_x, equation.eval(self.rect.pivot[0] + delta_x) ])

        self.rect.move_newpivot(new_pivot)
        self.slidePivot(equation,delta_t)
        self.rotateBlock(equation,delta_t)