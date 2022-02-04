import numpy as np
def lineLenght(p1, p2):
    distX = p1[0] - p2[0]
    distY = p1[1] - p2[1]
    return np.sqrt(distX**2 + distY**2)

def findClosest(dot, p1, p2):
    closestX = p1[0] + (dot * (p2[0] - p1[0]))
    closestY = p1[1] + (dot * (p2[1] - p1[1]))
    return closestX, closestY

def pointOnLine(p, lP1, lP2):
    lineLen = lineLenght(lP1, lP2)
    dist1 = lineLenght(p, lP1)
    dist2 = lineLenght(p, lP2)
    allowedError = 0.1 # stavljamo jer brojevi nisu u potpunosti tacni
    if(dist1 + dist2 >= lineLen - allowedError and dist1 + dist2 <= lineLen + allowedError):
        return True
    else:
        return False



#provera da li radi provera da li je tacka na liniji
# tL1 = np.array([15, 0])
# tL2 = np.array([15, 700])
# tac = np.array([15, 3000])
# print(pointOnLine(tac, tL1, tL2))