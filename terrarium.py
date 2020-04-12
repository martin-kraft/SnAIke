from dna import DNA

# Contains list of snakes and functions to find parents for further generations


class Terrarium():
    SNAKES = []

    def __init__(self, snakeCount):
        # Initialise snakes and put them into a list
        for _ in range(snakeCount):
            Terrarium.SNAKES.append(DNA())

    def getSnakeAt(self, index):
        return Terrarium.SNAKES[index]

    # Choosing the parents according to given ranks.
    # Each rank represents a chance (in %) to get chosen for a parent.
    def rankSelection(self, ranks):
        sortedTerrarium = sorted(
            Terrarium.SNAKES, key=lambda snake: snake.fitnessValue, reverse=True)

        snakePercentage = {}
        for i in range(len(ranks)):
            snakePercentage.update({sortedTerrarium[i]: ranks[i]})

        generate
