import numpy as np
import random
from random import randrange

def create_maze(rseed):
    random.seed(rseed)
    level = np.full((22, 22), 'W')
        
    x = randrange(22)
    startx = x
    y = 0
    endX = randrange(1,21) #if endX is 0 everything breaks
    endY = 21
    level[x][y] = 'S'
    level[endX][endY] = 'X'
    foundX = False
    list1 = [-1,1,1]
    list2 = [-1,-1,1]
    
    while not foundX:
        # select cell next to the current cell and ensure it's inbounds
        while True:
            if randrange(2) == 0:
                if x < endX:
                    num = random.choice(list1)
                else:
                    num = random.choice(list2)
                if x + num > 0 and x + num < 21 and y > 0:
                    x = x + num
                    break
            else:  
                if y < endY:
                    num = random.choice(list1)
                else:
                    num = random.choice(list2)
                if y + num > 0 and y + num < 21:
                    y = y + num
                    break

        # change the maze
        level[x][y] = ' '

        # check to see if we found 'X' in the last row
        if y == endY-1 and x == endX:
            foundX = True

    x = 0
    for x in range(5): # random path generation, this finds (5) random points and paths directly to them, this is optional
        foundX = False
        pointx = randrange(1,21)
        pointy = randrange(1,21)
        y = 0
        x1 = startx
        while not foundX:
            while True:
                if randrange(2) == 0:
                    if x1 < pointx:
                        num = 1
                    else:
                        num = -1
                    if x1 + num > 0 and x1 + num < 21 and y > 0:
                        x1 = x1 + num
                        break
                else:  
                    if y < pointy:
                        num = 1
                    else:
                        num = -1
                    if y + num > 0 and y + num < 21:
                        y = y + num
                        break   

            # change the maze
            level[x1][y] = ' '
            if y == pointy and x1 == pointx:
                foundX = True
                    
    return level