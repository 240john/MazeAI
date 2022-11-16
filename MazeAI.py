import numpy as np
import time
import pygame
import pygame.gfxdraw as gfx
import random

gen = 0
popSize = 2000
stepCount = 60 # initial amount of steps allowed - increases over time

# size of the maze
mazeWidth = 800
mazeHeight = 800

background = pygame.display.set_mode((mazeWidth,mazeHeight))

rectangle = ((10,10), (4,4))
numb1 = 10
numb2 = 10

background.fill((255, 255, 255))

pygame.init()
 
# displaying a window of height
# 500 and width 400
pygame.display.set_mode((mazeWidth, mazeHeight))
 
# Setting name for window
pygame.display.set_caption('Testing')
 
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
     
    # Update our window
    # example of random movement follows this comment
    list = [-1,0,1]
    RandNum1 = (random.choice(list))
    RandNum2 = (random.choice(list))
    while numb1 + RandNum1 < 0 or numb1 + RandNum1 > 799:
        RandNum1 = (random.choice(list))
    while numb2 + RandNum2 < 0 or numb2 + RandNum2 > 799:
        RandNum2 = (random.choice(list))
    numb1 = numb1 + RandNum1
    numb2 = numb2 + RandNum2
    background.fill((255, 255, 255))
    rectangle = ((numb1,numb2), (4,4))
    pygame.draw.rect(background,(50,100,250,255),rectangle,2)
    pygame.display.flip()
    time.sleep(.01)