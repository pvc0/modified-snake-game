import pygame, sys, random
import numpy as np
from pygame.math import Vector2

class SNAKE:
    def __init__(self): 
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = cell_size * block.x
            y_pos = cell_size * block.y
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (34,50,150), block_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:] #taking all elements 
            body_copy.insert(0, body_copy[0]+self.direction) #adding the new moved head of snake to beginning
            self.body = body_copy[:]
            self.new_block = False
        
        else:
            body_copy = self.body[:-1] #taking all elements except last one
            body_copy.insert(0, body_copy[0]+self.direction) #adding the new moved head of snake to beginning
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)  
        #pygame.draw.rect(screen, (130,166,114), fruit_rect) 
        screen.blit(apple, fruit_rect)

    def move_fruit(self):
        newpos = self.pos
        newpos_x = random.choice([-1,0,1])
        if newpos_x == 0:
            newpos_y = random.choice([1, -1])
        else:
            newpos_y = 0
        newpos = self.pos + 0.5*Vector2(newpos_x,newpos_y)
        self.pos = newpos

    def randomize(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)  #using vectors: self = [5,4]


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.fruit.move_fruit()
        self.fruit_collision()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        #if self.fruit.pos == self.snake.body[0]:
        for extraX in np.arange(-0.75, 0.75, 0.25):
            for extraY in np.arange(-0.75, 0.75, 0.25):
                if (self.snake.body[0].x == self.fruit.pos.x + extraX) and (self.snake.body[0].y == self.fruit.pos.y + extraY):
                    self.fruit.randomize()
                    self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def fruit_collision(self):
        
        if not 0 <= self.fruit.pos.x < cell_number/2:
            self.fruit.pos.x = -self.fruit.pos.x

        if not 0 <= self.fruit.y < cell_number/2:
            self.fruit.pos.y = -self.fruit.pos.y
        
        '''
        if self.fruit.pos.x > 600:
            print('collision')
            self.fruit.pos.x *= -1
        if self.fruit.pos.x < 0:
            self.fruit.pos.x *= -1
        if self.fruit.pos.y > 600: 
            self.fruit.pos.y *= -1
        if self.fruit.pos.y < 0:
            self.fruit.pos.y *= -1
        '''

    def game_over(self):
        pygame.quit()
        sys.exit()
        
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (55,75,10))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)

pygame.init()
cell_size = 40
cell_number = 20
running = True
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size)) #600x600 pixel
pygame.display.set_caption('Snake game')
clock = pygame.time.Clock()
appleIMG = pygame.image.load('/Users/patrick_leuchtenberger/Documents/Python/apple.png').convert_alpha()
apple = pygame.transform.scale(appleIMG, (cell_size, cell_size))
game_font = pygame.font.Font(None, 25)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)


while running:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y !=1:
                    main_game.snake.direction = Vector2(0,-1)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x !=-1:
                    main_game.snake.direction = Vector2(1,0)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y !=-1:
                    main_game.snake.direction = Vector2(0,1)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x !=1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((255, 255, 255)) #(red, green, blue), 100%=255
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)








