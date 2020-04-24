from dna import DNA
from random import random
import numpy as np


# Contains list of snakes and functions to find parents for further generations
class Terrarium():
    SNAKES = []
    MUTATION_CHANCE = 0.05
    NEXTGEN_COUNT = 2000

    def __init__(self, snakeCount):
        # Initialise snakes and put them into a list
        for _ in range(snakeCount):
            Terrarium.SNAKES.append(DNA())

    def getSnakeAt(self, index):
        return Terrarium.SNAKES[index]

    # Choosing the parents according to given ranks.
    # Each rank represents a chance (in %) to get chosen for a parent.
    # The sum of all the values added equals 100%
    def generateNextGeneration(self, ranks):
        sortedTerrarium = sorted(
            Terrarium.SNAKES, key=lambda snake: snake.fitnessValue, reverse=True)

        # Reformat the ranks so the chances are represented in sectors e.g. rank 1: 0-0.4; rank 2: 0.4-0.7; rank 3: 0.7-0.9; rank 4: 0.9-1.0
        # The input list is descending sorted and the output list is ascending sorted.
        formatedRanks = []
        for i in range(len(ranks)):
            if len(formatedRanks) == 0:
                formatedRanks.append(ranks[0])
            else:
                # Format values into an range from 0.0 to 1.0
                formatedRanks.append((formatedRanks[i-1] + ranks[i]))

        Terrarium.SNAKES = []
        while len(Terrarium.SNAKES) != Terrarium.NEXTGEN_COUNT:
            # Select two different parents
            parents = []
            while len(parents) < 2:
                randomNumber = random() * 100  # Number between 0 - 100
                for rank in formatedRanks:
                    if randomNumber <= rank and sortedTerrarium[formatedRanks.index(rank)] not in parents:
                        parents.append(
                            sortedTerrarium[formatedRanks.index(rank)])
                        break

            # Uniform crossover
            # For every Value in the matrix a value between 0 and 1.0 is generated.
            # If the generated value is under 0.5, the matrix value from the mother
            # (parents index 0) is taken, otherwise from the father (parents index 1).
            mother = parents[0]
            father = parents[1]
            matrixOneMother = mother.weightMatrixHiddenLayerOne
            matrixTwoMother = mother.weightMatrixOutput
            matrixOneFather = father.weightMatrixHiddenLayerOne
            matrixTwoFather = father.weightMatrixOutput

            # Create the first matrix for the child
            childMatrixOne = np.copy(matrixOneMother)
            for row in range(len(matrixOneMother)):
                for col in range(len(matrixOneMother[0])):
                    randomNumber = random()  # Number between 0.0 - 1.0
                    if randomNumber < 0.5:
                        # Mutation
                        if randomNumber < Terrarium.MUTATION_CHANCE:
                            childMatrixOne[row][col] = random()
                        else:
                            # Take "genes" from mother.
                            childMatrixOne[row][col] = matrixOneMother[row][col]
                    else:
                        # Mutation
                        if randomNumber < Terrarium.MUTATION_CHANCE:
                            childMatrixOne[row][col] = random()
                        else:
                            # Take "genes" from father.
                            childMatrixOne[row][col] = matrixOneFather[row][col]

            # Create the second matrix for the child
            childMatrixTwo = np.copy(matrixTwoMother)
            for row in range(len(matrixTwoMother)):
                for col in range(len(matrixTwoMother[0])):
                    randomNumber = random()  # Number between 0.0 - 1.0
                    if randomNumber < 0.5:
                        # Mutation
                        if randomNumber < Terrarium.MUTATION_CHANCE:
                            childMatrixTwo[row][col] = random()
                        # Take "genes" from mother.
                        else:
                            childMatrixTwo[row][col] = matrixTwoMother[row][col]
                    else:
                        # Mutation
                        if randomNumber < Terrarium.MUTATION_CHANCE:
                            childMatrixTwo[row][col] = random()
                        else:
                            #  Take "genes" from father.
                            childMatrixTwo[row][col] = matrixTwoFather[row][col]

            # Create child with both matrixes
            Terrarium.SNAKES.append(DNA(childMatrixOne, childMatrixTwo))

    def getTotalSnakeCount(self):
        return len(Terrarium.SNAKES)
