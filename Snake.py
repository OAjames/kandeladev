# Snake game using pyglet
# Run: python Snake.py

import pyglet
import random
from pyglet import shapes

# Configuration
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10
SNAKE_INITIAL_LENGTH = 5
BG_COLOR = (18, 18, 18)
SNAKE_COLOR = (0, 200, 0)
FOOD_COLOR = (200, 50, 50)
GRID_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)

class SnakeGame:
    def __init__(self):
        self.window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game")
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press
        
        # Initialize snake
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.snake = [(start_x - i, start_y) for i in range(SNAKE_INITIAL_LENGTH)]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.food = self.random_food_position()
        self.game_over = False
        self.score = 0
        
        # Schedule game update
        pyglet.clock.schedule_interval(self.update, 1.0 / FPS)
    
    def random_food_position(self):
        while True:
            pos = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
            if pos not in self.snake:
                return pos
    
    def on_key_press(self, symbol, modifiers):
        # Handle arrow keys or WASD
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
            if self.direction != (0, -1):
                self.next_direction = (0, 1)
        elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
            if self.direction != (0, 1):
                self.next_direction = (0, -1)
        elif symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            if self.direction != (1, 0):
                self.next_direction = (-1, 0)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            if self.direction != (-1, 0):
                self.next_direction = (1, 0)
        elif symbol == pyglet.window.key.SPACE:
            if self.game_over:
                self.__init__()
    
    def update(self, dt):
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check collisions with walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # Check collision with itself
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.random_food_position()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def on_draw(self):
        self.window.clear()
        
        # Draw snake
        batch = pyglet.graphics.Batch()
        for segment in self.snake:
            rect = shapes.Rectangle(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, 
                                   CELL_SIZE, CELL_SIZE, color=SNAKE_COLOR, batch=batch)
        
        # Draw food
        food_rect = shapes.Rectangle(self.food[0] * CELL_SIZE, self.food[1] * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE, color=FOOD_COLOR, batch=batch)
        
        batch.draw()
        
        # Draw score
        label = pyglet.text.Label(f'Score: {self.score}', 
                                   font_size=14,
                                   x=10, y=SCREEN_HEIGHT - 25,
                                   color=(*TEXT_COLOR, 255))
        label.draw()
        
        # Draw game over message
        if self.game_over:
            game_over_label = pyglet.text.Label('GAME OVER - Press SPACE to restart',
                                                 font_size=16,
                                                 x=SCREEN_WIDTH // 2, 
                                                 y=SCREEN_HEIGHT // 2,
                                                 anchor_x='center', anchor_y='center',
                                                 color=(255, 0, 0, 255))
            game_over_label.draw()
    
    def run(self):
        pyglet.app.run()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()