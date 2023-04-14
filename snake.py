import pygame
import random
from os import path 
pygame.init()
height = 600
width = 800
clock = pygame.time.Clock()
blue = (178, 205, 217)
pink = (209, 136, 193)
orange = (255, 161, 110)
grey = (127, 128, 103)
yellow = (255, 161, 110)
white = (255, 255, 255)
black = (20, 20, 20)
fps = 5
speed = 15
x = 80
y = 80
snake_blok = 30
snake_step = 30
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("змейка")
img_dir = path.join(path.dirname(__file__), "img")
mus_dir = path.join(path.dirname(__file__), "music")
bg = pygame.image.load(path.join(img_dir, "Fon_grass3.png")).convert()
bg = pygame.transform.scale(bg, (width, height))
bg_rect = bg.get_rect()
pygame.mixer.music.load(path.join(mus_dir, "Intense.mp3"))
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)
am = pygame.mixer.Sound(path.join(mus_dir, "apple_bite.ogg"))
am.set_volume(0.5)
head = [pygame.image.load(path.join(img_dir, "HeadB.png")).convert(),
        pygame.image.load(path.join(img_dir, "HeadL.png")).convert(),
        pygame.image.load(path.join(img_dir, "HeadR.png")).convert(),
        pygame.image.load(path.join(img_dir, "HeadT.png")).convert()]
tail = [pygame.image.load(path.join(img_dir, "taildown.png")).convert(),
        pygame.image.load(path.join(img_dir, "tailup.png")).convert(),
        pygame.image.load(path.join(img_dir, "tailright.png")).convert(),
        pygame.image.load(path.join(img_dir, "tailleft.png")).convert(),]
def draw_head(i, snake_list):
    snake_head_img = head[i]
    snake_head = pygame.transform.scale(snake_head_img,(snake_blok, snake_blok))
    snake_head.set_colorkey(white)
    snake_head_rect = snake_head.get_rect(x = snake_list[-1][0], y= snake_list[-1][1])
    screen.blit(snake_head, snake_head_rect)
def draw_tail(i, snake_list):
    snake_tail_img = tail[i]
    snake_tail = pygame.transform.scale(snake_tail_img, (snake_blok, snake_blok))
    snake_tail.set_colorkey(white)
    snake_tail_rect = snake_tail.get_rect(x = snake_list[0][0], y= snake_list[0][1])
    screen.blit(snake_tail, snake_tail_rect)
def create_message(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    msg = font_style.render(msg, True, color)
    screen.blit(msg, [x, y])
def eaten_check(xcor, ycor, foodx, foody):
    if foodx-snake_blok <= xcor <= foodx+snake_blok:
        if foody-snake_blok <= ycor <= foody+snake_blok:
            return True
    else:
        return False

def game_loop():
    foodx = random.randrange(0, width - snake_blok)
    foody = random.randrange(0, height - snake_blok)
    i = 0
    game_close = False
    x1 = width/2
    y1 = height/2
    x1_change = 0
    y1_change = 0
    lenght = 2
    snake_list = []
    food_list =[pygame.image.load(path.join(img_dir, "f_1.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_2.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_3.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_4.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_5.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_6.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_7.png")).convert()]
    food = pygame.transform.scale(random.choice(food_list),(30,30))
    food.set_colorkey(pink)
    food_rect = food.get_rect(x = foodx, y = foody)
    
    run = True
    while run:
        while game_close:
            screen.fill(grey)
            create_message("Вы проиграли", blue, 200, 200, "comicsans", 70)
            create_message("Нажмите Q для выхода, для повторной игры C", orange, 50, 300, 'comicsans', 30)
            create_message(f"Финальный счет: {lenght - 2}", pink, 0,0, "comicsans", 25)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change -= snake_step 
                    y1_change = 0
                    i = 1
                elif event.key == pygame.K_RIGHT:
                    x1_change += snake_step
                    y1_change = 0
                    i = 2
                elif event.key == pygame.K_UP:
                    y1_change -= snake_step
                    x1_change = 0
                    i = 3
                elif event.key == pygame.K_DOWN:
                    y1_change += snake_step
                    x1_change = 0
                    i = 0
        if x1 >= width or x1 <= 0 or y1 >= height or y1 <= 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill(yellow)
        screen.blit(bg, bg_rect)
        screen.blit(food, food_rect)
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > lenght:
            del snake_list[0]
        for x in snake_list[1:]:
            snake_image = pygame.image.load(path.join(img_dir, "body.png")).convert()
            snake = pygame.transform.scale(snake_image,(snake_blok, snake_blok))
            snake.set_colorkey(white)
            screen.blit(snake, (x[0], x[1]))
        draw_head(i, snake_list)
        draw_tail(i, snake_list)
        create_message(f"Текущий счет: {lenght - 2}", black, 0,0, "comicsans", 25)
        pygame.display.update()
        if eaten_check(x1, y1, foodx, foody):
            foodx = random.randrange(0, width - snake_blok)
            foody = random.randrange(0, height - snake_blok)
            food_list =[pygame.image.load(path.join(img_dir, "f_1.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_2.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_3.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_4.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_5.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_6.png")).convert(),
                pygame.image.load(path.join(img_dir, "f_7.png")).convert()]
            food = pygame.transform.scale(random.choice(food_list),(30,30))
            food.set_colorkey(pink)
            food_rect = food.get_rect(x = foodx, y = foody)
            lenght += 1
            am.play()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
game_loop()
