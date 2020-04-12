import math

# Calculates the angle from the head to the food and
# which is then represented from -1 to 1 (-1 left, 0 straight forward, 1 right)


def calcDegree(snakeX, snakeY, foodX, foodY, direction):
    calc = math.atan2(snakeY - foodY, snakeX - foodX)
    switch = {
        "Up": -math.pi / 2,
        "Down": math.pi / 2,
        "Left": 0,
        "Right": math.pi
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
    if direction == "Right" and newDirection == "Up":
        result = "Left"
    elif direction == "Rigth" and newDirection == "Down":
        result = "Right"
    elif direction == "Right" and newDirection == "Right":
        result = "Down"

    elif direction == "Left" and newDirection == "Up":
        result = "Right"
    elif direction == "Left" and newDirection == "Down":
        result = "Left"
    elif direction == "Left" and newDirection == "Left":
        result = "Down"

    elif direction == "Down" and newDirection == "Left":
        result = "Right"
    elif direction == "Down" and newDirection == "Right":
        result = "Left"
    else:
        result = "Forward"
    return result