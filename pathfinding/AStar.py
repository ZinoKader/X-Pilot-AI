global grid

def gridDistance(startPos, endPos):
    d = abs(startPos[0] - endPos[0]) + abs(startPos[1] - endPos[1])
    return d

def getMin(lst, diction):
    minNeighb = lst[0]
    for i in lst:
        if  diction[tuple(minNeighb)] > diction[tuple(i)]:
            minNeighb = i

    return minNeighb

def getNeighbors(position, grid):
    look = [[0,1],[1,0],[-1,0],[0,-1]]
    neighbList = []
    for vect in look:
        # sum is a tuple now
        sum = position[0] + vect[0], position[1] + vect[1]
        if grid[sum[0]][sum[1]] == 1:
            neighbList.append(list(sum))

    return neighbList


def astar(mapgrid, start, goal):
    grid = mapgrid
    closedSet = []
    openSet = [start]
    cameFrom = {}
    gScore = {}
    gScore[tuple(start)] = 0 # cost from start to start 0 of course
    # estimated total cost from start to goal through y
    fScore = {}

    fScore[tuple(start)] = gScore[tuple(start)] + gridDistance(start, goal)

    # while openSet not empty...
    while openSet:
        current = getMin(openSet, fScore)
        if current == goal:
            return reconstructPath(cameFrom, goal)

        openSet.remove(current)
        closedSet.append(current)
        for neighb in getNeighbors(current, grid) :
            if neighb in closedSet:
                continue
            tentativeGScore = gScore[tuple(current)] + 1 # add the distance of the neighbor to the cost of the path
            if neighb not in openSet:
                openSet.append(neighb)
            elif tentativeGScore >= gScore[tuple(neighb)]:
                continue # this is not a better path

            # the path is the best until now so record it
            cameFrom[tuple(neighb)] = current
            gScore[tuple(neighb)] = tentativeGScore
            fScore[tuple(neighb)] = gScore[tuple(neighb)] + gridDistance(neighb, goal)

    return False


def reconstructPath(cameFrom, current):
    totalPath = [current]
    while tuple(current) in cameFrom.keys():
        current = cameFrom[tuple(current)]
        totalPath.append(current)

    # get the reverse array...
    return totalPath[::-1]
