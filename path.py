# Determines a simple path plan to move from the inputted start node to the goal node
# Input: start {Tuple} - the coordinates of the starting position, with the default value of (0,0)
#        goal {Tuple} - the coordinates of the final position, with the default value of (0,0)
# Output: pathList {Tuples list} - list of coordinates taking one step at a time to reach the 'goal' from the 'start'
def getPath(start = (0,0), goal = (0,0)):
    x_increase = goal[0] > start[0]
    y_increase = goal[1] > start[1]

    pathList = [start]
    x = start[0]
    y = start[1]

    if(start == goal): return pathList # Check if 'start' and 'goal' coordinates are the same point

    # Start by taking a step in the x-direction, except if there is no change in goal and start x values
    if(goal[0] == start[0]):
        if(y_increase): y += 1
        else: y -= 1
        slope = None
        b = None
    else:
        slope = (goal[1]-start[1])/(goal[0]-start[0])
        b = goal[1] - slope * goal[0] # y-intercept: found using slope-intercept equation (y = mx+b)
        if(x_increase): x += 1
        else: x -= 1
    
    coordinate = (x,y)
    pathList.append(coordinate)

    # Will increment or decrement the x or y value, one step at a time, until the goal coordinate is reached.
    # Each step will add the new coordinate to 'pathList'
    while(not(coordinate == goal)):
        
        if(slope is None): # Check for a vertical path
            if(y_increase): y += 1
            else: y -= 1
        elif(slope == 0): # Check for a horizontal path
            if(x_increase): x += 1
            else: x -= 1
        elif(y_increase):
            if(y < slope * x + b): y += 1
            else:
                if(x_increase): x += 1
                else: x -= 1
        else:
            if(y > slope * x + b): y -= 1
            else:
                if(x_increase): x += 1
                else: x -= 1

        coordinate = (x,y)
        pathList.append(coordinate)
    
    return pathList