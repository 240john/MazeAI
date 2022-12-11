import numpy as np
import time
import pygame
import pygame.gfxdraw as gfx
import random
import maze

walls = [] # List to hold the walls
ending = [] # list to hold the end

class Wall(object):
    def __init__(self, pos, width):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], width, 16)

class End(object):
    def __init__(self, pos, width):
        ending.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], width, 16)

def Maze_generation(level):
    gen = 0
    popSize = 60
    stepCount = 30 # initial amount of steps allowed - increases
                   # with each generation
    steps = 0 # amount of steps completed per generation
    startEnd = np.empty((2,2))
    offset = 20 # used to bring maze away from edge

    # Holds the level layout in a list of strings.
    # level = maze.create_maze()

    # Parse the level string above. W = wall, X = start/exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x+offset, y+offset),16)
            if col == "S":
                startEnd[0][0] = x+offset
                startEnd[0][1] = y+offset
            if col == "X":
                End((x+14+offset,y+offset),2)
                startEnd[1][0] = x+offset
                startEnd[1][1] = y+offset
            x += 16
        y += 16
        x = 0

    # two arrays to hold all values of current rectangles, currently values all are 0
    RectanglesX = np.empty(popSize, dtype=int) 
    RectanglesX = [startEnd[0][0] for i in range(popSize)] 
    RectanglesY = np.empty(popSize, dtype=int)
    RectanglesY = [startEnd[0][1] for i in range(popSize)]
    RectanglesDead = np.empty(popSize, dtype=bool) 
    RectanglesDead = [False for i in range(popSize)]
    RectanglesFitness = np.empty(stepCount, dtype=int) 
    RectanglesFitness = [10000 for i in range(popSize)]
    RectanglesXHistory = np.zeros((popSize, stepCount), dtype=int)
    RectanglesYHistory = np.zeros((popSize, stepCount), dtype=int)
    NextX = np.zeros((5, stepCount), dtype=int)
    NextY = np.zeros((5, stepCount), dtype=int)

    #array for rectangle colors
    RectanglesColor = np.empty(popSize, dtype=int)
    RectanglesColor = [0 for i in range(popSize)]

    #assigns rectangle colors
    for populationCounter in range(popSize):
        RandColorVal = (100,100,255,255)
        RectanglesColor[populationCounter] = RandColorVal

    # size of the maze
    mazeWidth = 700
    mazeHeight = 500

    background = pygame.display.set_mode((mazeWidth,mazeHeight))

    background.fill((255, 255, 255))

    pygame.init()
    
    # displaying a window
    pygame.display.set_mode((mazeWidth, mazeHeight))
    
    # Setting name for window
    pygame.display.set_caption('Maze AI')
    
    # creating a bool value which checks
    # if game is running
    running = True
    
    # Game loop
    # keep game running till running is true
    while running:
    
        # check to see if it's time to start a new generation
        if steps == stepCount:           
            # calculate fitness of dots
            # if dot is in collision with a wall fitness = 0
            for populationCounter in range(popSize):
                if RectanglesDead[populationCounter] != True:
                    RectanglesFitness[populationCounter] = np.sqrt((RectanglesX[populationCounter]-startEnd[1][1])**2+(RectanglesY[populationCounter]-startEnd[1][0])**2) # distance formula to calculate fitness

            # save moves made by 5 best dots
            # this will keep track of 5 best dots, of which we can find the moves in the
            lowest = 9999.0
            inc = -1
            SortedRectangles = np.empty(5, dtype=int)
            for x in range(0, 5):
                for populationCounter in range(popSize):
                    if RectanglesFitness[populationCounter] < lowest:
                        lowest = RectanglesFitness[populationCounter]
                        inc = populationCounter
                RectanglesFitness[inc] = 9999.0
                lowest = 9999.0
                SortedRectangles[x] = inc
            
            # reset dots
            RectanglesX = np.empty(popSize, dtype=int)  
            RectanglesX = [startEnd[0][0] for i in range(popSize)] 
            RectanglesY = np.empty(popSize, dtype=int)
            RectanglesY = [startEnd[0][1] for i in range(popSize)]
            RectanglesDead = [False for i in range(popSize)]
            NextX = np.zeros((5, stepCount), dtype=int)
            NextY = np.zeros((5, stepCount), dtype=int)

            # iterate through the rectangles up to stepCount and mutate based on saved moves
            '''
            for rectangle in SortedRectangles:
                randomNum = random.randrange(0, 30)
                if randomNum == 25: # do change a value in the history and all subsequent moves
                    randomNum2 = random.randrange(0, 2) # decide if we are changing x or y
                    randomNum3 = random.randrange(0, 2) # decide if we add or subtract one
                    if randomNum2 == 0: # x
                        if randomNum3 == 0: # add one
                            for bananas in range(0, popSize):
                                RectanglesXHistory[bananas][rectangle] += 1
                        else: # subtract one
                            for bananas in range(0, popSize):
                                RectanglesXHistory[bananas][rectangle] -= 1
                    else: # y
                        if randomNum3 == 0: # add one
                            for bananas in range(0, popSize):
                                RectanglesYHistory[bananas][rectangle] += 1
                        else: # subtract one
                            for bananas in range(0, popSize):
                                RectanglesYHistory[bananas][rectangle] -= 1'''

            # store mutated values
            for dot in range(0, 5):
                for st in range(0, stepCount):
                    NextX[dot][st] = RectanglesXHistory[SortedRectangles[dot]][st]
                    NextY[dot][st] = RectanglesYHistory[SortedRectangles[dot]][st]
            
            # reset steps and increase stepCount
            stepCount += 30
            steps = 0

            # add 30 more columns to the matrices to store history
            new_col = RectanglesXHistory.sum(1)[...,None]
            new_col.shape
            for i in range(0, 30):
                RectanglesXHistory = np.append(RectanglesXHistory, new_col, 1)
                RectanglesYHistory = np.append(RectanglesYHistory, new_col, 1)
                RectanglesXHistory.shape
                RectanglesYHistory.shape
            
        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():
            # if event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

        # Random movement for ALL rectangles, values are randomed and added to arrays on lines 14-16
        if steps < stepCount - 30:
            for populationCounter in range(popSize):
                RectanglesX[populationCounter] = NextX[populationCounter%5][steps]
                RectanglesXHistory[populationCounter][steps] = NextX[populationCounter%5][steps]
                RectanglesY[populationCounter] = NextY[populationCounter%5][steps]
                RectanglesYHistory[populationCounter][steps] = NextY[populationCounter%5][steps]
        else:
            for populationCounter in range(popSize):
                list = [-1,0,1]
                RandNum1 = (random.choice(list))
                RandNum2 = (random.choice(list))
                if RectanglesDead[populationCounter] == False:
                    while RectanglesX[populationCounter] + RandNum1 < 20 or RectanglesY[populationCounter] + RandNum1 > 352:
                        RandNum1 = (random.choice(list))
                if RectanglesDead[populationCounter] == False:
                    while RectanglesY[populationCounter] + RandNum2 < 20 or RectanglesY[populationCounter] + RandNum2 > 352:
                        RandNum2 = (random.choice(list))
                if RectanglesDead[populationCounter] == False:
                    RectanglesX[populationCounter] = RectanglesX[populationCounter] + RandNum1
                    RectanglesXHistory[populationCounter][steps] = RectanglesX[populationCounter] + RandNum1
                if RectanglesDead[populationCounter] == False:
                    RectanglesY[populationCounter] = RectanglesY[populationCounter] + RandNum2
                    RectanglesYHistory[populationCounter][steps] = RectanglesY[populationCounter] + RandNum2
            
        # check to see if dots will be colliding with wall
        # if it is, add it to the dead dot array
        for populationCounter in range(popSize):
            # check if wall is where the dot will be
            xy = background.get_at((RectanglesX[populationCounter].astype(np.int64), RectanglesY[populationCounter].astype(np.int64)))
            if xy == (0,0,1,255):
                RectanglesDead[populationCounter] = True

        # set background to white, then fill in rectangles following array
        background.fill((255, 255, 255))
        for populationCounter in range(popSize):
            rectangle = ((RectanglesX[populationCounter],RectanglesY[populationCounter]), (4,4))
            pygame.draw.rect(background,RectanglesColor[populationCounter],rectangle,2)

        # draw walls and end of maze
        for wall in walls:
            pygame.draw.rect(background, (0, 0, 1, 255), wall.rect)
        for end in ending:
            pygame.draw.rect(background, (0, 255, 150, 255), end.rect)


        pygame.display.flip()
        time.sleep(.01) # edit to adjust speed 
        steps += 1