import pygame
import numpy as np
from pygame import draw
import config
import ball
import walls

class Game:
    def __init__(self):
        #intialization of pygame
        pygame.init()

        #making the screen 600x700 and painting it black
        self.screen = pygame.display.set_mode((600, 700)) # (width, height)
        self.screen.fill(config.black)

        self.main_ball = ball.Ball(True)
        self.walls = walls.Walls()
        self.obs_balls = self.create_obs_bals()
        self.mouse_down = np.array([0.0, 0.0])
        self.mouse_up = np.array([0.0, 0.0])
        self.main_ball_clicked = False
        self.main_ball_force = np.array([0.0, 0.0])
        
        #title and icon
        pygame.display.set_caption("Mini golf")
        icon = pygame.image.load('golf.png')
        pygame.display.set_icon(icon)

    def draw_walls(self):
        for i in range(self.walls.walls_number):
            pygame.draw.polygon(self.screen, config.green, self.walls.walls_list[i])

    def draw_main_ball(self):
        pygame.draw.circle(self.screen, config.ball_colour, self.main_ball.pos, self.main_ball.radius)

    def create_obs_bals(self):
        obs_balls = []
        for i in range(config.obs_balls_number):
            obs_balls.append(ball.Ball(False, config.obs_ball_start[i]))
        return obs_balls

    def draw_obs_balls(self):
        for i in range(config.obs_balls_number):
            pygame.draw.circle(self.screen, config.obs_ball_colour, self.obs_balls[i].pos, self.obs_balls[i].radius)

    def draw_rectangle(self):
        for i in range(config.rectangle_number):
            pygame.draw.rect(self.screen, config.rectangle_colour, (config.rectangle_start[i], config.rectangle_size))


    # def check_collision(self):
    #     if self.main_ball.pos

    #this function only calculates the force applyed by our mouse
    def calculate_main_ball_force(self):
        self.main_ball_force = ((self.mouse_down[0] - self.mouse_up[0])/3, (self.mouse_down[1] - self.mouse_up[1])/3)

    def read_mouse_down(self, mouse_down_pos):
        self.mouse_down = mouse_down_pos

    def read_mouse_up(self, mouse_up_pos):
        self.mouse_up = mouse_up_pos

    #not used currently but maybe later
    def draw_all(self):
        self.draw_walls()
        self.draw_ball()

