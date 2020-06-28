#!/usr/bin/env python3

import os
import random
import pygame
import time


pygame.mixer.init()
pygame.init()


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (1,1,1)


# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load(".Backgrounds/mainBG.jpeg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
intoImg = pygame.image.load(".Backgrounds/beginning.jpeg")
intoImg = pygame.transform.scale(intoImg, (screen_width, screen_height)).convert_alpha()
endImg = pygame.image.load(".Backgrounds/gameOver.jpeg")
endImg = pygame.transform.scale(endImg, (screen_width, screen_height)).convert_alpha()


# Game Title
pygame.display.set_caption("Let's feed the Snake...")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    col1 = white
    if color == green:
        col1 = red
    len = 0 
    for x,y in snk_list:
        if len%2== 0 : 
            pygame.draw.circle(gameWindow, col1, [x, y], int(snake_size/2)) 
            len+=1
        else : 
            pygame.draw.circle(gameWindow, black, [x, y], int(snake_size/2)) 
            len+=1

def welcome():

    exit_game = False
    while not exit_game:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('.Musics/JaricoLandscapeNCS.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
                if event.key == pygame.K_ESCAPE:
                    exit_game = True
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 20
    snake_y = 88
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    # Check if Highest_Score file exists
    if(not os.path.exists(".highest")):
        with open(".highest", "w") as f:
            f.write("0")

    with open(".highest", "r") as f:
        Highest_Score = f.read()

    food_x = random.randint(20, screen_width-20)
    food_y = random.randint(88, screen_height-20)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60
    start_time = time.time()
    while not exit_game:
        if game_over:     
            with open(".highest", "r") as f:
                preHighest = f.read()   
            if int(preHighest) < int(Highest_Score):
                with open(".highest", "w") as f:
                    f.write(str(Highest_Score))

            gameWindow.blit(endImg, (0, 0))
            text_screen(str(score),white, 420, 430)
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                   exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game = True
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            text_screen(str(int(time.time()-start_time)), red, 550, 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score +=10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(food_x-snake_x)<20 and abs(food_y-snake_y)<20:
                score +=10
                while True:
                    food_x = random.randint(20, screen_width-20)
                    food_y = random.randint(88, screen_height-20)
                    if not([food_x,food_y] in snk_list):
                        break

                snk_length +=5
                if score>int(Highest_Score):
                    Highest_Score = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen(str(score), white, 150, 30)
            text_screen(str(Highest_Score), white, 790, 30)
            text_screen(str(int(time.time()-start_time)), (222, 222, 222), 350, 30)
            # if len(snk_list)%2==0:
            pygame.draw.circle(gameWindow, white, [food_x, food_y], int(snake_size/2))
            pygame.draw.circle(gameWindow, black, [food_x, food_y], int(snake_size/3))

           

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]


            if (head in snk_list[:-1]) or (snake_x<18 or snake_x>screen_width-18 or snake_y<86 or snake_y>screen_height-18) :
                game_over = True
                pygame.mixer.music.load('.Musics/dead.mp3')
                pygame.mixer.music.play()
                plot_snake(gameWindow, green, snk_list, snake_size)
                pygame.display.update()
                time.sleep(1)
                pygame.mixer.music.load('.Musics/DeathNote.mp3')
                pygame.mixer.music.play(-1)
            plot_snake(gameWindow, white, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    # print("Game Over....")
    quit()
    


# print("Game has been started....")
gameWindow.blit(intoImg, (0,0))
pygame.mixer.music.load('.Musics/DeathNote.mp3')
pygame.mixer.music.play(-1)
welcome()
