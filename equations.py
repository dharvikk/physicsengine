import numpy as np
from scipy.optimize import brentq
from scipy.optimize import minimize_scalar
from scipy.misc import derivative
from vector_math import signof
class GeneralEquation:

    def __init__(self,f,args,domain = None):
        self.f = f
        self.args = args
        if domain is not None:
            self.lower = domain[0]
            self.upper = domain[1]
            return
        self.lower = -np.inf
        self.upper = np.inf
    def eval(self,x):
        return self.f(x,*self.args)
    
    #returns the ideal vector that lies on the graph
    def find_ideal_vector(self,pivot,other_point):
        self.x1 = pivot[0]
        self.y1 = pivot[1]
        self.length = np.linalg.norm(other_point - pivot)
        vec_between = other_point - pivot
        best_x = brentq(self.ideal_vector_minimization_func,pivot[0],other_point[0] + signof(vec_between[0]) * 1.5*self.length,maxiter = 100)

        return np.array([best_x,self.eval(best_x)])

    #returns point of collision and None if there is no collision
    def collision(self,rect,tolerance):
        if rect.bottom_left[0] > self.upper or rect.bottom_right[0] < self.lower:
            return None
        if self.distance(rect.bottom_left) <= tolerance:
            return rect.bottom_left
        if self.distance(rect.bottom_right) <= tolerance:
            return rect.bottom_right
        if rect.pivot is not None:
            if (self.distance(rect.pivot) <= tolerance):
                return rect.pivot
        self.m = (rect.bottom_right[1] - rect.bottom_left[1])/ (rect.bottom_right[0] - rect.bottom_left[0])
        self.b = rect.bottom_right[1] - self.m*rect.bottom_right[0]
        collision_x = minimize_scalar(self.collision_minimization_func,method = "bounded",bounds =  [rect.bottom_left[0],rect.bottom_right[0]]).x

        if self.collision_minimization_func(collision_x) < tolerance:
            return np.array([collision_x,self.eval(collision_x)])

        return None
    #returns a boolean that represents where the top two points of the rect are colliding
    def top_collision(self,rect,tolerance):
        if rect.top_left[0] > self.upper or rect.top_right[0] < self.lower:
            return None
        if self.distance(rect.top_left) <= tolerance:
            return True
        if self.distance(rect.top_right) <= tolerance:
            return True
        
        self.m = (rect.top_right[1] - rect.top_left[1])/ (rect.top_right[0] - rect.top_left[0])
        self.b = rect.top_right[1] - self.m*rect.top_right[0]
        collision_x = minimize_scalar(self.collision_minimization_func,method = "bounded",bounds =  [rect.top_left[0],rect.top_right[0]]).x

        if self.collision_minimization_func(collision_x) < tolerance:
            return True

        return False
    #returns the tangent vector at a point
    def tangent_vector(self,vector):
        vec = np.array([1,derivative(self.eval,vector[0])])
        return vec / np.linalg.norm(vec)
    
    def distance(self,point):
        return np.abs(point[1] - self.eval(point[0]))

    def ideal_vector_minimization_func(self,x):
        return np.sqrt((self.x1-x)**2 + (self.y1 - self.eval(x))**2) - self.length
    
    def collision_minimization_func(self,x):
        return np.abs(self.eval(x) - self.m *x - self.b)