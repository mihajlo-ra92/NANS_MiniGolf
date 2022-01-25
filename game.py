import pygame
import numpy as np
from pygame import draw
import config
import ball
import line
import walls
import square

class Game:
    def __init__(self):
        #intialization of pygame
        pygame.init()

        #making the screen 600x700 and painting it black
        self.screen = pygame.display.set_mode((600, 700)) # (width, height)
        self.screen.fill(config.black)

        self.main_ball = ball.Ball(True)
        self.squares = self.create_squares()
        self.walls = walls.Walls()
        self.obs_balls, self.all_balls = self.create_obs_and_all_balls()
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

    def create_obs_and_all_balls(self):
        obs_balls = []
        all_balls = []
        for i in range(config.obs_balls_number):
            obs_balls.append(ball.Ball(False, config.obs_ball_start[i]))
            all_balls.append(ball.Ball(False, config.obs_ball_start[i]))
        all_balls.append(self.main_ball)
        return obs_balls, all_balls

    def create_squares(self):
        squares = []
        for i in range(config.squares_number):
            squares.append(square.Square(config.squares_centers[i]))
        return squares

    
    def draw_obs_balls(self):
        for i in range(config.obs_balls_number):
            pygame.draw.circle(self.screen, config.obs_ball_colour, self.obs_balls[i].pos, self.obs_balls[i].radius)
    
    def draw_squares(self):
        for i in range(config.squares_number):
            pygame.draw.polygon(self.screen, config.blue, self.squares[i].points)

    def draw_rectangle(self):
        for i in range(config.rectangle_number):
            pygame.draw.rect(self.screen, config.rectangle_colour, (config.rectangle_start[i], config.rectangle_size))

    def create_line_form_points(self,point1, point2):
        #line: a*y = b*x + c
        if point1[0] - point2[0] != 0:
                wallLineSlope = (point2[1] - point1[1]) / (point2[0] - point1[0]) #m = (y2 - y1)/(x2 - x1)
                wallLineA = 1.0
                wallLineB = wallLineSlope
                wallLineC = (-1) * wallLineSlope * point2[0] + point2[1]
        else:
            wallLineA = 0
            wallLineB = -1
            wallLineC = point1[0]
        return wallLineA, wallLineB, wallLineC

    def check_collision_ball_wall(self):
        #bice for loop koji prolazi kroz sve obs lopte
        # lin = []
        # for wallIt in self.walls.walls_list:
        #     for i in range(3):
        #         lin[i] = self.create_line_form_points(wallIt[i], wallIt[i+1])
        #     lin [3] = self.create_line_form_points(wallIt[3],wallIt[0])


        for wallIt in self.walls.walls_list:

            for i in range(4):
                p1Lin = wallIt[i]

                if i == 3:
                    p2Lin = wallIt[0]
                else:
                    p2Lin = wallIt[i+1]


                # p1Lin = np.array([15, 0])
                # p2Lin = np.array([15, 700])
                if p1Lin[0] == p2Lin[0]:
                    linLen = line.lineLenght(p1Lin, p2Lin)
                    dot = ((self.main_ball.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (self.main_ball.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                    closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                    closest = np.array([closestX, closestY])
                    if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                        circleLineDist = line.lineLenght(self.main_ball.pos, closest)
                        if circleLineDist <= self.main_ball.radius:
                            self.main_ball.velocity[0] *= (-1)
                            self.main_ball.update()

                    for obsBallIt in self.obs_balls:
                        dot = ((obsBallIt.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (obsBallIt.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            circleLineDist = line.lineLenght(obsBallIt.pos, closest)
                            if circleLineDist <= obsBallIt.radius:
                                obsBallIt.velocity[0] *= (-1)
                                obsBallIt.update()
                            
                    
                    # if line.pointOnLine(closest, p1Lin, p2Lin) != True:
                    #     return False
                    # circleLineDist = line.lineLenght(self.main_ball.pos, closest)
                    # if circleLineDist <= self.main_ball.radius:
                    #     self.main_ball.velocity[0] *= (-1)
                    #     self.main_ball.update()
                    #     return True

                if p1Lin[1] == p2Lin[1]:
                    linLen = line.lineLenght(p1Lin, p2Lin)
                    dot = ((self.main_ball.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (self.main_ball.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                    closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                    closest = np.array([closestX, closestY])
                    if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                        
                        circleLineDist = line.lineLenght(self.main_ball.pos, closest)
                        if circleLineDist <= self.main_ball.radius:
                            self.main_ball.velocity[1] *= (-1)
                            self.main_ball.update()
                        
                    for obsBallIt in self.obs_balls:
                        dot = ((obsBallIt.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (obsBallIt.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            circleLineDist = line.lineLenght(obsBallIt.pos, closest)
                            if circleLineDist <= obsBallIt.radius:
                                obsBallIt.velocity[1] *= (-1)
                                obsBallIt.update()

    #posle mozda stavim AABB(axis-aligned bounding box) check da ih ne poredi ako nisu ni blizu
    def check_collision_main_ball_obs_ball(self):
        for ballIt in self.obs_balls:
        # for i in range(config.obs_balls_number):
            distX = self.main_ball.pos[0] - ballIt.pos[0]
            distY = self.main_ball.pos[1] - ballIt.pos[1]
            distance = np.sqrt( distX**2 + distY**2)
            if distance <= self.main_ball.radius + ballIt.radius:
                
                # #normale
                # nx = (self.main_ball.pos[0] - ballIt.pos[0]) / distance
                # ny = (self.main_ball.pos[1] - ballIt.pos[1]) / distance
                # #tangente
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
                
                #the code above is not very good, somethimes the balls get stuck in eachother
                radiuses = self.main_ball.radius + ballIt.radius
                colision_distance = distance - radiuses

                collision_point_main_ball = np.array([0.0, 0.0])
                collision_point_main_ball[0] = (ballIt.pos[0] - self.main_ball.pos[0]) / distance * self.main_ball.radius
                collision_point_main_ball[1] = (ballIt.pos[1] - self.main_ball.pos[1]) / distance * self.main_ball.radius
                
                collision_point_ball_it = np.array([0.0, 0.0])
                collision_point_ball_it[0] = (self.main_ball.pos[0] - ballIt.pos[0]) / distance * ballIt.radius
                collision_point_ball_it[1] = (self.main_ball.pos[1] - ballIt.pos[1]) / distance * ballIt.radius

                reaction_vector_main_ball = np.array([0.0, 0.0])
                reaction_vector_main_ball[0] = (ballIt.pos[0] - self.main_ball.pos[0]) - collision_point_main_ball[0] + collision_point_ball_it[0]
                reaction_vector_main_ball[1] = (ballIt.pos[1] - self.main_ball.pos[1]) - collision_point_main_ball[1] + collision_point_ball_it[1]
                reaction_vector_ball_it = np.array([0.0, 0.0])
                reaction_vector_ball_it[0] = (self.main_ball.pos[0] - ballIt.pos[0] ) - collision_point_ball_it[0] + collision_point_main_ball[0]
                reaction_vector_ball_it[1] = (self.main_ball.pos[1] - ballIt.pos[1] ) - collision_point_ball_it[1] + collision_point_main_ball[1]

                self.main_ball.velocity = reaction_vector_main_ball
                ballIt.velocity = reaction_vector_ball_it
                self.update_obs_balls()

    def check_collision_obs_ball_obs_ball(self):
        for ballIt1 in self.obs_balls:
            for ballIt2 in self.obs_balls:
                if ballIt1 != ballIt2:
                    distX = ballIt1.pos[0] - ballIt2.pos[0]
                    distY = ballIt1.pos[1] - ballIt2.pos[1]
                    distance = np.sqrt( distX**2 + distY**2)
                    if distance <= ballIt1.radius + ballIt2.radius:      
                        # #normale
                        # nx = (ballIt1.pos[0] - ballIt2.pos[0]) / distance
                        # ny = (ballIt1.pos[1] - ballIt2.pos[1]) / distance
                        # #tangente
                        # tx = -ny
                        # ty = nx

                        # dpTan1 = ballIt1.velocity[0] * tx + ballIt1.velocity[1] * ty
                        # dpTan2 = ballIt2.velocity[0] * tx + ballIt2.velocity[1] * ty

                        # dpNorm1 = ballIt1.velocity[0] * nx + ballIt1.velocity[1] * ny
                        # dpNorm2 = ballIt2.velocity[0] * nx + ballIt2.velocity[1] * ny

                        # m1 = (dpNorm1 * (ballIt1.mass - ballIt2.mass) + 2 * ballIt2.mass * dpNorm2) / (ballIt1.mass + ballIt2.mass)
                        # m2 = (dpNorm2 * (ballIt2.mass - ballIt1.mass) + 2 * ballIt1.mass * dpNorm1) / (ballIt1.mass + ballIt2.mass)

                        # ballIt1.velocity[0] = tx * dpTan1 + nx * m1
                        # ballIt1.velocity[1] = ty * dpTan1 + ny * m1
                        # ballIt2.velocity[0] = tx * dpTan2 + nx * m2
                        # ballIt2.velocity[1] = ty * dpTan2 + ny * m2
                        # self.update_obs_balls()

                        radiuses = ballIt1.radius + ballIt2.radius
                        colision_distance = distance - radiuses

                        collision_point_ball1 = np.array([0.0, 0.0])
                        collision_point_ball1[0] = (ballIt2.pos[0] - ballIt1.pos[0]) / distance * ballIt1.radius
                        collision_point_ball1[1] = (ballIt2.pos[1] - ballIt1.pos[1]) / distance * ballIt1.radius
                        
                        collision_point_ball2 = np.array([0.0, 0.0])
                        collision_point_ball2[0] = (ballIt1.pos[0] - ballIt2.pos[0]) / distance * ballIt2.radius
                        collision_point_ball2[1] = (ballIt1.pos[1] - ballIt2.pos[1]) / distance * ballIt2.radius

                        reaction_vector_ball1 = np.array([0.0, 0.0])
                        reaction_vector_ball1[0] = (ballIt2.pos[0] - ballIt1.pos[0]) - collision_point_ball1[0] + collision_point_ball2[0]
                        reaction_vector_ball1[1] = (ballIt2.pos[1] - ballIt1.pos[1]) - collision_point_ball1[1] + collision_point_ball2[1]
                        reaction_vector_ball2 = np.array([0.0, 0.0])
                        reaction_vector_ball2[0] = (ballIt1.pos[0] - ballIt2.pos[0] ) - collision_point_ball2[0] + collision_point_ball1[0]
                        reaction_vector_ball2[1] = (ballIt1.pos[1] - ballIt2.pos[1] ) - collision_point_ball2[1] + collision_point_ball1[1]

                        ballIt1.velocity = reaction_vector_ball1
                        ballIt2.velocity = reaction_vector_ball2
                        self.update_obs_balls()

   


    def check_collision(self):
        self.check_collision_main_ball_obs_ball()
        self.check_collision_obs_ball_obs_ball()
        self.check_collision_ball_wall()
        # self.che


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

    def update_squares(self):
        for squareIt in self.squares:
            squareIt.update()