import numpy as np
import config

class Square():
    def __init__(self, center, angular_vel = 0, width = config.square_width):
        self.center = center
        self.width = width
        self.points = np.array([[self.center[0] - self.width, self.center[1] - self.width],[self.center[0] - self.width, self.center[1] + self.width],[self.center[0] + self.width, self.center[1] + self.width],[self.center[0] + self.width, self.center[1] - self.width]])
        self.angle = 0.0 #in degrees
        self.angular_velocity = angular_vel
        self.velocity = np.array([0.0, 0.0])
        self.mass = 10.0
        self.impulse = 0

    def update(self):
        self.velocity *= config.friction_coef
        self.center += self.velocity
        # as we move the center, we must move the points with it
        self.points = np.array([[self.center[0] - self.width, self.center[1] - self.width],[self.center[0] - self.width, self.center[1] + self.width],[self.center[0] + self.width, self.center[1] + self.width],[self.center[0] + self.width, self.center[1] - self.width]])
        # self.angular_velocity *= config.friction_coef
        self.angle += self.angular_velocity
        self.rotate()
        if self.center[1] > 700.0 and self.angular_velocity == 0.0:
            self.center[1] = 7000.0

    def rotate(self):
        radAngle = self.angle * np.pi/180
        tempX = (self.points[0, 0] - self.center[0])*np.cos(radAngle) - (self.points[0, 1] - self.center[1])*np.sin(radAngle) + self.center[0]
        tempY = (self.points[0, 0] - self.center[0])*np.sin(radAngle) + (self.points[0, 1] - self.center[1])*np.cos(radAngle) + self.center[1]
        self.points[0, 0] = tempX
        self.points[0, 1] = tempY

        tempX = (self.points[1, 0] - self.center[0])*np.cos(radAngle) - (self.points[1, 1] - self.center[1])*np.sin(radAngle) + self.center[0]
        tempY = (self.points[1, 0] - self.center[0])*np.sin(radAngle) + (self.points[1, 1] - self.center[1])*np.cos(radAngle) + self.center[1]
        self.points[1, 0] = tempX
        self.points[1, 1] = tempY

        tempX = (self.points[2, 0] - self.center[0])*np.cos(radAngle) - (self.points[2, 1] - self.center[1])*np.sin(radAngle) + self.center[0]
        tempY = (self.points[2, 0] - self.center[0])*np.sin(radAngle) + (self.points[2, 1] - self.center[1])*np.cos(radAngle) + self.center[1]
        self.points[2, 0] = tempX
        self.points[2, 1] = tempY

        tempX = (self.points[3, 0] - self.center[0])*np.cos(radAngle) - (self.points[3, 1] - self.center[1])*np.sin(radAngle) + self.center[0]
        tempY = (self.points[3, 0] - self.center[0])*np.sin(radAngle) + (self.points[3, 1] - self.center[1])*np.cos(radAngle) + self.center[1]
        self.points[3, 0] = tempX
        self.points[3, 1] = tempY
        