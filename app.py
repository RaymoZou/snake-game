import sys
import pygame
import random
from pygame.math import Vector2

randomNum = random.randrange(0, 10)

# class SNAKE:
#     def __init__(self):
#         self.body = 

class Fruit:
   def __init__(self):
       self.x = random.randrange(0,tile_number-1) * tile_size
       self.y = random.randrange(0,tile_number-1) * tile_size
       self.pos = Vector2(self.x,self.y)

   def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x, self.pos.y, tile_size, tile_size)
        pygame.draw.rect(screen, (255,0,0), fruit_rect)



pygame.init()

isRunning = True
tile_size = 50
tile_number = 19

clock = pygame.time.Clock()

screen = pygame.display.set_mode((tile_size * tile_number, tile_size * tile_number))
screen.fill((78, 168, 50))

# Checker the board
count = 0

for i in range(tile_number):
    for j in range(tile_number):
        if count % 2 == 1:
            dark_tile = pygame.Surface((tile_size, tile_size))
            dark_tile.fill((0, 128, 0))
            screen.blit(dark_tile, (i * tile_size, j * tile_size))
        # print(str(i * tile_size) + ", " + str(j * tile_size))
        count += 1

# Title and Icon
pygame.display.set_caption("The Very Hungry Snake")

fruit = Fruit()

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fruit.draw_fruit()

    pygame.display.update()
    clock.tick(60)
