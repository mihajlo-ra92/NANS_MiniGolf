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

    def draw_aim_line(self):
        if self.main_ball_clicked:
            pygame.draw.line(self.screen, config.blue, self.main_ball.pos, pygame.mouse.get_pos(), 3)

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



    def check_collision_ball_wall(self):
        #bice for loop koji prolazi kroz sve obs lopte
        for wallIt in self.walls.walls_list:
            #line: a*y = b*x + c
            #vrv ce mi biti lakse da radim a*y + b*x + c = 0
            if wallIt[1][0] - wallIt[0][0] != 0:
                wallLineSlope = (wallIt[1][1] - wallIt[0][1]) / (wallIt[1][0] - wallIt[0][0]) #m = (y2 - y1)/(x2 - x1)
                wallLineA = 1.0
                wallLineB = wallLineSlope * (-1)
                wallLineC = wallLineSlope * wallIt[1][0] - wallIt[1][1]
            else:
                wallLineA = 0
                wallLineB = -1
                wallLineC = wallIt[0][0]*(-1)
            
            distance = (abs(wallLineA * self.main_ball.pos[0]) + (wallLineB * self.main_ball.pos[1] + wallLineC) / np.sqrt(wallLineA**2 + wallLineB**2))

            if self.main_ball.radius <= distance:
                self.main_ball.velocity = np.array([0.0, 0.0])

    #posle mozda stavim AABB(axis-aligned bounding box) check da ih ne poredi ako nisu ni blizu
    def check_collision_ball_ball(self):
        for ballIt in self.obs_balls:
        # for i in range(config.obs_balls_number):
            distX = self.main_ball.pos[0] - ballIt.pos[0]
            distY = self.main_ball.pos[1] - ballIt.pos[1]
            distance = np.sqrt( distX**2 + distY**2)
            if distance <= self.main_ball.radius + ballIt.radius:
                # self.main_ball.velocity = np.array([0.0, 0.0])
                # ballIt.velocity = np.array([0.0, 0.0])
                
                #normale
                nx = (self.main_ball.pos[0] - ballIt.pos[0]) / distance
                ny = (self.main_ball.pos[1] - ballIt.pos[1]) / distance
                #tangente
                # tx = -ny
                # ty = nx

                # dpTan1 = self.main_ball.velocity[0] * tx + self.main_ball.velocity[1] * ty
                # dpTan2 = ballIt.velocity[0] * tx + ballIt.velocity[1] * ty

                # dpNorm1 = self.main_ball.velocity[0] * nx + self.main_ball.velocity[1] * ny
                # dpNorm2 = ballIt.velocity[0] * nx + ballIt.velocity[1] * ny

                # m1 = (dpNorm1 * (self.main_ball.mass - ballIt.mass) + 2 * ballIt.mass * dpNorm2) / (self.main_ball.mass + ballIt.mass)
                # m2 = (dpNorm2 * (ballIt.mass - self.main_ball.mass) + 2 * self.main_ball.mass * dpNorm1) / (self.main_ball.mass + ballIt.mass)

                # self.main_ball.velocity[0] = tx * dpTan1 + nx * m1
                # self.main_ball.velocity[1] = ty * dpTan1 + ny * m1
                # ballIt.velocity[0] = tx * dpTan2 + nx * m2
                # ballIt.velocity[1] = ty * dpTan2 + ny * m2

                p = 2 * (self.main_ball.velocity[0] * nx + self.main_ball.velocity[1] * ny - 
                ballIt.velocity[0] * nx - ballIt.velocity[1] * ny) /(self.main_ball.mass + ballIt.mass)

                self.main_ball.velocity[0] -= p * self.main_ball.mass * nx
                self.main_ball.velocity[1] -= p * self.main_ball.mass * ny
                ballIt.velocity[0] -= p * ballIt.mass * nx
                ballIt.velocity[1] -= p * ballIt.mass * ny
                print(f'mainVelX = {self.main_ball.velocity[0]}\nmainVelY = {self.main_ball.velocity[1]}\nobsVelX = {ballIt.velocity[0]}\nobsVelY = {ballIt.velocity[1]}\n')

                # self.main_ball.velocity[0] = (self.main_ball.velocity[0] * (self.main_ball.mass - ballIt.mass) + (2 * ballIt.mass * ballIt.velocity[0])) / (self.main_ball.mass + ballIt.mass)
                # self.main_ball.velocity[1] = (self.main_ball.velocity[1] * (self.main_ball.mass - ballIt.mass) + (2 * ballIt.mass * ballIt.velocity[1])) / (self.main_ball.mass + ballIt.mass)
                # ballIt.velocity[0] = (ballIt.velocity[0] * (ballIt.mass - self.main_ball.mass) + (2 * self.main_ball.mass * ballIt.velocity[0])) / (self.main_ball.mass + ballIt.mass)
                # ballIt.velocity[1] = (ballIt.velocity[1] * (ballIt.mass - self.main_ball.mass) + (2 * self.main_ball.mass * ballIt.velocity[1])) / (self.main_ball.mass + ballIt.mass)


    def check_collision(self):
        # self.check_collision_ball_wall()
        self.check_collision_ball_ball()

    #this function only calculates the force applyed by our mouse
    def calculate_main_ball_force(self):
        #force is calculated from ball centre not mouse down point because it works better when we click the edge of the ball 
        # self.main_ball_force = ((self.mouse_down[0] - self.mouse_up[0])/3, (self.mouse_down[1] - self.mouse_up[1])/3)
        self.main_ball_force = ((self.main_ball.pos[0] - self.mouse_up[0])/3, (self.main_ball.pos[1] - self.mouse_up[1])/3)

    def read_mouse_down(self, mouse_down_pos):
        self.mouse_down = mouse_down_pos

    def read_mouse_up(self, mouse_up_pos):
        self.mouse_up = mouse_up_pos

    #not used currently but maybe later
    def draw_all(self):
        self.draw_walls()
        self.draw_ball()

    def update_obs_balls(self):
        for ballIt in self.obs_balls:
            ballIt.update()