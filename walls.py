import numpy as np

class Walls():
    def __init__(self):

        self.width = 15
        self.walls_number = 9

        #individual walls
        left_wall = np.array([[0,0],[0, 700],[self.width, 700], [self.width, 0]])
        right_wall = np.array([[600,700],[600-self.width,700],[600-self.width,0], [600, 0]])
        upper_wall = np.array([[0,0],[0,self.width],[600, self.width], [600, 0]])
        lower_left_wall = np.array([[0,700],[0,700-self.width],[280,700-self.width], [280, 700]])
        lower_right_wall = np.array([[330,700],[330,700-self.width],[600,700-self.width], [600, 700]])
        court_wall1 = np.array([[85,85],[85,700],[85+self.width,700], [85+self.width, 85]])
        court_wall2 = np.array([[85,85],[85,85+self.width],[500, 85+self.width], [500, 85]])
        court_wall3 = np.array([[500, 85],[500+self.width,85],[500+self.width,600],[500,600]])
        court_wall4 = np.array([[330,700],[330+self.width,700],[330+self.width,200], [330, 200]])

        

        #list of walls
        self.walls_list = [left_wall, right_wall, upper_wall, lower_left_wall, lower_right_wall, court_wall1, court_wall2, court_wall3, court_wall4]