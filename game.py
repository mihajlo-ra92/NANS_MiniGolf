from email import message
import math
import pygame
import numpy as np
from pygame import draw
import config
import ball
import line
# from sat import sat_polygon_circle, sat_two_polygons, dot
import sat
import walls
import square
import sys

class Game:
    def __init__(self):
        #intialization of pygame
        pygame.init()

        #making the screen 600x800 and painting it black
        self.screen = pygame.display.set_mode((600, 800)) # (width, height)
        self.screen.fill(config.black)

        self.main_ball = ball.Ball(True)
        self.squares = self.create_squares()
        self.decoration_squares = self.create_decoration_squares()
        self.walls = walls.Walls()
        self.obs_balls, self.all_balls = self.create_obs_and_all_balls()
        self.mouse_down = np.array([0.0, 0.0])
        self.mouse_up = np.array([0.0, 0.0])
        self.main_ball_clicked = False
        self.main_ball_force = np.array([0.0, 0.0])
        self.score = 0
        self.game_over = False
        self.wall_corner_squares = self.create_wall_corner_squares()
        
        #title and icon
        pygame.display.set_caption("Mini golf")
        icon = pygame.image.load('golf.png')
        pygame.display.set_icon(icon)


    def draw_walls(self):
        for i in range(self.walls.walls_number):
            pygame.draw.polygon(self.screen, config.green, self.walls.walls_list[i].points)

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

    def create_wall_corner_squares(self):
        squares = []
        for i in range(config.wall_corner_squares_number):
            squares.append(square.Square(config.wall_corner_squares_centers[i], 0, config.wall_width/2.0))
        # for i in range(config.wall_corner_squares_number):
        #     squares[i].center = np.array([15.0, 15.0])#config.wall_corner_squares_centers[i]
        return squares

    def create_decoration_squares(self):
        decoration_squares = []
        for i in range(config.decoration_squares_number):
            decoration_squares.append(square.Square(config.decoration_squares_centers[i], 1.3))
        return decoration_squares
    
    def draw_decoration_squares(self):
        for i in range(config.decoration_squares_number):
            pygame.draw.polygon(self.screen, config.white, self.decoration_squares[i].points)

    def draw_obs_balls(self):
        for i in range(config.obs_balls_number):
            pygame.draw.circle(self.screen, config.obs_ball_colour, self.obs_balls[i].pos, self.obs_balls[i].radius)
    
    def draw_squares(self):
        for i in range(config.squares_number):
            pygame.draw.polygon(self.screen, config.blue, self.squares[i].points)

    def draw_wall_corner_squares(self):
        for i in range(config.wall_corner_squares_number):
            pygame.draw.polygon(self.screen, config.blue, self.wall_corner_squares[i].points)
    # def draw_rectangle(self):
    #     for i in range(config.rectangle_number):
    #         pygame.draw.rect(self.screen, config.rectangle_colour, (config.rectangle_start[i], config.rectangle_size))

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

    def check_collision_all_wall(self):

        for wall_it in self.walls.walls_list:

            



            # is_coliding,_,_ = sat.sat_polygon_circle(self.main_ball, wall_it)
            # if is_coliding:
            #     # print("ZID")
            #     #trazicemo dve najblize tacke pa cemo onda gledati da li su one uspravne ili vodoravne
            #     first_closest = wall_it.points[0]
            #     second_closest = wall_it.points[0]
            #     for point_it in wall_it.points:
            #         # (self.main_ball.pos[0] - point_it[0])**2 + (self.main_ball.pos[1] - point_it[1])**2 < (self.main_ball.pos[0] - first_closest[0])**2 + (self.main_ball.pos[1] - first_closest[1])**2
            #         if (self.main_ball.pos[0] - point_it[0])**2 + (self.main_ball.pos[1] - point_it[1])**2 < (self.main_ball.pos[0] - first_closest[0])**2 + (self.main_ball.pos[1] - first_closest[1])**2:
            #             first_closest = point_it

            #     for point_it in wall_it.points:  
            #         # if point_it != first_closest:
            #         if (self.main_ball.pos[0] - point_it[0])**2 + (self.main_ball.pos[1] - point_it[1])**2 < (self.main_ball.pos[0] - second_closest[0])**2 + (self.main_ball.pos[1] - second_closest[1])**2 and point_it[0] != first_closest[0] and point_it[1] != first_closest[1]:
            #             second_closest = point_it

            #     #ako su "uspravni"
            #     if first_closest[0] == second_closest[0]:
            #         self.main_ball.velocity[0] *= (-1)
            #         self.main_ball.update()

            #     #ako su "vodoravni"
            #     if first_closest[1] == second_closest[1]:
            #         self.main_ball.velocity[1] *= (-1)
            #         self.main_ball.update()



            for i in range(4):
                p1Lin = wall_it.points[i]

                if i == 3:
                    p2Lin = wall_it.points[0]
                else:
                    p2Lin = wall_it.points[i+1]


                #ako su im x-evi isti, tj. ako je "uspravan" zid
                if p1Lin[0] == p2Lin[0]:
                    linLen = line.lineLenght(p1Lin, p2Lin)
                    dot = ((self.main_ball.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (self.main_ball.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                    closestX, closestY = line.findClosest(dot, p1Lin, p2Lin)
                    closest = np.array([closestX, closestY])
                    if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                        circleLineDist = line.lineLenght(self.main_ball.pos, closest)
                        if circleLineDist <= self.main_ball.radius:
                            self.main_ball.velocity[0] *= (-0.8)
                            self.main_ball.update()

                    for obsBallIt in self.obs_balls:
                        dot = ((obsBallIt.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (obsBallIt.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            circleLineDist = line.lineLenght(obsBallIt.pos, closest)
                            if circleLineDist <= obsBallIt.radius:
                                obsBallIt.velocity[0] *= (-0.8)
                                obsBallIt.update()
                            
                    for square_it in self.squares:
                        # square_wall_col,_,_ = sat.sat_two_polygons(square_it.points, wall_it.points)
                        # if square_wall_col:
                        #     square_it.velocity[0] *= -0.8
                        #     square_it.update()

                        dot = ((square_it.center[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (square_it.center[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            squareLineDist = line.lineLenght(square_it.center, closest)
                            if squareLineDist <= config.square_width:
                                square_it.velocity[0] *= -0.8
                                square_it.update()
                            
                    

                #ako su im y-evi isti, tj. ako je "lezeci" zid
                if p1Lin[1] == p2Lin[1]:
                    linLen = line.lineLenght(p1Lin, p2Lin)
                    dot = ((self.main_ball.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (self.main_ball.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                    closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                    closest = np.array([closestX, closestY])
                    if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                        
                        circleLineDist = line.lineLenght(self.main_ball.pos, closest)
                        if circleLineDist <= self.main_ball.radius:
                            self.main_ball.velocity[1] *= (-0.8)
                            self.main_ball.update()
                        
                    for obsBallIt in self.obs_balls:
                        dot = ((obsBallIt.pos[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (obsBallIt.pos[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            circleLineDist = line.lineLenght(obsBallIt.pos, closest)
                            if circleLineDist <= obsBallIt.radius:
                                obsBallIt.velocity[1] *= (-0.8)
                                obsBallIt.update()

                    for square_it in self.squares:
                        # square_wall_col,_,_ = sat.sat_two_polygons(square_it.points, wall_it.points)
                        # if square_wall_col:
                        #     square_it.velocity[1] *= -0.8
                        #     square_it.update()
                        dot = ((square_it.center[0] - p1Lin[0])*(p2Lin[0] - p1Lin[0]) + (square_it.center[1] - p1Lin[1])*(p2Lin[1] - p1Lin[1])) / linLen**2
                        closestX, closestY = line.findClosest(dot, p1Lin, p2Lin) #nz da li ovo ispradne np.array ili tuple pa sam za sad stavio ovako
                        closest = np.array([closestX, closestY])
                        if line.pointOnLine(closest, p1Lin, p2Lin) == True:
                            squareLineDist = line.lineLenght(square_it.center, closest)
                            if squareLineDist <= config.square_width:
                                square_it.velocity[1] *= -0.8
                                square_it.update()


    def check_collision_main_ball_obs_ball(self):
        for ballIt in self.obs_balls:
        # for i in range(config.obs_balls_number):
            distX = self.main_ball.pos[0] - ballIt.pos[0]
            distY = self.main_ball.pos[1] - ballIt.pos[1]
            distance = np.sqrt( distX**2 + distY**2)
            if distance <= self.main_ball.radius + ballIt.radius:
                
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
                self.main_ball.update()
                ballIt.velocity = reaction_vector_ball_it
                self.update_obs_balls()
                self.score += 1

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
                        ballIt1.update()
                        ballIt2.velocity = reaction_vector_ball2
                        ballIt2.update()

    def check_collision_all_wall_corner(self):
        for square_it in self.wall_corner_squares:
                is_col, norm, depth = sat.sat_polygon_circle(self.main_ball, square_it)
                if is_col:
                    
                    self.main_ball.velocity += -norm * depth / 2
                    self.main_ball.velocity *= 0.8
                    self.main_ball.update()

                for ball_it in self.obs_balls:
                    is_col, norm, depth = sat.sat_polygon_circle(ball_it, square_it)
                    if is_col:
                        ball_it.velocity += -norm * depth / 2
                        ball_it.velocity *= 0.8
                        ball_it.update()

                for square_it2 in self.squares:
                    is_col, norm, depth = sat.sat_two_polygons(square_it.points, square_it2.points)
                    if is_col:
                        square_it2.velocity += norm * depth / 2
                        square_it2.velocity *= 0.8
                        square_it2.update()

    def check_collision_main_ball_square(self):
        for square_it in self.squares:
            is_col, norm, depth = sat.sat_polygon_circle(self.main_ball, square_it)
            if is_col:
                square_it.velocity += norm * depth / 2
                square_it.velocity *= 0.8
                square_it.update()
                self.main_ball.velocity += -norm * depth / 2
                self.main_ball.velocity *= 0.8
                self.main_ball.update()
                self.score += 0.5
        
    def check_collision_obs_ball_square(self):
        for square_it in self.squares:
            for ball_it in self.obs_balls:
                is_col, norm, depth = sat.sat_polygon_circle(ball_it, square_it)
                if is_col:
                    square_it.velocity += norm * depth / 2
                    square_it.velocity *= 0.8
                    square_it.update()
                    ball_it.velocity += -norm * depth / 2
                    ball_it.velocity *= 0.8
                    ball_it.update()

    def check_collision_sqares(self):
        for square_it1 in self.squares:
            for square_it2 in self.squares:
                if square_it1 != square_it2:
                    is_col, norm, depth = sat.sat_two_polygons(square_it1.points, square_it2.points)
                    if is_col:
                        square_it1.velocity += -norm * depth / 2
                        square_it1.velocity *= 0.8
                        square_it1.update()
                        square_it2.velocity += norm * depth / 2
                        square_it2.velocity *= 0.8
                        square_it2.update()

    def check_collision(self):
        self.check_collision_main_ball_obs_ball()
        self.check_collision_obs_ball_obs_ball()
        self.check_collision_all_wall()
        self.check_collision_all_wall_corner()
        self.check_collision_main_ball_square()
        self.check_collision_obs_ball_square()
        self.check_collision_sqares()


    #this function only calculates the force applyed by our mouse
    def calculate_main_ball_force(self):
        #force is calculated from ball centre not mouse down point because it works better when we click the edge of the ball 
        # self.main_ball_force = ((self.mouse_down[0] - self.mouse_up[0])/3, (self.mouse_down[1] - self.mouse_up[1])/3)
        self.main_ball_force = ((self.main_ball.pos[0] - self.mouse_up[0])/3, (self.main_ball.pos[1] - self.mouse_up[1])/3)

    def read_mouse_down(self, mouse_down_pos):
        self.mouse_down = mouse_down_pos

    def read_mouse_up(self, mouse_up_pos):
        self.mouse_up = mouse_up_pos


    def update_obs_balls(self):
        for ballIt in self.obs_balls:
            ballIt.update()

    def update_squares(self):
        for squareIt in self.squares:
            squareIt.update()
    
    def update_decoration_squares(self):
        for squareIt in self.decoration_squares:
            squareIt.update()

    def print_score(self):
        self.message_to_screen("Score: " + str(math.floor(self.score)), (250, 750), config.white)

    def check_if_game_over(self):
        if self.main_ball.pos[1] > 700:
            self.game_over = True

    def message_to_screen(self, message, cordinates, colour = config.red):
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render(message, True, colour)
        self.screen.blit(text, cordinates)

    def do_game(self):
        self.draw_walls()
        self.main_ball.update()
        self.update_obs_balls()
        self.update_squares()
        self.update_decoration_squares()
        self.draw_main_ball()
        self.draw_squares()
        self.draw_decoration_squares()
        self.draw_obs_balls()
        self.check_collision()
        self.draw_aim_line()
        self.print_score()
        self.check_if_game_over()
        self.message_to_screen("END", (285, 684))
        # self.draw_wall_corner_squares() #dont need to be drawn