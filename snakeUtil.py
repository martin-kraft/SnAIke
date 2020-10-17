import math
import numpy as np


# Calculates the angle from the head to the food and
# which is then represented from -1 to 1 (-1 left, 0 straight forward, 1 right)
def calcDegree(snakeX, snakeY, foodX, foodY, direction):
    calc = math.atan2(snakeY - foodY, snakeX - foodX)
    switch = {
        "Up": -math.pi / 2,
        "Down": math.pi / 2,
        "Left": 0,
        "Right": -math.pi
    }
    return math.sin(calc + switch.get(direction))


# Returns distance between the snake's head to the wall or body part relative to the snakes directions.
# Distance = tiles before collision + 1 / panelSize
def checkLeft(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (0, -panelSize),
        "Left": (0, panelSize),
        "Up": (-panelSize, 0),
        "Down": (panelSize, 0)
    }

    distanceToWall = 0
    distanceToSnake = 0
    switchX, switchY = switch.get(direction)
    wallHit = False
    snakeHit = False
    while not wallHit:
        futureHeadPosition = snakeX + \
            switchX, snakeY + switchY
        futureHeadPositionX, futureHeadPositionY = futureHeadPosition

        if futureHeadPosition in snakePositions[1:]:
            snakeHit = True
            distanceToSnake += 1
        # count up if snake is not hit and stop counting if hit
        if not snakeHit:
            distanceToSnake += 1

        if not (futureHeadPositionX in (0, BOARD_SIZE) or
                futureHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
            distanceToWall += 1
            snakeX, snakeY = futureHeadPositionX, futureHeadPositionY
        else:
            wallHit = True

    if not snakeHit:
        distanceToSnake = 0

    OldRange = (panelSize - 0)
    NewRange = (1 - 0)
    NewValue = (((distanceToSnake - 0) * NewRange) / OldRange) + 0
    print(NewValue)
    return distanceToWall / panelSize, NewValue


def checkRight(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (0, panelSize),
        "Left": (0, -panelSize),
        "Up": (panelSize, 0),
        "Down": (-panelSize, 0)
    }
    distanceToWall = 0
    distanceToSnake = 0
    switchX, switchY = switch.get(direction)
    wallHit = False
    snakeHit = False
    while not wallHit:
        futureHeadPosition = snakeX + \
            switchX, snakeY + switchY
        futureHeadPositionX, futureHeadPositionY = futureHeadPosition

        if futureHeadPosition in snakePositions[1:]:
            snakeHit = True
            distanceToSnake += 1
        # count up if snake is not hit and stop counting if hit
        if not snakeHit:
            distanceToSnake += 1

        if not (futureHeadPositionX in (0, BOARD_SIZE) or
                futureHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
            distanceToWall += 1
            snakeX, snakeY = futureHeadPositionX, futureHeadPositionY
        else:
            wallHit = True

    if not snakeHit:
        distanceToSnake = 0

    OldRange = (panelSize - 0)
    NewRange = (1 - 0)
    NewValue = (((distanceToSnake - 0) * NewRange) / OldRange) + 0
    # print(NewValue)
    return distanceToWall / panelSize, NewValue


def checkForward(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (panelSize, 0),
        "Left": (-panelSize, 0),
        "Up": (0, -panelSize),
        "Down": (0, panelSize)
    }

    distanceToWall = 0
    distanceToSnake = 0
    switchX, switchY = switch.get(direction)
    wallHit = False
    snakeHit = False
    while not wallHit:
        futureHeadPosition = snakeX + \
            switchX, snakeY + switchY
        futureHeadPositionX, futureHeadPositionY = futureHeadPosition

        if futureHeadPosition in snakePositions[1:]:
            snakeHit = True
            distanceToSnake += 1
        # count up if snake is not hit and stop counting if hit
        if not snakeHit:
            distanceToSnake += 1

        if not (futureHeadPositionX in (0 - panelSize, BOARD_SIZE) or
                futureHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
            distanceToWall += 1
            snakeX, snakeY = futureHeadPositionX, futureHeadPositionY
        else:
            wallHit = True
    # if the snake couldn't bite itself, reset the value; otherwise it would return distance to wall
    if not snakeHit:
        distanceToSnake = 0

    # OldRange = (OldMax - OldMin)
    # NewRange = (NewMax - NewMin)
    # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

    OldRange = (panelSize - 0)
    NewRange = (1 - 0)
    NewValue = (((distanceToSnake - 0) * NewRange) / OldRange) + 0
    # print(1 - (panelSize - distanceToSnake) /
    #       panelSize)  # (value-min)/(max-min)
    # je weiter weg, desto größer der Wert, erstmal testen was daraus wird
    # print(NewValue)
    return distanceToWall / panelSize, NewValue


# Convert direction relative to snake's current direction
def convertDirectionRelativeToSnake(direction, newDirection):
    # LEFT, RIGHT, FORWARD
    if direction == "Right" and newDirection == "Left":
        result = "Up"
    elif direction == "Right" and newDirection == "Right":
        result = "Down"

    elif direction == "Left" and newDirection == "Right":
        result = "Up"
    elif direction == "Left" and newDirection == "Left":
        result = "Down"

    elif direction == "Down" and newDirection == "Left":
        result = "Right"
    elif direction == "Down" and newDirection == "Right":
        result = "Left"

    elif direction == "Up" and newDirection == "Left":
        result = "Left"
    elif direction == "Up" and newDirection == "Right":
        result = "Right"
    else:
        result = "Forward"
    return result


def sigmmoid(x):
    return 1/(1 + np.exp(-x))


def rectified(x):
    return max(0, x)


def tanH(x):
    return math.tanh(x)
