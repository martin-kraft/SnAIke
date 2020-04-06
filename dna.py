import random
import numpy as np
import helper
# Creates the population of snakes with their own DNA.
# DNA for each snake contains matrixes with float values between -1 to 1.

# 4 input layers
# 0 or 1 if body part or wall on the left side of snake's head
#                                    right side
#                                    front
# and a value of sinus of angle on which the food is inclined relative to the snake
# every input also includes the direction in which the snake is moving


class DNA():
    def __init__(self, boardSize, textSize, moveIncrement):
        self.BOARD_SIZE = boardSize
        self.MOVE_INCREMENT = moveIncrement
        self.TEXT_SIZE = textSize
        self.TO_ADD = moveIncrement / 2

        # Create matrix for this particular snake
        self.weightMatrixHiddenLayerOne, self.weightMatrixOutput = self.createWeightMatrix()

    def performance(self):
        # Should also track how many steps the snake did before dying
        pass

    # After each move, new calculations are made for new inputs
    def decision(self, snakePositions, foodPosition, direction):
        # check left, right and in front of snake
        inputVector = []

        ############################# Collision #############################
        inputVector.append(helper.checkLeft(snakePositions, self.MOVE_INCREMENT,
                                            self.BOARD_SIZE, self.TEXT_SIZE, direction))
        inputVector.append(helper.checkRight(snakePositions, self.MOVE_INCREMENT,
                                             self.BOARD_SIZE, self.TEXT_SIZE, direction))
        inputVector.append(helper.checkForward(snakePositions, self.MOVE_INCREMENT,
                                               self.BOARD_SIZE, self.TEXT_SIZE, direction))

        ############################# Angle -1 to 1 #############################
        # upper left corner of the snake's head
        snakeHeadX, snakeHeadY = snakePositions[0]
        # reminder: MOVE_INCREMENT is the size of food or snake picture
        # get the exact middle point of the picture in context of the coordiante system
        snakeHeadMidX = snakeHeadX + self.TO_ADD
        snakeHeadMidY = snakeHeadY + self.TO_ADD
        foodX, foodY = foodPosition
        foodXMid = foodX + self.TO_ADD
        foodYMid = foodY + self.TO_ADD
        inputVector.append(helper.calcDegree(snakeHeadMidX, snakeHeadMidY,
                                             foodXMid, foodYMid, direction))

        # Multiply the weight matrix with the input vector
        valuesHiddenLayer = np.dot(
            self.weightMatrixHiddenLayerOne, inputVector)
        valuesOutput = np.dot(self.weightMatrixOutput, valuesHiddenLayer)

        # Check which value is the biggest;
        # indexposition decides which action to take: 0 -> left; 1 -> right; 2 -> forward
        biggestValue = 0
        index = 0
        for i in range(valuesOutput.size):
            if valuesOutput[i] > biggestValue:
                biggestValue = valuesOutput[i]
                index = i
        switch = {0 : "Left",
                  1 : "Right",
                  2 : "Forward"}
        return helper.convertDirectionRelativeToSnake(direction, switch.get(index))
        # return self.matrix.dot(inputVector)

    # Create matrix with values between -1 and 1(exclusive)
    # Every row represents the weight of the connection between all neurons of the first layer
    # to a single neuron in the next.
    # NO BIAS
    def createWeightMatrix(self, neuronCountInputLayer=4, neuronCountHiddenLayerOne=6, outputNeurons=3):
        inputToHiddenOneWeights = (np.random.rand(neuronCountHiddenLayerOne,
                                                  neuronCountInputLayer) - 0.5) * 2
        hiddenOneToOutputWeights = (np.random.rand(outputNeurons,
                                                   neuronCountHiddenLayerOne) - 0.5) * 2
        return inputToHiddenOneWeights, hiddenOneToOutputWeights
