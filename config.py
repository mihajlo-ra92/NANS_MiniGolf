import pygame
import numpy as np

#colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#movement constants
friction_coef = 0.997
min_velocity = 0.03

#ball constants
ball_colour = white
obs_ball_colour = red
obs_balls_number = 5
obs_ball_start = [(50, 262),(287,50),(430, 630),(220, 300),(220, 500)]

#rectangle constants
rectangle_colour = blue
rectangle_size = 20, 20
rectangle_number = 4
rectangle_start = [(50,200),(400,50),(220,400),(430,500)]
