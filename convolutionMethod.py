import os, sys, time, random
import numpy as np
from scipy.signal import convolve2d
import pygame
import itertools

def generateRandomGrid(n: int) -> list:
    return np.array([[random.randint(0, 1) for _ in range(n)] for _ in range(n)])

def displayGrid(grid: list):
    print('\n'.join([''.join(['{:3}'.format('*' if item==1 else ' ') for item in row]) for row in grid]))

def formatedGrid(grid: list):
    print('\n'.join([''.join(['{:3}'.format('*' if (item in [2, 3]) and () else ' ') for item in row]) for row in grid]))

def computeGeneration(grid: list):
    grid = np.array(grid)
    numGrid = np.array(convolve2d(
        grid,
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        mode='same'
    ))
    out = [
        list(map(lambda x, y: predictFuture(x, y), grid[row], numGrid[row]))
        for row in range(len(grid))
    ]
    return np.array(out)

def predictFuture(oldGridValue, numGridValue) -> int:
    if oldGridValue == 1:
        if oldGridValue in [2, 3] or numGridValue <= 3 and numGridValue >= 2:
            return 1
        else:
            return 0
    elif oldGridValue == 0 and numGridValue == 3:
        return 1
    else:
        return oldGridValue
        

grid = generateRandomGrid(200)
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

    grid = computeGeneration(grid)

    clock.tick(30)


pygame.quit()

# for _ in range(200):
#     displayGrid(grid)
#     grid = computeGeneration(grid)
#     time.sleep(.02)
#     os.system('clear')