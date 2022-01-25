import pygame
import config
import numpy as np
import game
import ball
import walls
import sat

game = game.Game()


running = True
while running:
    game.screen.fill(config.black)
    game.draw_walls()
    game.main_ball.update()
    game.update_obs_balls()
    game.update_squares()
    game.draw_main_ball()
    game.draw_squares()
    game.draw_obs_balls()
    game.check_collision()
    game.draw_aim_line()


    if sat.sat_two_polygons(game.squares[0].points, game.squares[1].points):
        print("DODIR")

    # if sat.sat_polygon_circle(game.main_ball.pos, game.main_ball.radius, game.squares[0].points):
    #     print("DODIR")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #reading the cordinates of where the mouse is pressed
            game.read_mouse_down(pygame.mouse.get_pos())
            #if the mouse was clicked on the main ball
            #also checks if the ball is moving, if it is, then we cant click it
            if ((game.mouse_down[0] - game.main_ball.pos[0])**2 + (game.mouse_down[1] - game.main_ball.pos[1])**2 <= game.main_ball.radius**2 and np.all((game.main_ball.velocity == 0))):
                print("main ball is clicked!")
                game.main_ball_clicked = True
            print(game.mouse_down)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:#3 znaci desni klik
            print("desni klik")
            # game.read_mouse_down(pygame.mouse.get_pos())
            # game.main_ball.pos[0] = game.mouse_down[0]
            # game.main_ball.pos[1] = game.mouse_down[1]
            # game.main_ball.velocity[0] = 0.0
            # game.main_ball.velocity[1] = 0.0
            game.squares[0].center[0] = game.mouse_down[0]
            game.squares[0].center[1] = game.mouse_down[1]

        if event.type == pygame.MOUSEBUTTONUP:  
            #reading the cordinates of where the mouse is unpressed
            game.read_mouse_up(pygame.mouse.get_pos())
            #if the main ball was clicked, the force that acts on the ball is 
            #equal to the vector made form the point where the mouse was clicked
            #and the point where the mouse was unclicked
            if game.main_ball_clicked:
                print("ball unclicked")
                game.calculate_main_ball_force()
                print(f'force vector is: {game.main_ball_force}')
                game.main_ball_clicked = False
                game.main_ball.apply_force(game.main_ball_force)
            print(game.mouse_up)

    pygame.display.update()