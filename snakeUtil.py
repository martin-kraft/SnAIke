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


# Returns 1 if a wall or body part is on the left side of the snake's head or 0 if it is clear,
# in relation to the moving direction
# If the snake is moving "down", then the right side is checked (from the players perspective)
def checkLeft(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    result = 0
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (0, -panelSize),
        "Left": (0, panelSize),
        "Up": (-panelSize, 0),
        "Down": (panelSize, 0)
    }
    switchX, switchY = switch.get(direction)
    leftHeadPosition = (snakeX + switchX, snakeY + switchY)
    leftHeadPositionX, leftHeadPositionY = leftHeadPosition

    if (leftHeadPosition in snakePositions[1:] or
            leftHeadPositionX in (0, BOARD_SIZE) or
            leftHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
        result = 1
    return result


def checkRight(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    result = 0
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (0, panelSize),
        "Left": (0, -panelSize),
        "Up": (panelSize, 0),
        "Down": (-panelSize, 0)
    }
    switchX, switchY = switch.get(direction)
    leftHeadPosition = (snakeX + switchX, snakeY + switchY)
    leftHeadPositionX, leftHeadPositionY = leftHeadPosition

    if (leftHeadPosition in snakePositions[1:] or
            leftHeadPositionX in (0, BOARD_SIZE) or
            leftHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
        result = 1
    return result


def checkForward(snakePositions, panelSize, BOARD_SIZE, TEXT_SIZE, direction):
    result = 0
    snakeX, snakeY = snakePositions[0]
    switch = {
        "Right": (panelSize, 0),
        "Left": (-panelSize, 0),
        "Up": (0, -panelSize),
        "Down": (0, panelSize)
    }
    switchX, switchY = switch.get(direction)
    leftHeadPosition = (snakeX + switchX, snakeY + switchY)
    leftHeadPositionX, leftHeadPositionY = leftHeadPosition

    if (leftHeadPosition in snakePositions[1:] or
            leftHeadPositionX in (0 - panelSize, BOARD_SIZE) or
            leftHeadPositionY in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)):
        result = 1
    return result


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
