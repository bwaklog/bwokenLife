import os, sys, time, random
import numpy as np
from scipy.signal import convolve2d
import keyboard

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
    out = []
    for row in range(len(grid)):
        out.append(list(map(
            lambda x, y: predictFuture(x, y), grid[row], numGrid[row]
        )))
    return np.array(out)

def predictFuture(oldGridValue, numGridValue) -> int:
    if oldGridValue == 1:
        if oldGridValue in [2, 3]:
            return 1
        elif numGridValue > 3 or numGridValue < 2:
            return 0
        else:
            return 1
    elif oldGridValue == 0 and numGridValue == 3:
        return 1
    else:
        return oldGridValue
        

grid = generateRandomGrid(60)

for _ in range(200):
    displayGrid(grid)
    grid = computeGeneration(grid)
    time.sleep(.02)
    os.system('clear')