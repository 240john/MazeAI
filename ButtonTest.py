import pygame
import MazeAI
import maze
import numpy as np
import pygame.gfxdraw as  gfx
from random import randrange


pygame.init()
screen = pygame.display.set_mode((700, 500))
screen.fill((255,255,255))

walls = [] # List to hold the walls
ending = [] # list to hold the end
empty = [] # list to hold empty tiles
level = ""

class Wall(object):
    def __init__(self, pos, width):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], width, 16)

class Empty(object):
    def __init__(self, pos, width):
        empty.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], width, 16)

class End(object):
    def __init__(self, pos, width):
        ending.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], width, 16)
 
def button(screen, position, text): # constructor
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0)) # where the text goes
    x, y, w , h = text_render.get_rect() # gets the size of the button
    x, y = position
    xpadding = 10
    ypadding = 5
    pygame.draw.line(screen, "black", (x - xpadding, y - ypadding), (x + w + xpadding, y - ypadding), 5) #draws the top border
    pygame.draw.line(screen, "black", (x - xpadding, y - 2 - ypadding), (x - xpadding, y + h + ypadding), 5) #draws the left border
    pygame.draw.line(screen, "black", (x - xpadding, y + h + ypadding - 2), (x + w + xpadding , y + h + ypadding - 2), 5) #draws the bottom boder
    pygame.draw.line(screen, (50, 50, 50), (x + w + xpadding - 2, y + h + ypadding), [x + w + xpadding - 2, y - ypadding], 5) #draws the right border
    pygame.draw.rect(screen, "white", (x, y, w , h)) #draw the button body
    return screen.blit(text_render, (x, y)) 

def generate():

    #generates the random seed for generation
    global rseed
    rseed = randrange(1000000)

    # Holds the level layout in a list of strings.
    level = maze.create_maze(rseed)
    offset = 20 # used to bring maze away from edge
    walls.clear()
    empty.clear()
    ending.clear()

    x = y = 0   # makes an empty array used to clear the maze when regenerating the maze
    for row in level:
        for col in row:
            Empty((x+offset, y+offset),16)
            x += 16
        y += 16
        x = 0

    # Parse the level string above. W = wall, X = start/exit
    # this loop puts values in for the final print at the end of the menu function
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x+offset, y+offset),16)  
#            elif col == "S":
 #             #  Empty((x+offset, y+offset),16)
            elif col == "X":
                End((x+14+offset,y+offset),2)
            x += 16
        y += 16
        x = 0

    return level

def start(level): #event for start button
    MazeAI.Maze_generation(level)
 
def menu(): # main loop
    screen.fill((255, 255, 255))

    # This is the menu that waits you to click the s key to start 
    b1 = button(screen, (610, 425), "Quit") #create the quit button
    b2 = button(screen, (495, 425), "Start") #create the start button
    b3 = button(screen, (15, 425), "Generate")#create the generate maze button

    genCheck = False # this is necesarry for the conditional statement for b2
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                if key_to_start:
                    start(level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()): #conditional statement checks if generated map exists
                    if genCheck == True:
                        start(level)
                    else:
                        level = generate()
                        start(level)
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    genCheck = True
                    level = generate()

        # draw walls and end of maze
        for spot in empty: # This is used to clear the already populated maze when regenerating it
            pygame.draw.rect(screen, (255, 255, 255, 255), spot.rect)
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 1, 255), wall.rect)
        for end in ending:
            pygame.draw.rect(screen, (0, 255, 150, 255), end.rect)
        pygame.display.update()
    pygame.quit()
 
menu()