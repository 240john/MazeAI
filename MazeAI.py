import numpy as np
import time
import pygame
import pygame.gfxdraw as gfx
import random
import maze

walls = [] # List to hold the walls

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

def Maze_generation():
    gen = 0
    popSize = 200
    stepCount = 60 # initial amount of steps allowed - increases over time

    # two arrays to hold all values of current rectangles, currently values all are 0
    RectanglesX = np.empty(popSize, dtype=int) 
    RectanglesX = [0 for i in range(popSize)] 
    RectanglesY = np.empty(popSize, dtype=int)
    RectanglesY = [0 for i in range(popSize)]

    #array for rectangle colors
    RectanglesColor = np.empty(popSize, dtype=int)
    RectanglesColor = [0 for i in range(popSize)]

    #assigns rectangle colors
    for populationCounter in range(popSize):
        RandColorVal = (random.randrange(1, 16777217))
        RectanglesColor[populationCounter] = RandColorVal

    # size of the maze
    mazeWidth = 800
    mazeHeight = 800

    background = pygame.display.set_mode((mazeWidth,mazeHeight))

    # Holds the level layout in a list of strings.
    level = maze.create_maze()

    # Parse the level string above. W = wall, E = exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "X":
                end_rect = pygame.Rect(x, y, 16, 16)
            x += 16
        y += 16
        x = 0

    rectangle = ((10,10), (4,4))
    numb1 = 10
    numb2 = 10

    background.fill((255, 255, 255))

    pygame.init()
    
    # displaying a window of height
    # 500 and width 400
    pygame.display.set_mode((mazeWidth, mazeHeight))
    
    # Setting name for window
    pygame.display.set_caption('Maze AI')
    
    # creating a bool value which checks
    # if game is running
    running = True
    
    # Game loop
    # keep game running till running is true
    while running:
    
        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():
        
            # if event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

    #--Random movement for ALL rectangles, values are randomed and added to arrays on lines 14-16
        for populationCounter in range(popSize):
            list = [-1,0,1]
            RandNum1 = (random.choice(list))
            RandNum2 = (random.choice(list))
            while RectanglesX[populationCounter] + RandNum1 < 0 or RectanglesX[populationCounter] + RandNum1 > 799:
                RandNum1 = (random.choice(list))
            while RectanglesY[populationCounter] + RandNum2 < 0 or RectanglesY[populationCounter] + RandNum2 > 799:
                RandNum2 = (random.choice(list))
            RectanglesX[populationCounter] = RectanglesX[populationCounter] + RandNum1
            RectanglesY[populationCounter] = RectanglesY[populationCounter] + RandNum2
            

    #---Previous random code for 1 Rectangle-----------------------
        #    list = [-1,0,1]
        #    RandNum1 = (random.choice(list))
        #    RandNum2 = (random.choice(list))
        #    while numb1 + RandNum1 < 0 or numb1 + RandNum1 > 799:
        #        RandNum1 = (random.choice(list))
        #    while numb2 + RandNum2 < 0 or numb2 + RandNum2 > 799:
        #        RandNum2 = (random.choice(list))
        #    numb1 = numb1 + RandNum1
        #    numb2 = numb2 + RandNum2
    #---------------------------------------------------------------

    #set background to white, then fill in rectangles following array
        background.fill((255, 255, 255))
        for populationCounter in range(popSize):
            rectangle = ((RectanglesX[populationCounter],RectanglesY[populationCounter]), (4,4))
            pygame.draw.rect(background,(RectanglesColor[populationCounter]),rectangle,2)
            #(50,100,250,255)
        for wall in walls:
            pygame.draw.rect(background, (0, 0, 0), wall.rect)


        pygame.display.flip()
        time.sleep(.001) #edit to adjust speed

#Maze_generation()