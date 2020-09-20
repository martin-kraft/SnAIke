import random
import numpy as np
import snakeUtil
# Creates the population of snakes with their own DNA.
# DNA for each snake contains matrixes with float values between -1 to 1.

# 4 input neurons
# 0 or 1 if body part or wall on the left side of snake's head
#                                    right side
#                                    front
# and a value of sinus of angle on which the food is inclined relative to the snake
# every input also includes the direction in which the snake is moving


class DNA():
    def __init__(self, nnStructure, availableActivationFunctions, selectedFunctions, matrices=[]):
        self.fitnessValue = 0
        self.neuralNetworkStructure = nnStructure
        self.availableActivationFunctions = availableActivationFunctions
        self.selectedFunctions = selectedFunctions
        # Create matrix (brain) for this particular snake
        if len(matrices) == 0:
            # Random
            # self.weightMatrixHiddenLayerOne, self.weightMatrixOutput = self.createWeightMatrix()
            self.neuralNetwork = self.createNeuralNetwork()
        else:
            # Creating child with genes from parents
            self.neuralNetwork = matrices

        # Vectorize functions for later use
        self.preparedActivationFunctionList = self.prepareActivationFunctions()

    def fitness(self, score, steps):
        # self.fitnessValue = 2**score / steps
        self.fitnessValue = steps + \
            (2**score + score**2.1 * 500) - \
            abs(score**1.2 * (0.25 * steps)**1.3)

    # After each move, new calculations are made for new inputs

    def decision(self, snakePositions, foodPosition, direction, board):
        # check left, right and in front of snake
        self.inputVector = []

        ############################# Collision #############################
        self.inputVector.append(snakeUtil.checkLeft(snakePositions, board.MOVE_INCREMENT,
                                                    board.BOARD_SIZE, board.TEXT_SIZE, direction))
        self.inputVector.append(snakeUtil.checkRight(snakePositions, board.MOVE_INCREMENT,
                                                     board.BOARD_SIZE, board.TEXT_SIZE, direction))
        self.inputVector.append(snakeUtil.checkForward(snakePositions, board.MOVE_INCREMENT,
                                                       board.BOARD_SIZE, board.TEXT_SIZE, direction))

        ############################# Angle -1 to 1 #############################
        # upper left corner of the snake's head
        snakeHeadX, snakeHeadY = snakePositions[0]
        # reminder: MOVE_INCREMENT is the size of food or snake picture
        # get the exact middle point of the picture in context of the coordiante system
        toAdd = board.MOVE_INCREMENT / 2
        snakeHeadMidX = snakeHeadX + toAdd
        snakeHeadMidY = snakeHeadY + toAdd
        foodX, foodY = foodPosition
        foodXMid = foodX + toAdd
        foodYMid = foodY + toAdd
        self.inputVector.append(snakeUtil.calcDegree(snakeHeadMidX, snakeHeadMidY,
                                                     foodXMid, foodYMid, direction))
        # Propagate
        self.outputVector = self.propagate(self.inputVector)

        # Check which value is the biggest;
        # indexposition decides which action to take: 0 -> left; 1 -> right; 2 -> forward
        biggestValue = 0
        index = 0
        for i in range(len(self.outputVector)):
            if self.outputVector[i] > biggestValue:
                biggestValue = self.outputVector[i]
                index = i
        switch = {0: "Left",
                  1: "Forward",
                  2: "Right"}
        return snakeUtil.convertDirectionRelativeToSnake(direction, switch.get(index))

    # Taking a list of numbers which stand for the numbers of neurons for the specific layer.
    # First and last layers are always input and output layers respectively.
    # Every row represents the weight of the connection between all neurons of the first layer
    # to a single neuron in the next.
    # Returns list with numpy matrices.
    def createNeuralNetwork(self):
        matrices = []
        for i in range(1, len(self.neuralNetworkStructure)):
            matrices.append((np.random.rand(
                self.neuralNetworkStructure[i], self.neuralNetworkStructure[i-1]) - 0.5) * 2)
        return matrices

    def propagate(self, inputVector):
        result = []
        result.append(self.preparedActivationFunctionList[0](
            np.dot(self.neuralNetwork[0], inputVector)))

        for i in range(1, len(self.neuralNetwork)):
            result.append(self.preparedActivationFunctionList[i](
                np.dot(self.neuralNetwork[i], result[-1])))

        return result[-1]  # Output

    def prepareActivationFunctions(self):
        listWithFunctions = []
        # ["SIGMOID", "TANH", "RECTIFIER"]
        switch = {
            "SIGMOID": np.vectorize(snakeUtil.sigmmoid),
            "TANH": np.vectorize(snakeUtil.tanH),
            "RECTIFIER": np.vectorize(snakeUtil.rectified)
        }
        for func in self.selectedFunctions:
            listWithFunctions.append(switch.get(func))
        return listWithFunctions