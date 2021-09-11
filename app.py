import sys
import pygame
import random
from pygame.math import Vector2

randomNum = random.randrange(0, 10)
isRunning = True

def check_next_tile(snake, fruit):
    next_tile = snake.body[0] + snake.direction
    print(next_tile)
    
    # check wall
    if next_tile.x < 0 or next_tile.y < 0 or next_tile.x >= tile_number or next_tile.y >= tile_number:
        isRunning = False
        print("Hit wall, restart")

    # check fruit
    if next_tile == Vector2(fruit.x, fruit.y):
        snake.eat_fruit()
        print("Fruit eaten")
        fruit.respawn()

    # check body
    for v in snake.body:
        if v == next_tile:
            isRunning = False
            print("Hit body, restart")

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.fruit_eaten = 0
    
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * tile_size)
            y_pos = int(block.y * tile_size)
            block_rect = pygame.Rect(x_pos,y_pos,tile_size,tile_size)
            pygame.draw.rect(screen, (105, 56, 209),block_rect)

    def move_snake(self):
        if self.fruit_eaten > 0:
            body_copy = self.body[:]
            self.fruit_eaten -= 1
        else:
            body_copy = self.body[:-1]

        # Move the snake
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def eat_fruit(self):
        self.fruit_eaten += 1
        
        

class Fruit:
   def __init__(self):
       self.x = random.randrange(0, tile_number - 1) 
       self.y = random.randrange(0, tile_number - 1) 
       self.pos = Vector2(self.x * tile_size, self.y * tile_size)

   def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x, self.pos.y, tile_size, tile_size)
        pygame.draw.ellipse(screen, (255,0,0), fruit_rect)

   def respawn(self):
        self.x = random.randrange(0, tile_number - 1) 
        self.y = random.randrange(0, tile_number - 1)
        self.pos = Vector2(self.x * tile_size, self.y * tile_size) 


pygame.init()


tile_size = 50
tile_number = 19

clock = pygame.time.Clock()

screen = pygame.display.set_mode((tile_size * tile_number, tile_size * tile_number))

# Title and Icon
pygame.display.set_caption("The Very Hungry Snake")

fruit = Fruit()
snake = Snake()

# Updates the screen (moves snake) every update_timer milliseconds
update_timer = 200

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, update_timer)


while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            check_next_tile(snake, fruit)
            snake.move_snake()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DOWN) and (snake.direction != Vector2(0, -1)):
                snake.direction = Vector2(0, 1)
            if (event.key == pygame.K_UP) and (snake.direction != Vector2(0, 1)):
                snake.direction = Vector2(0, -1)
            if (event.key == pygame.K_RIGHT) and (snake.direction != Vector2(-1, 0)):
                snake.direction = Vector2(1, 0)
            if (event.key == pygame.K_LEFT) and (snake.direction != Vector2(1, 0)):
                snake.direction = Vector2(-1, 0)
            
    # Checker the board
    screen.fill((78, 168, 50))
    count = 0

    for i in range(tile_number):
        for j in range(tile_number):
            if count % 2 == 1:
                dark_tile = pygame.Surface((tile_size, tile_size))
                dark_tile.fill((0, 128, 0))
                screen.blit(dark_tile, (i * tile_size, j * tile_size))
            # print(str(i * tile_size) + ", " + str(j * tile_size)) # for printing coordinatees of the tiles
            count += 1
        

    fruit.draw_fruit()
    snake.draw_snake()
    pygame.display.update()
    clock.tick(60)
