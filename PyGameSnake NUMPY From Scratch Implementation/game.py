import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)  # Set the font for the game

# Define the directions as an Enum for better readability
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')  # Define a point with x and y coordinates

# Define some color constants
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20  # Size of each block in the game
SPEED = 4000  # Speed of the game

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w  # Width of the game window
        self.h = h  # Height of the game window
        # Initialize the game display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')  # Set the window title
        self.clock = pygame.time.Clock()  # Initialize a clock for controlling the speed of the game
        self.reset()  # Reset the game state

    def reset(self):
        # Initialize the game state
        self.direction = Direction.RIGHT  # The initial direction of the snake
        self.head = Point(self.w/2, self.h/2)  # The initial position of the snake's head
        # The initial body of the snake, including the head and two body segments
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0  # The initial score
        self.food = None  # The initial food position
        self._place_food()  # Place the first food
        self.frame_iteration = 0  # The initial frame iteration

    def _place_food(self):
        # Place a food at a random position
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:  # If the food is placed inside the snake's body, place it again
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1  # Increase the frame iteration
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user wants to quit the game, quit the game
                pygame.quit()
                quit()
        
        # 2. move the snake according to the action
        self._move(action)  # update the head
        self.snake.insert(0, self.head)  # Add the new head to the snake's body
        
        # 3. check if game over
        reward = 0
        game_over = False
        # If the snake hits the boundary or its own body, or the frame iteration exceeds a limit, the game is over
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10  # Give a negative reward for game over
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:  # If the snake eats the food
            self.score += 1  # Increase the score
            reward = 10  # Give a positive reward for eating the food
            self._place_food()  # Place a new food
        else:  # If the snake does not eat the food, remove the tail
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()  # Update the game display
        self.clock.tick(SPEED)  # Control the speed of the game
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Check if the snake hits the boundary or its own body
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)  # Fill the background with black

        # Draw the snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        # Draw the food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Display the score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()  # Update the game display

    def _move(self, action):
        # Move the snake according to the action
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        # Determine the new direction based on the action
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        # Move the head to the new direction
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)  # Update the head position