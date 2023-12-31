import os, sys, time, random
import numpy as np
import pygame
import itertools

def generateGridTemplate(n:int)->list:
    return [ [float("inf")] * n for _ in range(n) ]

def generateRandomGrid(n: int) -> list:
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]


def displayGrid(grid: list) -> None:
    for i in grid:
        for j in i:
            print(j, end=" ")
        print()

def readGridTemplate() -> list:
    out = []
    with open('grid.txt', 'r') as f:
        for line in f:
            out.append(list(line.strip()))

    return out


def decodeCurrentGeneration(grid: list) -> list:
    """
    The emoji grid is converted into a number grid
    0 -> no life
    1 -> life
    """
    for row in grid:
        for i in range(len(row)):
            if row[i] == "⬛":
                row[i] = 0
            if row[i] == "🟩":
                row[i] = 1

    return grid


def computeNextGeneration(grid: list) -> list:
    gridLen = len(grid)
    out = generateGridTemplate(n=gridLen)

    for i in range(gridLen):
        for j in range(gridLen):
            """ Check surrounding
            - 0 1 2
            0 a b c
            1 d X e
            2 f g h

            Compute these values, if its an edge,
            then return the value of 0
            """

            # Check for row 1
            a = gridVal(grid, i-1, j-1)
            b = gridVal(grid, i-1, j)
            c = gridVal(grid, i-1, j+1)

            # Check row 2
            d = gridVal(grid, i, j-1)
            e = gridVal(grid, i, j+1)

            # Check row 3
            f = gridVal(grid, i+1, j-1)
            g = gridVal(grid, i+1, j)
            h = gridVal(grid, i+1, j+1)

            curVal = grid[i][j]
            aliveSur = sum([a, b, c, d, e, f, g ,h])

            if (aliveSur < 2) and curVal == 1:
                out[i][j] = 0
            
            elif (aliveSur in [2, 3]) and curVal == 1:
                out[i][j] = 1

            elif (aliveSur > 3) and curVal == 1:
                out[i][j] = 0

            elif (curVal == 0) and (aliveSur == 3):
                out[i][j] = 1
            
            else:
                out[i][j] = grid[i][j]

    return out


def gridVal(grid: list, i: int, j: int) -> int:
    gridLen = len(grid)
    if (i < 0) or (i >= gridLen) or (j < 0) or (j >= gridLen):
        return 0
    return grid[i][j]


# convert numbers to nice emojis :)
def emojiDisplay(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 1:
                print("{:3}".format('*'), end="")
            else:
                print("{:3}".format(" "), end="")

        print()


# grid = readGridTemplate()
grid = generateRandomGrid(n=200)
# for _ in range(200):
#     grid = decodeCurrentGeneration(grid)
#     emojiDisplay(grid)
#     # cont = [True ,False][input("Next(y/n) : ").lower() == "n"]
#     grid = computeNextGeneration(grid)

array = np.array(grid).shape

# Pygame stuff
grid_width, grid_height = array[0], array[1]
# grid = np.random.randint(2, size=(grid_width, grid_height))
cell_size = 5
screen_width = grid_width * cell_size
screen_height = grid_height * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('bwokenLife')

white = (255, 255, 255)
black = (0, 0, 0)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    for i, j in itertools.product(range(grid_width), range(grid_height)):
        color = white if grid[i][j] == 1 else black
        x = i * cell_size
        y = j * cell_size
        pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

    pygame.display.flip()

    grid = computeNextGeneration(grid)

    clock.tick(30)


pygame.quit()