import tkinter as tk
import tkinter.font
from dna import DNA
from terrarium import Terrarium
from random import randint
from PIL import Image, ImageTk

SCALE_FACTOR = 4


class Snake(tk.Canvas):
    MOVE_INCREMENT = 20  # size of the food and snake "picture"
    MOVES_PER_SECOND = 200
    GAME_SPEED = 1000 // MOVES_PER_SECOND
    BOARD_SIZE = 20 * MOVE_INCREMENT
    TEXT_SIZE = 20
    BORDER_SIZE = 7
    INITIAL_SNAKE_COUNT = 2000
    GENERATION = 0

    def __init__(self):
        super().__init__(
            width=Snake.BOARD_SIZE,
            height=Snake.BOARD_SIZE + Snake.TEXT_SIZE,
            background="black",
            highlightthickness=0
        )
        # Initialise terrarium with specified number of snakes
        self.snakeCount = 0
        self.terrarium = Terrarium(Snake.INITIAL_SNAKE_COUNT)
        self.currentSnake = self.terrarium.getSnakeAt(self.snakeCount)

        # First position is always the head
        self.snakePositions = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"  # starting position
        # Changes with key input; further information in on_key_press method
        self.notYetDirection = self.direction

        # self.foodPosition = self.setNewFoodPosition()
        self.foodPosition = (100, 400)
        self.score = 0
        self.highScore = 0
        self.stepCount = 0

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
        if self.snakeCount + 1 < Snake.INITIAL_SNAKE_COUNT:
            self.snakeCount += 1
        else:
            # All snakes played the game
            # Create children
            self.terrarium.generateNextGeneration([40, 30, 20, 10])
            Snake.GENERATION += 1
            self.snakeCount = 0
            self.highScore = 0
            Snake.INITIAL_SNAKE_COUNT = self.terrarium.getTotalSnakeCount()
            # self.currentSnake = self.terrarium.getSnakeAt(0)

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

        # Reset playing field
        self.delete("snake")
        self.snakePositions = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.notYetDirection = self.direction
        self.createSnake()
        self.score = 0
        self.stepCount = 0
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
        if self.checkCollisions() or self.stepCount == 300:
            shouldRun = self.endGame()

        nextDecision = self.currentSnake.decision(
            self.snakePositions, self.foodPosition, self.direction, self)
        self.moveSnake(nextDecision)
        self.checkFoodCollision()
        self.createScore()
        if shouldRun:  # TODO: MAINLOOP LÄUFT IMMER NOCH WEITER!
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
        if len(score) == 0:
            self.create_text(
                # fff",
                190, 12, text=f"Score: {self.score} H.score: {self.highScore} SnakeNr: {self.snakeCount+1}/{Snake.INITIAL_SNAKE_COUNT} Gen.: {Snake.GENERATION+1} S.count: {self.stepCount}", tag="score", fill="#fff"
            )
        else:
            self.itemconfigure(
                score, text=f"Score: {self.score} H.score: {self.highScore} SnakeNr: {self.snakeCount+1}/{Snake.INITIAL_SNAKE_COUNT} Gen.: {Snake.GENERATION+1} S.count: {self.stepCount}", tag="score")

    def createOutline(self):
        self.create_rectangle(Snake.BORDER_SIZE, Snake.TEXT_SIZE + Snake.BORDER_SIZE, Snake.BOARD_SIZE -
                              Snake.BORDER_SIZE, Snake.BOARD_SIZE + Snake.TEXT_SIZE - Snake.BORDER_SIZE, outline="#525d69")

    def createSnake(self):
        for xPosition, yPosition in self.snakePositions:
            self.create_image(xPosition, yPosition,
                              image=self.snakeBody, tag="snake")

    def createFood(self):
        self.create_image(*self.foodPosition, image=self.food, tag="food")


root = tk.Tk()
root.title("SnAIke")
root.resizable(False, False)
root.tk.call("tk", "scaling", SCALE_FACTOR)

board = Snake()

root.lift()
root.attributes("-topmost", True)
root.mainloop()
