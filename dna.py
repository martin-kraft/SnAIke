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
    def __init__(self, childMatrixOne=[], childMatrixTwo=[]):
        self.fitnessValue = 0

        # Create matrix (brain) for this particular snake
        if len(childMatrixOne) == 0:
            # Random
            self.weightMatrixHiddenLayerOne, self.weightMatrixOutput = self.createWeightMatrix()
        else:
            # Creating child with genes from parents
            self.weightMatrixHiddenLayerOne = childMatrixOne
            self.weightMatrixOutput = childMatrixTwo

        # Vectorize functions for later use
        self.vectorizedSigmoid = np.vectorize(snakeUtil.sigmmoid)
        self.vectorizedRectifier = np.vectorize(snakeUtil.rectified)
        self.vectorizedTanH = np.vectorize(snakeUtil.tanH)

    def fitness(self, score, steps):
        self.fitnessValue = 2**score / steps

    # After each move, new calculations are made for new inputs
    def decision(self, snakePositions, foodPosition, direction, board):
        # check left, right and in front of snake
        inputVector = []

        ############################# Collision #############################
        inputVector.append(snakeUtil.checkLeft(snakePositions, board.MOVE_INCREMENT,
                                               board.BOARD_SIZE, board.TEXT_SIZE, direction))
        inputVector.append(snakeUtil.checkRight(snakePositions, board.MOVE_INCREMENT,
                                                board.BOARD_SIZE, board.TEXT_SIZE, direction))
        inputVector.append(snakeUtil.checkForward(snakePositions, board.MOVE_INCREMENT,
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
        inputVector.append(snakeUtil.calcDegree(snakeHeadMidX, snakeHeadMidY,
                                                foodXMid, foodYMid, direction))
        # Multiply the weight matrix with the input vector
        valuesHiddenLayer = np.dot(
            inputVector, self.weightMatrixHiddenLayerOne)
        # Apply sigmoid
        self.vectorizedSigmoid(valuesHiddenLayer)
        valuesOutput = np.dot(valuesHiddenLayer, self.weightMatrixOutput)
        # Apply sigmoid
        self.vectorizedSigmoid(valuesOutput)
        print("input: \n", inputVector)
        # print("weight: \n", self.weightMatrixHiddenLayerOne)
        # print("weight x input: \n", valuesHiddenLayer)
        # print("weightMatrixOutput: \n", self.weightMatrixOutput)
        # print("VALUESOUTPUT: \n", valuesOutput)

        # Check which value is the biggest;
        # indexposition decides which action to take: 0 -> left; 1 -> right; 2 -> forward
        biggestValue = 0
        index = 0
        for i in range(valuesOutput.size):
            if valuesOutput[i] > biggestValue:
                biggestValue = valuesOutput[i]
                index = i
        switch = {0: "Left",
                  1: "Right",
                  2: "Forward"}
        return snakeUtil.convertDirectionRelativeToSnake(direction, switch.get(index))

    # Create matrix with values between -1 and 1(exclusive)
    # Every row represents the weight of the connection between all neurons of the first layer
    # to a single neuron in the next.
    # NO BIAS
    def createWeightMatrix(self, neuronCountInputLayer=4, neuronCountHiddenLayerOne=6, outputNeurons=3):
        inputToHiddenOneWeights = (np.random.rand(neuronCountInputLayer,
                                                  neuronCountHiddenLayerOne) - 0.5) * 2
        hiddenOneToOutputWeights = (np.random.rand(neuronCountHiddenLayerOne,
                                                   outputNeurons) - 0.5) * 2
        return inputToHiddenOneWeights, hiddenOneToOutputWeights

    # Taking a list of numbers which stand for the numbers of neurons for the specific layer.
    # First and last layers are always input and output layers respectively.
    def createNN(self, list):
        pass
