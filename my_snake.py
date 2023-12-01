import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Snake Game - Pankaj Sharma")

red = (245, 93, 66)

dis_width = 800
dis_height = 600

display = pygame.display.set_mode((dis_width, dis_height))

background = pygame.image.load('resources/snake_background.jpg')
background = pygame.transform.scale(background, (800, 600))
game_play = pygame.image.load('resources/background.jpg')
game_play = pygame.transform.scale(game_play, (800, 600))
apple = pygame.image.load('resources/apple.jpg')
apple = pygame.transform.scale(apple, (15, 15))
background_music = pygame.mixer.Sound('resources/background_music.mp3')

block = 15
snake_speed = 15

clock = pygame.time.Clock()

High_Score_file = "high_score.txt"
high_score = 0
point = 0

direction = 'right'

try:
    with open(High_Score_file, "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass


def show_pause_screen():
    pygame.mixer.music.pause()
    font = pygame.font.Font(None, 36)
    text = font.render("PAUSED", True, 'black')
    text_rect = text.get_rect(center=(dis_width/2, dis_height/2))
    display.blit(text, text_rect)
    pygame.display.update()


def show_high_score():
    display.fill('black')
    font = pygame.font.Font(None, 36)
    text = font.render(f"High Score: {high_score}", True, 'white')
    text_surface = text.get_rect(center=(dis_width / 2, dis_height / 2))
    display.blit(text, text_surface)
    pygame.display.update()


def message(x_mess, y_mess, size, mess):
    text = pygame.font.SysFont(None, size)
    blend = text.render(mess, True, 'red')
    display.blit(blend, (x_mess, y_mess))


def score(point):
    text = pygame.font.SysFont(None, 25)
    blend = text.render(f'Score:{point}', True, 'red')
    display.blit(blend, (0, 0))


def button(x_but, y_but, color, text):
    pygame.draw.rect(display, color, [x_but, y_but, 110, 30])
    message(x_but, y_but, 50, text)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x_but < mouse[0] < x_but + 110 and y_but < mouse[1] < y_but + 30:
        pygame.draw.rect(display, red, [x_but, y_but, 110, 30])
        message(x_but, y_but, 50, text)
        if click == (1, 0, 0) and text == 'START':
            start_game(snake_speed, point)
        if click == (1, 0, 0) and text == 'QUIT':
            quit()
        if click == (1, 0, 0) and text == 'Score':
            show_high_score()


def snake(snake_list, block):
    for x1 in snake_list:
        pygame.draw.rect(display, red, [x1[0], x1[1], block, block])


def over(scr, high_score):
    background_music.stop()
    if scr > high_score:
        high_score = scr
        with open(High_Score_file, "w") as file:
            file.write(str(high_score))
    tex = 'Your Score is ' + str(scr)
    display.fill('grey')
    message(dis_width/4, dis_height/3, 50, tex)
    pygame.display.update()
    time.sleep(3)
    intro()


def intro():
    background_music.play(loops=-1)
    game_over = False
    while not game_over:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.blit(background, [0, 0, dis_width, dis_height])
        button(150, 400, 'green', 'START')
        button(600, 400, 'green', 'QUIT')
        button(150, 100, 'green', 'Score')
        pygame.display.update()


def start_game(snake_speed, point):
    background_music.stop()
    background_music.play(loops=-1)
    eat_sound = pygame.mixer.Sound('resources/eating_sound.mp3')
    crash_sound = pygame.mixer.Sound('resources/crash_sound.mp3')
    x = dis_width/2
    y = dis_height/2
    x_change = 0
    y_change = 0
    x_food = 400
    y_food = 200

    snake_list = []
    length_of_snake = 1
    game_over = False
    paused = False
    while not game_over:
        global direction
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                game_over = True
            if events.type == pygame.KEYDOWN:
                if (events.key == pygame.K_UP or events.key == pygame.K_w) and direction != 'down':
                    direction = 'up'
                    x_change = 0
                    y_change = -10
                elif (events.key == pygame.K_DOWN or events.key == pygame.K_s) and direction != 'up':
                    direction = 'down'
                    x_change = 0
                    y_change = 10
                elif (events.key == pygame.K_LEFT or events.key == pygame.K_a) and direction != 'right':
                    direction = 'left'
                    x_change = -10
                    y_change = 0
                elif (events.key == pygame.K_RIGHT or events.key == pygame.K_d) and direction != 'left':
                    direction = 'right'
                    x_change = 10
                    y_change = 0
                if events.key == pygame.K_SPACE:
                    paused = not paused
        if paused:
            show_pause_screen()
        else:
            if x < 0 or x >= dis_width or y < 0 or y >= dis_height:
                crash_sound.play()
                over(length_of_snake-1, high_score)
            x += x_change
            y += y_change
            display.fill('grey')
            display.blit(apple, [x_food, y_food, block, block])
            snake_head = []
            snake_head.append(x)
            snake_head.append(y)
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for x1 in snake_list[:-1]:
                if x1 == snake_head:
                    over(length_of_snake-1, high_score)
            snake(snake_list, block)
            score(point)
            pygame.display.update()
            if x_food == x and y_food == y:
                eat_sound.play()
                point += 1
                x_food = round(random.randrange(0, dis_width-block)/10.0)*10.0
                y_food = round(random.randrange(0, dis_height-block)/10.0)*10.0
                length_of_snake += 1
                snake_speed += 1

            clock.tick(snake_speed)

    pygame.quit()
    quit()


intro()
