import numpy as np
#line: a*y = b*x + c
#vrv ce mi biti lakse da radim a*y + b*x + c = 0

def check_collision_ball_wall():
    tacka = np.array([1,1])
    wallIt = np.array([[5,0],[5, 11]])
    if wallIt[1][0] - wallIt[0][0] != 0:
        wallLineSlope = (wallIt[1][1] - wallIt[0][1]) / (wallIt[1][0] - wallIt[0][0]) #m = (y2 - y1)/(x2 - x1)
        wallLineA = 1.0
        wallLineB = wallLineSlope * (-1)
        wallLineC = wallLineSlope * wallIt[1][0] - wallIt[1][1]
    else:
        wallLineA = 0
        wallLineB = -1
        wallLineC = wallIt[0][0]*(-1)
    print(tacka[0] < max(wallIt[1][0], wallIt[0][0]))

    print(wallIt[1][0] - wallIt[0][0])
    print(f'{wallLineA}*y + {wallLineB}*x + {wallLineC} = 0')

def check_collision_ball_ball():

    ball1_pos = np.array([0,1])
    ball1_rad = 1
    ball2_pos = np.array([1,3])
    ball2_rad = 1

    distX = ball1_pos[0] - ball2_pos[0]
    distY = ball1_pos[1] - ball2_pos[1]
    distance = np.sqrt( distX**2 + distY**2)
    print(f'distX = {distX}\ndistY = {distY}\ndistance = {distance}')
    if distance <= ball1_rad + ball2_rad:
        print("KOLIZIJA")
    else:
        print("NIJE KOLIZIJA")

#distance = (abs(wallLineA *self.main_ball.pos[0]) + wallLineB * self.main_ball.pos[1] + wallLineC) / np.sqrt(wallLineA**2 + wallLineB**2))

check_collision_ball_ball()