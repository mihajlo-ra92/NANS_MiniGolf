from math import sqrt
from dis import dis
import numpy as np
import sys
def sat_two_polygons(verticies1, verticies2):
    for i in range(len(verticies1)):
        vector_a = verticies1[i]
        #%len(points1) is for the last iteration so we dont go out of range
        #and we create an edge from the last and the first point
        vector_b = verticies1[(i + 1) % len(verticies1)]
        edge = np.array([0.0, 0.0])
        edge[0] = vector_b[0] - vector_a[0]
        edge[1] = vector_b[1] - vector_a[1]
        axis = np.array([edge[1], -edge[0]])
        min1, max1 = project_vetricies(verticies1, axis)
        min2, max2 = project_vetricies(verticies2, axis)
        if min1 >= max2 or min2 >= max1:
            return False

    for i in range(len(verticies2)):
        vector_a = verticies2[i]
        vector_b = verticies2[(i + 1) % len(verticies2)]
        edge = np.array([0.0, 0.0])
        edge[0] = vector_b[0] - vector_a[0]
        edge[1] = vector_b[1] - vector_a[1]
        axis = np.array([edge[1], -edge[0]]) 

        min1, max1 = project_vetricies(verticies1, axis)
        min2, max2 = project_vetricies(verticies2, axis)
        if min1 >= max2 or min2 >= max1:
            return False

    return True

def project_vetricies(vetricies, axis):
    min = sys.maxsize
    max = -sys.maxsize
    for i in range(len(vetricies)):
        v = vetricies[i]
        #projection is dot product of vetrices and axis
        proj = dot(v,axis)
        if proj < min:
            min = proj
        if proj > max:
            max = proj
    
    return min, max

def sat_polygon_circle(circle_center, circle_radius, verticies):

    normal = np.array([0.0, 0.0])
    depth = sys.maxsize
    for i in range(len(verticies)):
        vector_a = verticies[i]
        #%len(points1) is for the last iteration so we dont go out of range
        #and we create an edge from the last and the first point
        vector_b = verticies[(i + 1) % len(verticies)]
        edge = np.array([0.0, 0.0])
        edge[0] = vector_b[0] - vector_a[0]
        edge[1] = vector_b[1] - vector_a[1]
        axis = np.array([edge[1], -edge[0]])
        min1, max1 = project_vetricies(verticies, axis)
        min2, max2 = project_circle(circle_center, circle_radius, axis)
        if min1 >= max2 or min2 >= max1:
            return False


    closest_point = find_closest_point_of_polygon(circle_center, verticies)
    axis = verticies[closest_point] - circle_center
    min1, max1 = project_vetricies(verticies, axis)
    min2, max2 = project_circle(circle_center, circle_radius, axis)
    if min1 >= max2 or min2 >= max1:
        return False

    return True

def project_circle(circle_center, circle_radius, axis):

    norm = sqrt(axis[0] ** 2 + axis[1] ** 2)
    axis_normalised = np.array([0.0, 0.0])
    axis_normalised[0] = axis[0] / norm
    axis_normalised[1] = axis[1] / norm
    #we used the normalised axis multiplied by the radius to find the "edges" of the circle
    point1 = circle_center - axis_normalised * circle_radius
    point2 = circle_center + axis_normalised * circle_radius
    #we use dot products to find min and max value
    min = dot(point1, axis)
    max = dot(point2, axis)
    #just in case, if min is greater than the max, swap them
    if min > max:
        temp = min
        min = max
        max = temp

    return min, max

def dot(value1, value2):
    return value1[0] * value2[0] + value1[1] * value2[1]

def find_closest_point_of_polygon(point, vetricies):
    result = -1
    min_distance = sys.maxsize
    for i in range(len(vetricies)):
        current_vetricies = vetricies[i]
        distance = 0.0
        distance = sqrt((point[0] - current_vetricies[0])**2 + (point[1] - current_vetricies[1])**2)
        if distance < min_distance:
            min_distance = distance
            result = i
        return result