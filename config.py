import pygame
import numpy as np

#colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#movement constants
friction_coef = 0.995
min_velocity = 0.09

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

#square constraints
square_width = 15
squares_number = 2
decoration_squares_number = 2
squares_centers = np.array([[220.0, 400.0], [150.0, 400.0]])
decoration_squares_centers = np.array([[215.0, 758.0], [370.0, 758.0]])

#wall
wall_width = 15.0

#wall corner squares
wall_corner_squares_number = 6
wall_corner_squares_centers = np.array([[85.0 + wall_width/2, 85.0 + wall_width/2], [500+wall_width/2, 85+wall_width/2], [500+wall_width/2, 600-wall_width/2], [330.0+wall_width/2, 200.0+wall_width/2], [280.0-wall_width/2, 700.0-wall_width/2], [330.0+wall_width/2, 700.0-wall_width/2]])
