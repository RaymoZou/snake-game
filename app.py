import sys
import pygame
import random
from pygame.math import Vector2
from pygame import mixer

#pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()

# global isRunning
isRunning = True
gameIsOver = False

# sprites
apple_image = pygame.image.load("./apple.png")
banana_image = pygame.image.load("./banana.png")
pineapple_image = pygame.image.load("./pineapple.png")
watermelon_image = pygame.image.load("./watermelon.png")
eye_image = pygame.image.load("./eye.png")
eye_rotate = pygame.transform.rotate(eye_image, 90)
tongue_image = pygame.image.load("./tongue.png")

# sounds
#Background Music
pygame.mixer.music.set_volume(0.05)
mixer.music.load('2_23_AM.mp3')
mixer.music.play(-1)


fruits = [apple_image, banana_image, pineapple_image, watermelon_image]

def check_next_tile(snake, fruit):
    global gameIsOver
    next_tile = snake.body[0] + snake.direction
    # print(next_tile)
    
    # check wall
    if next_tile.x < 0 or next_tile.y < 0 or next_tile.x >= tile_number or next_tile.y >= tile_number:
        gameIsOver = True
        snake.play_death_sound()
        # print("Hit wall, restart")
        # print(gameIsOver)

    # check body
    for v in snake.body:
        if v == next_tile:
            snake.play_death_sound()
            # print("Hit body, restart")
            gameIsOver = True

    # check fruit
    if next_tile == Vector2(fruit.x, fruit.y):
        snake.eat_fruit()
        # print("Fruit eaten")
        fruit.respawn()
        snake.play_eat_sound()

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.fruit_eaten = 0
        self.eat_sound = pygame.mixer.Sound('./eat_sound.wav')
        self.death_sound = pygame.mixer.Sound('./death_sound.wav')
    
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * tile_size)
            y_pos = int(block.y * tile_size)
            block_rect = pygame.Rect(x_pos,y_pos,tile_size,tile_size)
            pygame.draw.rect(screen, (105, 56, 209), block_rect)
            if block == self.body[0]:
                if snake.direction == Vector2(0, -1): # snake is moving up
                    leftEye = pygame.Rect(x_pos - 6 - tile_size / 2, y_pos - tile_size / 2, tile_size / 3, tile_size / 3)
                    rightEye = pygame.Rect(x_pos - 6 + tile_size / 2, y_pos - tile_size / 2, tile_size / 3, tile_size / 3)
                    screen.blit(eye_image, leftEye)
                    screen.blit(eye_image, rightEye)
                    
                    tongue_rect = pygame.Rect(x_pos, y_pos - tile_size, tile_size / 3, tile_size / 3)
                    screen.blit(tongue_image, tongue_rect)

                if snake.direction == Vector2(0, 1): # snake is moving down
                    leftEye = pygame.Rect(x_pos - 6 - tile_size / 2, y_pos - tile_size / 2, tile_size / 3, tile_size / 3)
                    rightEye = pygame.Rect(x_pos - 6 + tile_size / 2, y_pos - tile_size / 2, tile_size / 3, tile_size / 3)
                    screen.blit(eye_image, leftEye)
                    screen.blit(eye_image, rightEye)
                    
                    tongue_down = pygame.transform.rotate(tongue_image, 180)
                    tongue_rect = pygame.Rect(x_pos, y_pos + tile_size, tile_size / 3, tile_size / 3)
                    screen.blit(tongue_down, tongue_rect)

                if snake.direction == Vector2(1, 0): # snake is moving right
                    leftEye = pygame.Rect(x_pos - tile_size / 2, y_pos - 7 + tile_size / 2, tile_size / 3, tile_size / 3)
                    rightEye = pygame.Rect(x_pos - tile_size / 2, y_pos - 7 - tile_size / 2, tile_size / 3, tile_size / 3)
                    screen.blit(eye_rotate, leftEye)
                    screen.blit(eye_rotate, rightEye)
                    
                    tongue_right = pygame.transform.rotate(tongue_image, 270)
                    tongue_rect = pygame.Rect(x_pos + tile_size, y_pos, tile_size / 3, tile_size / 3)
                    screen.blit(tongue_right, tongue_rect)

                if snake.direction == Vector2(-1, 0): # snake is moving left
                    leftEye = pygame.Rect(x_pos - tile_size / 2, y_pos - 7 + tile_size / 2, tile_size / 3, tile_size / 3)
                    rightEye = pygame.Rect(x_pos - tile_size / 2, y_pos - 7 - tile_size / 2, tile_size / 3, tile_size / 3)
                    screen.blit(eye_rotate, leftEye)
                    screen.blit(eye_rotate, rightEye)
                    
                    tongue_left = pygame.transform.rotate(tongue_image, 90)
                    tongue_rect = pygame.Rect(x_pos - tile_size, y_pos, tile_size / 3, tile_size / 3)
                    screen.blit(tongue_left, tongue_rect)

                
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
        # eat_sound.play()

    def respawn(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.fruit_eaten = 0
        
    def play_eat_sound(self):
        self.eat_sound.play()

    def play_death_sound(self):
        self.death_sound.play()

class Fruit:
   def __init__(self):
       self.x = random.randrange(0, tile_number - 1) 
       self.y = random.randrange(0, tile_number - 1) 
       self.pos = Vector2(self.x * tile_size, self.y * tile_size)
       self.image = apple_image

   def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x, self.pos.y, tile_size, tile_size)
        screen.blit(self.image, fruit_rect)
        # pygame.draw.ellipse(screen, (255,0,0), fruit_rect)

   def respawn(self): 

        self.x = random.randrange(0, tile_number - 1) 
        self.y = random.randrange(0, tile_number - 1)

        if Vector2(self.x, self.y) in snake.body:
            #print("Rerolling")
            self.respawn()
        else:
            self.pos = Vector2(self.x * tile_size, self.y * tile_size) 

            fruitNum = random.randrange(0, 4)
            self.image = fruits[fruitNum]
        

def newGame(fruit, snake):
    global gameIsOver
    fruit.respawn()
    snake.respawn()
    gameIsOver = False

def draw_score(snake):
    score_text = "Fruits: " + str(len(snake.body) - 3)
    score_surface = font.render(score_text, True, (255, 255, 255))
    score_rect = score_surface.get_rect(center = (tile_number * tile_size - 100, 50))
    
    screen.blit(score_surface,score_rect)

def draw_restart():
    restart_text = "Game over! Press 'r' to restart the game."
    restart_surface = font.render(restart_text, True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center = (tile_number * tile_size / 2, tile_number * tile_size / 2))
    
    screen.blit(restart_surface,restart_rect)

pygame.font.init()

tile_size = 50
tile_number = 19

font = pygame.font.SysFont('Tahoma', 30)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((tile_size * tile_number, tile_size * tile_number))

# Title and Icon
pygame.display.set_caption("The Very Hungry Snake")

global snake
snake = Snake()

global fruit
fruit = Fruit()

# Updates the screen (moves snake) every update_timer milliseconds
update_timer = 150

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, update_timer)


while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and not gameIsOver:
            check_next_tile(snake, fruit)
            if gameIsOver:
                draw_restart()
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
            if (event.key == pygame.K_r) and gameIsOver:
                # print('r pressed')
                newGame(fruit, snake)


    if not gameIsOver:     
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
        draw_score(snake)

    pygame.display.update()
    clock.tick(60)

