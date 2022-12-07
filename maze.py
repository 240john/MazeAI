import numpy as np
import random
from random import randrange

def create_maze():
    level = np.full((22, 22), 'W')
        
    x = randrange(22)
    y = 0
    endX = randrange(22)
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

    return level