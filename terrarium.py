from dna import DNA
import random
import numpy as np


# Contains list of snakes and functions to find parents for further generations
class Terrarium():
    SNAKES = []

    def __init__(self, snakeCount, mutationChance, nnStructure, availableActivationFunctions, selectedFunctions):
        self.generationCount = snakeCount
        self.mutationChance = mutationChance
        # Initialise snakes and put them into a list
        for _ in range(self.generationCount):
            Terrarium.SNAKES.append(
                DNA(nnStructure, availableActivationFunctions, selectedFunctions))

    def getSnakeAt(self, index):
        return Terrarium.SNAKES[index]

    # Choosing the parents according to given ranks.
    # Each rank represents a chance (in %) to get chosen for a parent.
    # The sum of all the values added equals 100%
    def generateNextGeneration(self, ranks):
        sortedTerrarium = sorted(
            Terrarium.SNAKES, key=lambda snake: snake.fitnessValue, reverse=True)

        # Reformat the ranks so the chances are represented in sectors e.g. rank 1: 0 to 40; rank 2: 40 to 70; rank 3: 7 to 90; rank 4: 90 to 100
        # The input list is descending sorted and the output list is ascending sorted.
        formatedRanks = []
        for i in range(len(ranks)):
            if len(formatedRanks) == 0:
                formatedRanks.append(ranks[0])
            else:
                # Format values into an range from 0 to 99
                formatedRanks.append((formatedRanks[i-1] + ranks[i]))

        Terrarium.SNAKES = []

        # Select two different parents to "create" a child
        while len(Terrarium.SNAKES) != self.generationCount:
            parents = []
            while len(parents) < 2:
                randomNumber = random.randrange(100)  # Number between 0 - 99
                for rank in formatedRanks:
                    if randomNumber < rank and sortedTerrarium[formatedRanks.index(rank)] not in parents:
                        parents.append(
                            sortedTerrarium[formatedRanks.index(rank)])
                        break

            motherDNA = parents[0]
            fatherDNA = parents[1]
            # Uniform crossover
            childDNA = self.uniformCrossover(motherDNA, fatherDNA)

            # Create child with both matrixes
            Terrarium.SNAKES.append(DNA(motherDNA.neuralNetworkStructure,
                                        motherDNA.availableActivationFunctions, motherDNA.selectedFunctions, childDNA))

    def getTotalSnakeCount(self):
        return len(Terrarium.SNAKES)

    # For every Value in the matrix a value between 0 and 1.0 is generated.
    # If the generated value is under 0.5, the matrix value from the mother
    # (parents index 0) is taken, otherwise from the father (parents index 1).
    def uniformCrossover(self, motherDNA, fatherDNA):
        # Neural network contains all weights between input and output
        childDNA = []
        for matrixIndice in range(len(motherDNA.neuralNetwork)):
            childMatrix = np.copy(motherDNA.neuralNetwork[matrixIndice])
            for row in range(len(motherDNA.neuralNetwork[matrixIndice])):
                mutationOccured = False  # Allowing mutation per weight
                for col in range(len(motherDNA.neuralNetwork[matrixIndice][0])):
                    randomNumber = random.random()  # [0.0, 1.0)
                    if randomNumber < 0.5:
                        # Take "genes" from mother.
                        pass
                    else:
                        # Take "genes" from father.
                        childMatrix[row][col] = fatherDNA.neuralNetwork[matrixIndice][row][col]
                    # Mutation
                    mutationChance = random.random()
                    if mutationChance < self.mutationChance and not mutationOccured:
                        mutationOccured = True
                        childMatrix[row][col] = random.uniform(-1.0, 1.0)
                        continue
            childDNA.append(childMatrix)
        return childDNA
