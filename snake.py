import tkinter as tk
import tkinter.font
from dna import DNA
from random import randint
from PIL import Image, ImageTk

SCALE_FACTOR = 4
MOVE_INCREMENT = 20  # size of the food and snake "picture"
MOVES_PER_SECOND = 3
GAME_SPEED = 1000 // MOVES_PER_SECOND
BOARD_SIZE = 20 * MOVE_INCREMENT
TEXT_SIZE = 20
BORDER_SIZE = 7


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=BOARD_SIZE,
            height=BOARD_SIZE + TEXT_SIZE,
            background="black",
            highlightthickness=0
        )
        # First position is always the head
        self.snakePositions = [(100, 100), (80, 100), (60, 100)]

        self.foodPosition = self.setNewFoodPosition()
        self.score = 0
        self.stepCount = 0

        self.loadAssets()
        self.createObjects()

        self.pack()

        self.after(GAME_SPEED, self.performActions)

        self.direction = "Right"  # starting position
        # Changes with key input; further information in on_key_press method
        self.notYetDirection = self.direction
        self.bind_all("<Key>", self.onKeyPress)

        # *** DNA ***
        self.dna = DNA(BOARD_SIZE, TEXT_SIZE, MOVE_INCREMENT)

    def reset(self):
        pass

    def endGame(self):
        self.delete(tk.ALL)
        # self.create_text(
        #     self.winfo_width() / 2,
        #     self.winfo_height() / 2,
        #     text=f"Game over! You scored {self.score}!",
        #     fill="#fff",
        #     font=("", 10)
        # )
        return self.score, self.stepCount

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
            headXPosition in (0, BOARD_SIZE)
            or headYPosition in (TEXT_SIZE, BOARD_SIZE + TEXT_SIZE)
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

            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    def moveSnake(self, nextComputerMove):
        headX, headY = self.snakePositions[0]

        # Check for computer input 
        if nextComputerMove:
            if nextComputerMove != "Forward":
                self.notYetDirection = nextComputerMove

        # Human player and computer inputs 
        if self.notYetDirection == "Left" or nextComputerMove == "Left":
            newHeadPosition = (
                headX - MOVE_INCREMENT, headY)
        elif self.notYetDirection == "Right" or nextComputerMove == "Right":
            newHeadPosition = (
                headX + MOVE_INCREMENT, headY)
        elif self.notYetDirection == "Down" or nextComputerMove == "Down":
            newHeadPosition = (
                headX, headY + MOVE_INCREMENT)
        elif self.notYetDirection == "Up" or nextComputerMove == "Up":
            newHeadPosition = (
                headX, headY - MOVE_INCREMENT)
        elif nextComputerMove == "Forward":
            pass # Just keep the snake moving where it is already heading

        self.snakePositions = [newHeadPosition] + self.snakePositions[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snakePositions):
            # update coords for each snake segment
            self.coords(segment, position)

        self.direction = self.notYetDirection  # update the actual direction

    def setNewFoodPosition(self):
        while True:
            # xPosition = randint(
            #     1, BOARD_SIZE / MOVE_INCREMENT-1) * MOVE_INCREMENT
            # yPosition = randint(
            #     3, BOARD_SIZE / MOVE_INCREMENT) * MOVE_INCREMENT
            boardPanelsInXAndY = BOARD_SIZE / MOVE_INCREMENT
            xPosition = randint(TEXT_SIZE / MOVE_INCREMENT,
                                boardPanelsInXAndY - 1) * MOVE_INCREMENT
            yPosition = randint(TEXT_SIZE / MOVE_INCREMENT + 1,
                                boardPanelsInXAndY) * MOVE_INCREMENT
            foodPosition = (xPosition, yPosition)

            if foodPosition not in self.snakePositions:
                return foodPosition

    def performActions(self):
        if self.checkCollisions():
            self.endGame()

        nextDecision = self.dna.decision(self.snakePositions, self.foodPosition, self.direction)
        print(nextDecision)
        self.moveSnake(nextDecision)
        self.checkFoodCollision()
        self.after(GAME_SPEED, self.performActions)

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
        # textSize = tk.font.Font().measure("Score:  ")  # runs on mac correctly
        self.create_text(
            35, 12, text=f"Score: {self.score}", tag="score", fill="#fff",
        )

        for xPosition, yPosition in self.snakePositions:
            self.create_image(xPosition, yPosition,
                              image=self.snakeBody, tag="snake")
        self.create_image(*self.foodPosition, image=self.food, tag="food")
        self.create_rectangle(BORDER_SIZE, TEXT_SIZE + BORDER_SIZE, BOARD_SIZE -
                              BORDER_SIZE, BOARD_SIZE + TEXT_SIZE - BORDER_SIZE, outline="#525d69")


root = tk.Tk()
root.title("SnAIke")
root.resizable(False, False)
root.tk.call("tk", "scaling", SCALE_FACTOR)
root.lift()

board = Snake()
board.after(GAME_SPEED)

root.mainloop()
