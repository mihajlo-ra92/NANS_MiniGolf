import square
import numpy as np
import sat
import pygame
import config
import game
square1 = square.Square(np.array([100, 100]))
square2 = square.Square(np.array([150, 100]))


game = game.Game()

running = True
while running:
    game.screen.fill(config.black)
    game.draw_squares()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #reading the cordinates of where the mouse is pressed
            game.read_mouse_down(pygame.mouse.get_pos())
            game.squares[0].center[0] = pygame.mouse.get_pos()[0]
            game.squares[1].center[1] = pygame.mouse.get_pos()[1]
            game.draw_squares()
            # square1.center[0] = pygame.mouse.get_pos()[0]
            # square1.center[1] = pygame.mouse.get_pos()[1]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:#3 znaci desni klik
            print("desni klik")
            game.read_mouse_down(pygame.mouse.get_pos())
            game.main_ball.pos[0] = game.mouse_down[0]
            game.main_ball.pos[1] = game.mouse_down[1]
            game.main_ball.velocity[0] = 0.0
            game.main_ball.velocity[1] = 0.0

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