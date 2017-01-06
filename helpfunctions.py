import math

def distanceTo(dist1, dist2):
    if dist1 > dist2:
        return dist1 - dist2
    else:
        return dist2 - dist1

def angleDiff(one, two):
    """Calculates the smallest angle between two angles"""

    a1 = (one - two) % (2*math.pi)
    a2 = (two - one) % (2*math.pi)
    return min(a1, a2)
