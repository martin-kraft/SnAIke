import tkinter as tk
import tkinter.font
import os
import datetime
from dna import DNA
from stats import Stats
from terrarium import Terrarium
from random import randint
from PIL import Image, ImageTk

SCALE_FACTOR = 4
FILE_NAME = "Result.txt"


class Snake(tk.Canvas):
    # NN settings
    ACTIVATION_FUNCTIONS = ["SIGMOID", "TANH", "RECTIFIER"]
    SELECTED_FUNCTIONS = ["TANH", "TANH", "TANH"]
    NN_STRUCTURE = [4, 5, 3, 3]  # Input and output inclusive
    RANK_SECTORS = [30, 20, 15, 13, 10, 8, 4]
    SNAKES_PER_GENERATION = 100
    MUTATION_CHANCE = 0.05
    AI_ACTIVE = True

    # Debug if AI is deactivated
    # Possible options: "INPUT", "OUTPUT", "NN"
    PRINTOUT = [
        # "INPUT"
        # , "OUTPUT"
        # "NN"
    ]

    # Game settings
    MOVES_PER_SECOND = 1000
    GAME_SPEED = 1000 // MOVES_PER_SECOND
    MOVE_INCREMENT = 20  # size of the food and snake "picture" in pixels
    BOARD_SIZE = 20 * MOVE_INCREMENT
    TEXT_SIZE = 20
    BORDER_SIZE = 7
    GENERATION = 0
    ADDED_STEPS_AFTER_FOOD_IS_FOUND = 100

    def __init__(self, statsWindow):
        super().__init__(
            width=Snake.BOARD_SIZE,
            height=Snake.BOARD_SIZE + Snake.TEXT_SIZE,
            background="black",
            highlightthickness=0
        )
        date = datetime.datetime.now()
        setupText = f"{date}\nSetup:\nNN Structure: {Snake.NN_STRUCTURE}, Selected A.Functions: {Snake.SELECTED_FUNCTIONS}, Snakes per Generation: {Snake.SNAKES_PER_GENERATION}, Mutation chance: {Snake.MUTATION_CHANCE}\n"
        self.printToFile(setupText)

        # Stats window
        self.statsWindow = statsWindow

        # Initialise terrarium with specified number of snakes
        self.snakeCount = 0
        self.terrarium = Terrarium(Snake.SNAKES_PER_GENERATION, Snake.MUTATION_CHANCE,
                                   Snake.NN_STRUCTURE, Snake.ACTIVATION_FUNCTIONS, Snake.SELECTED_FUNCTIONS)
        self.currentSnake = self.terrarium.getSnakeAt(self.snakeCount)

        # First position is always the head
        self.snakePositions = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"  # starting position
        # Changes with key input; further information in on_key_press method
        self.notYetDirection = self.direction

        # Stats
        self.totalStepsGeneration = 0
        self.totalScoreGeneration = 0
        self.foodPosition = (100, 400)
        self.score = 0
        self.highScore = 0
        self.stepCount = 0

        # Max steps before the snake is killed; Increased if snake eats
        self.stepsUntilDeath = Snake.ADDED_STEPS_AFTER_FOOD_IS_FOUND

        self.loadAssets()
        self.createObjects()

        self.pack()
        self.after(Snake.GAME_SPEED, self.performActions)
        self.bind_all("<Key>", self.onKeyPress)

    def endGame(self):
        # Calculate fitness of current snake
        self.currentSnake.fitness(self.score, self.stepCount)
        if self.highScore < self.score:
            self.highScore = self.score

        # Check if snakes are available
        if self.snakeCount + 1 < Snake.SNAKES_PER_GENERATION:
            self.snakeCount += 1
        else:
            # All snakes played the game
            # Create children / next generation
            # self.terrarium.generateNextGeneration([40, 30, 20, 10])
            self.terrarium.generateNextGeneration(self.RANK_SECTORS)
            roundedTotalScorePerSnake = "{:.2f}".format(
                self.totalScoreGeneration / (self.terrarium.getTotalSnakeCount()))

            textToInsert = f"Generation: {str(Snake.GENERATION+1).ljust(5)} H.Score: {str(self.highScore).ljust(5)} Food/Snake: {roundedTotalScorePerSnake}"
            self.statsWindow.add(textToInsert)
            self.printToFile(textToInsert + "\n")
            Snake.GENERATION += 1
            self.snakeCount = 0
            self.highScore = 0
            self.totalScoreGeneration = 0
            self.totalStepsGeneration = 0
            Snake.INITIAL_SNAKE_COUNT = self.terrarium.getTotalSnakeCount()

            # self.delete(tk.ALL)
            # self.create_text(
            #     self.winfo_width() / 2,
            #     self.winfo_height() / 2,
            #     text="No Snakes available in the terrarium!",
            #     fill="#fff",
            #     font=("", 5)
            # )
            # return False

        # Select new snake
        self.currentSnake = self.terrarium.getSnakeAt(self.snakeCount)

        # Prepare board for the next snake
        self.delete("snake")
        self.snakePositions = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.notYetDirection = self.direction
        self.createSnake()
        self.totalScoreGeneration += self.score
        self.totalStepsGeneration += self.stepCount
        self.score = 0
        self.stepCount = 0
        self.stepsUntilDeath = Snake.ADDED_STEPS_AFTER_FOOD_IS_FOUND
        # Update scores
        self.createScore()

        return True

    def onKeyPress(self, e):
        # This function can be called multiple times before an actual position change of the
        # snake occured. Therefore a new class variable self.notYetDirection is needed.
        newDirection = e.keysym

        allDirections = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (newDirection in allDirections and {newDirection, self.direction} not in opposites):
            self.notYetDirection = newDirection

    def checkCollisions(self):
        headXPosition, headYPosition = self.snakePositions[0]

        return (
            headXPosition in (0, self.BOARD_SIZE)
            or headYPosition in (Snake.TEXT_SIZE, Snake.BOARD_SIZE + Snake.TEXT_SIZE)
            or (headXPosition, headYPosition) in self.snakePositions[1:]
        )

    def checkFoodCollision(self):
        if self.snakePositions[0] == self.foodPosition:
            self.score += 1
            self.snakePositions.append(self.snakePositions[-1])
            self.create_image(
                *self.snakePositions[-1], image=self.snakeBody, tag="snake"
            )

            self.foodPosition = self.setNewFoodPosition()
            self.coords(self.find_withtag("food"), *self.foodPosition)

            self.stepsUntilDeath += Snake.ADDED_STEPS_AFTER_FOOD_IS_FOUND

    def moveSnake(self, nextComputerMove=None):
        headX, headY = self.snakePositions[0]

        # Check for computer input
        if nextComputerMove:
            if nextComputerMove != "Forward":
                self.notYetDirection = nextComputerMove

        # Human player and computer inputs
        if self.notYetDirection == "Left" or nextComputerMove == "Left":
            newHeadPosition = (
                headX - Snake.MOVE_INCREMENT, headY)
        elif self.notYetDirection == "Right" or nextComputerMove == "Right":
            newHeadPosition = (
                headX + Snake.MOVE_INCREMENT, headY)
        elif self.notYetDirection == "Down" or nextComputerMove == "Down":
            newHeadPosition = (
                headX, headY + Snake.MOVE_INCREMENT)
        elif self.notYetDirection == "Up" or nextComputerMove == "Up":
            newHeadPosition = (
                headX, headY - Snake.MOVE_INCREMENT)

        self.snakePositions = [newHeadPosition] + self.snakePositions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snakePositions):
            # update coords for each snake segment
            self.coords(segment, position)

        self.direction = self.notYetDirection  # update the actual direction
        self.stepCount += 1

    def setNewFoodPosition(self):
        while True:
            # xPosition = randint(
            #     1, BOARD_SIZE / MOVE_INCREMENT-1) * MOVE_INCREMENT
            # yPosition = randint(
            #     3, BOARD_SIZE / MOVE_INCREMENT) * MOVE_INCREMENT
            boardPanelsInXAndY = Snake.BOARD_SIZE / Snake.MOVE_INCREMENT
            xPosition = randint(Snake.TEXT_SIZE / Snake.MOVE_INCREMENT,
                                boardPanelsInXAndY - 1) * Snake.MOVE_INCREMENT
            yPosition = randint(Snake.TEXT_SIZE / Snake.MOVE_INCREMENT + 1,
                                boardPanelsInXAndY) * Snake.MOVE_INCREMENT
            foodPosition = (xPosition, yPosition)

            if foodPosition not in self.snakePositions:
                return foodPosition

    def performActions(self):
        shouldRun = True
        if self.checkCollisions() or self.stepCount == self.stepsUntilDeath:
            shouldRun = self.endGame()

        nextDecision = self.currentSnake.decision(
            self.snakePositions, self.foodPosition, self.direction, self)
        if not Snake.AI_ACTIVE:
            nextDecision = None
            Snake.GAME_SPEED = 250
            self.debug()

        self.moveSnake(nextDecision)
        self.checkFoodCollision()
        self.createScore()
        if shouldRun:  # TODO: MAINLOOP STILL RUNS
            self.after(Snake.GAME_SPEED, self.performActions)

    def loadAssets(self):
        try:
            self.snakeBodyImage = Image.open("./assets/snake.png")
            self.snakeBody = ImageTk.PhotoImage(self.snakeBodyImage)

            self.foodImage = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.foodImage)
        except IOError as error:
            print(error)
            root.destroy()

    def createObjects(self):
        self.createOutline()
        self.createScore()
        self.createSnake()
        self.createFood()

    def createScore(self):
        score = self.find_withtag("score")
        textToInsert = f"Score: {str(self.score).ljust(2)} H.score: {str(self.highScore).ljust(2)} S.Nr.: {str(self.snakeCount+1).ljust(3)}/{str(Snake.SNAKES_PER_GENERATION)} Gen.: {str(Snake.GENERATION+1).ljust(2)}"
        if len(score) == 0:
            self.create_text(
                # fff",
                190, 12, text=textToInsert, tag="score", fill="#fff"
            )
        else:
            self.itemconfigure(
                score,
                text=textToInsert, tag="score")

    def createOutline(self):
        self.create_rectangle(Snake.BORDER_SIZE, Snake.TEXT_SIZE + Snake.BORDER_SIZE, Snake.BOARD_SIZE -
                              Snake.BORDER_SIZE, Snake.BOARD_SIZE + Snake.TEXT_SIZE - Snake.BORDER_SIZE, outline="#525d69")

    def createSnake(self):
        for xPosition, yPosition in self.snakePositions:
            self.create_image(xPosition, yPosition,
                              image=self.snakeBody, tag="snake")

    def createFood(self):
        self.create_image(*self.foodPosition, image=self.food, tag="food")

    def debug(self):
        if "INPUT" in Snake.PRINTOUT:
            print("input vector: ", self.currentSnake.inputVector)
        if "OUTPUT" in Snake.PRINTOUT:
            print("output vector: ", self.currentSnake.outputVector)
        if "NN" in Snake.PRINTOUT:
            print("NN: ", self.currentSnake.neuralNetwork)

    # Printing into a text file at the start and after each generation.
    def printToFile(self, toWrite):
        if os.path.exists(FILE_NAME):
            append_write = "a"  # append if already exists
        else:
            append_write = "w"  # make a new file if not

        f = open(FILE_NAME, append_write)
        f.write(toWrite)
        f.close()


root = tk.Tk()
root.title("SnAIke")
root.resizable(False, False)
root.tk.call("tk", "scaling", SCALE_FACTOR)
root.configure(bg="black")

stats = Stats(root, Snake.BOARD_SIZE - 30, 75)
board = Snake(stats)

root.lift()
root.attributes("-topmost", True)
root.mainloop()
# Print newline to file for better readability
board.printToFile("\n")
