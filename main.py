import math
import pygame
import config
import numpy as np
import game
import ball
import walls
import sat

my_game = game.Game()


running = True
while running:
    my_game.screen.fill(config.black)
    if not my_game.game_over:
        my_game.do_game()
    else:
        my_game.message_to_screen("Game over!", (240, 200))
        my_game.message_to_screen("Score: " + str(math.floor(my_game.score)), (258, 250))
        # my_game.message_to_screen("Press SPACE to play again", (180, 300), config.white)

        # restart_game = False
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
            
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             print("SPACE")
        #             # my_game.game_over = False
        #             restart_game = True
        #             my_game = game.Game()
        
        # if restart_game:
        #     break

            
    # is_col_two_squares,nista, nista = sat.sat_two_polygons(game.squares[0].points, game.squares[1].points)
    # if is_col_two_squares:
    #     print("DODIR")

    # is_col_circle_square,nista, nista = sat.sat_polygon_circle(game.main_ball, game.squares[0])
    # if is_col_circle_square:
    #     print("DODIR")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #reading the cordinates of where the mouse is pressed
            my_game.read_mouse_down(pygame.mouse.get_pos())
            #if the mouse was clicked on the main ball
            #also checks if the ball is moving, if it is, then we cant click it
            if ((my_game.mouse_down[0] - my_game.main_ball.pos[0])**2 + (my_game.mouse_down[1] - my_game.main_ball.pos[1])**2 <= my_game.main_ball.radius**2 and np.all((my_game.main_ball.velocity == 0))):
                print("main ball is clicked!")
                my_game.main_ball_clicked = True
            print(my_game.mouse_down)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:#3 znaci desni klik
            print("desni klik")
            my_game.read_mouse_down(pygame.mouse.get_pos())
            my_game.main_ball.pos[0] = my_game.mouse_down[0]
            my_game.main_ball.pos[1] = my_game.mouse_down[1]
            my_game.main_ball.velocity[0] = 0.0
            my_game.main_ball.velocity[1] = 0.0
            # my_game.squares[0].center[0] = my_game.mouse_down[0]
            # my_game.squares[0].center[1] = my_game.mouse_down[1]

        if event.type == pygame.MOUSEBUTTONUP:  
            #reading the cordinates of where the mouse is unpressed
            my_game.read_mouse_up(pygame.mouse.get_pos())
            #if the main ball was clicked, the force that acts on the ball is 
            #equal to the vector made form the point where the mouse was clicked
            #and the point where the mouse was unclicked
            if my_game.main_ball_clicked:
                print("ball unclicked")
                my_game.calculate_main_ball_force()
                print(f'force vector is: {my_game.main_ball_force}')
                my_game.main_ball_clicked = False
                my_game.main_ball.apply_force(my_game.main_ball_force)
                my_game.score += 1
            # print(my_game.mouse_up)

    pygame.display.update()