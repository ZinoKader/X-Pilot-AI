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


def extract_coordinates_move_instruction(message):
    moveinstruction = message[:12]
    message = message.replace(moveinstruction, "")
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
    return message.replace("attack ship ", "")


def get_wrapped_coordinates(ai, target):

    selfX = ( ai.selfRadarX() / ai.radarWidth() ) * ai.mapWidthPixels()
    selfY = ( ai.selfRadarY() / ai.radarHeight() ) * ai.mapHeightPixels()
    px = None
    py = None

    if selfX > ai.mapWidthPixels() / 2:
        if selfX - ai.targetX(target) >= (ai.mapWidthPixels() / 2):
            px = ai.mapWidthPixels() - (selfX - ai.targetX(target))
        else:
            px = ai.targetX(target) - selfX
    else:
        if ai.targetX(target) - selfX >= (ai.mapWidthPixels() / 2):
            px = -(ai.mapWidthPixels() - (ai.targetX(target) - selfX))
        else:
            px = ai.targetX(target) - selfX

    if selfY > ai.mapHeightPixels() / 2:
        if selfY - ai.targetY(target) >= (ai.mapHeightPixels() / 2):
            py = ai.mapHeightPixels() - (selfY - ai.targetY(target))
        else:
            py = ai.targetY(target) - selfY
    else:
        if ai.targetY(target) - selfY >= (ai.mapHeightPixels() / 2):
            py = -(ai.mapHeightPixels() - (ai.targetY(target) - selfY))
        else:
            py = ai.targetY(target) - selfY

    return(px, py)


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
