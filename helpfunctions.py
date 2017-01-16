import math
import random
import re

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


def extract_coordinates_move_instruction(message):
    message = message.replace("mission move to ", "")
    message = message.strip()

    xcoords = ""
    for char in message:
        if char == " ":
            break
        if char in "0123456789":
            xcoords += char

    message = message.replace(xcoords, "", 1) # ta bort en gång (ifall x och y-koordinaterna är samma)
    message = message.strip()

    ycoords = ""
    for char in message:
        if char == " ":
            break
        if char in "0123456789":
            ycoords += char

    return(xcoords, ycoords)


def extract_target_ship_name(message):
    message = re.sub(r'\[.+?\]\s*', '', message) # remove brackets and their contents (removes sender name)
    message = message.replace("mission attack ship ", "")
    return message


def no_targets_near(ai):
    return ai.shipCountScreen() == 1 # just our own ship


def get_wrapped_coordinates(ai, target):

    selfX = ( ai.selfRadarX() / ai.radarWidth() ) * ai.mapWidthPixels()
    selfY = ( ai.selfRadarY() / ai.radarHeight() ) * ai.mapHeightPixels()
    px = None
    py = None

    if selfX > ai.mapWidthPixels() / 2:
        if selfX - ai.shipX(target) >= (ai.mapWidthPixels() / 2):
            px = ai.mapWidthPixels() - (selfX - ai.shipX(target))
        else:
            px = ai.shipX(target) - selfX
    else:
        if ai.shipX(target) - selfX >= (ai.mapWidthPixels() / 2):
            px = -(ai.mapWidthPixels() - (ai.shipX(target) - selfX))
        else:
            px = ai.shipX(target) - selfX

    if selfY > ai.mapHeightPixels() / 2:
        if selfY - ai.shipY(target) >= (ai.mapHeightPixels() / 2):
            py = ai.mapHeightPixels() - (selfY - ai.shipY(target))
        else:
            py = ai.shipY(target) - selfY
    else:
        if ai.shipY(target) - selfY >= (ai.mapHeightPixels() / 2):
            py = -(ai.mapHeightPixels() - (ai.shipY(target) - selfY))
        else:
            py = ai.shipY(target) - selfY

    return(px, py)


# from teacherbot, thanks.
def find_free_random_position(ai):
    mapwidth = ai.mapWidthPixels()
    mapheight = ai.mapHeightPixels()
    mapwblock = ai.mapWidthBlocks()
    maphblock = ai.mapHeightBlocks()
    dw = mapwidth/mapwblock
    dh = mapheight/maphblock

    found = False
    while not found:
        bx = random.randint(0, mapwblock-1)
        by = random.randint(0, maphblock-1)
        type = ai.mapData(bx, by)
        if type == 0:
            found = True

    x = int(bx*dw + dw/2)
    y = int(by*dh + dh/2)

    return (x, y)


def time_of_impact(px, py, vx, vy, s):

    a = (s * s) - ( (vx * vx) + (vy * vy) )
    b = (px * vx) + (py * vy)
    c = (px * px) + (py * py)

    d = (b * b) + (a * c)

    t = 0
    if d >= 0:
        t = (b + math.sqrt(d)) / a
        if t < 0:
            t = 0
    return t
