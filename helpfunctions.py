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
