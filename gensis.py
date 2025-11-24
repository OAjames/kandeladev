# gensis.py - simple Snake game using pygame
# Run: python gensis.py

import pygame
import random

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

def draw_rect(surface, color, pos):
  r = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
  pygame.draw.rect(surface, color, r)

def random_food_position(snake):
  while True:
    pos = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
    if pos not in snake:
      return pos

def show_text(surface, text, size, y_offset=0):
  font = pygame.font.SysFont(None, size)
  surf = font.render(text, True, TEXT_COLOR)
  rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
  surface.blit(surf, rect)

def game_loop(screen, clock):
  # Initialize snake centered and going right
  start_x = GRID_WIDTH // 2
  start_y = GRID_HEIGHT // 2
  snake = [(start_x - i, start_y) for i in range(SNAKE_INITIAL_LENGTH)]
  direction = (1, 0)