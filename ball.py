import pygame
import numpy as np
import config

class Ball():
    #initialisation of ball, or constructor
    def __init__(self, is_main = False, pos = np.array([50.0, 650.0])):
        self.pos = pos
        self.velocity = np.array([0.0, 0.0])
        self.start = np.array([50.0, 650.0])
        self.mass = 10.0
        self.radius = 10.0
        self.is_main = is_main
    
    #gets force, turns it into velocity
    def apply_force(self, force, time = 1):
        #v = v0 + F/m * t
        self.velocity[0] += (force[0]/self.mass) * time
        self.velocity[1] += (force[1]/self.mass) * time
        #after we turn the force into velocity, we make 
        #it zero so it wouldnt affect the ball forever
        force = np.array([0.0, 0.0])

    #decreases the velocity because of the friction and changes the 
    #position because of the velocity
    def update(self):
        self.velocity *= config.friction_coef
        self.pos += self.velocity
        #if the velocity is under the minimum velocity, we stop the ball
        if self.velocity[0]**2 + self.velocity[1]**2 < config.min_velocity**2: 
            self.velocity = np.array([0.0, 0.0])