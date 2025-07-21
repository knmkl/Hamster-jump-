import pygame
import random
import math
import time

pygame.init()
pygame.mixer.init()

# хэмжээнүүд
WIDTH = 500
HEIGHT = 750
FPS = 60
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 90
PLATFORM_WIDTH = 75
PLATFORM_HEIGHT = 15

# дэлгэцийн зургууд
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Ehnii togloom : hamster jumper')
background = pygame.image.load('zurguud/ardtal.jpg')

# зургууд
player_img = pygame.transform.scale(pygame.image.load('zurguud/tsar.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
platform_img = pygame.transform.scale(pygame.image.load('zurguud/tavtsn.png'), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
platform_broken_img = pygame.transform.scale(pygame.image.load('zurguud/evdertsen.png'), (PLATFORM_WIDTH, PLATFORM_HEIGHT))
platform_spring_img = pygame.transform.scale(pygame.image.load('zurguud/purshtei.png'), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

# фонт
font = pygame.font.SysFont('comicsansms', 26)
big_font = pygame.font.SysFont('comicsansms', 40)

# дуунууд
jump_sound = pygame.mixer.Sound('sound/usrelt.wav')
spring_sound = pygame.mixer.Sound('sound/purshdelt.wav')
fall_sound = pygame.mixer.Sound('sound/unalt.wav')
monster_sound = pygame.mixer.Sound('sound/mangas.wav')
broken_plat = pygame.mixer.Sound('sound/hevreg.wav')
duusah = pygame.mixer.Sound('sound/duusah.wav')
ehlehdohio = pygame.mixer.Sound('sound/ehlehdohio.wav')
ehlehpursh = pygame.mixer.Sound('sound/ehlehpursh.wav')

clock = pygame.time.Clock()

# Platform class
class Platform:
    def __init__(self, x, y, kind='normal'):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.kind = kind
        self.broken_once = False

    def draw(self, surface):
        if self.kind == 'normal':
            surface.blit(platform_img, self.rect.topleft)
        elif self.kind == 'broken':
            if not self.broken_once:
                surface.blit(platform_broken_img, self.rect.topleft)
        elif self.kind == 'spring':
            surface.blit(platform_spring_img, self.rect.topleft)

   
def show_text(text, x, y, font_obj, color=(128, 0, 128)):
    render = font_obj.render(text, True, color)
    screen.blit(render, (x, y))


def draw_menu():


    pygame.init()
    screen = pygame.display.set_mode((500, 750))
    clock = pygame.time.Clock()

    background = pygame.transform.scale(pygame.image.load("zurguud/start_screen.png"), (WIDTH, HEIGHT))
    hamster = pygame.transform.scale(pygame.image.load("zurguud/tsar.png"), (90, 90))
      
    start_ticks = pygame.time.get_ticks()
    button_rect = pygame.Rect(200, 450, 150, 50)  
     
    last_offset = 0
    while True:
        screen.blit(background, (0, 0))
        
        # Үсрэх хөдөлгөөн
        time_ms = pygame.time.get_ticks() - start_ticks + 20
        bounce_offset = math.sin(time_ms / 300) * 90  # дээш доош 300 пиксел
        screen.blit(hamster, (260, 295 + bounce_offset))
        if last_offset < 0 and bounce_offset >=0:
            pygame.time.delay(10)
            ehlehpursh.play()
        last_offset = bounce_offset
        # Хамстэрийн үсрэлтийг шалгах
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    ehlehdohio.play()
                    pygame.time.delay(100)
                    return button_rect

        pygame.display.update()
        clock.tick(40)

def load_gif_frames(path_pattern, count):
    return [pygame.image.load(path_pattern % i) for i in range(count)]

def draw_button(text, x, y, w, h, color, hover_color):    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect, border_radius=15)
        if click[0] == 1:
            pygame.time.delay(200)
            return True
    else:
        pygame.draw.rect(screen, color, rect, border_radius=15)

    label = font.render(text, True, (0, 0, 80))
    screen.blit(label, (x + (w - label.get_width()) // 2 , y + (h - label.get_height()) // 2))
    return False

def game_over_screen(score, score_history):
    gif_frames = load_gif_frames("zurguud/frames/tile%03d.png", 70)  
    clock = pygame.time.Clock()

    while True:
        
        screen.fill((255, 255, 190))
        show_text("Хожигдлоо!", 150, 10, big_font)
        # Бүх онооны жагсаалтыг зурна
        for i, s in enumerate(score_history[-3:][::-1]):  # Сүүлийн 3 оноог доош харуулна
            show_text(f"{len(score_history) - i}: {s}", 200, 480 + i * 25, font)

        frame_index = (pygame.time.get_ticks() // 100) % len(gif_frames)
        screen.blit(gif_frames[frame_index], (50, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if draw_button("Тоглох", 85, 600, 150, 70, (180, 255, 230), (160, 230, 210)):
            ehlehdohio.play()
            pygame.time.delay(100)
            return "restart"
        if draw_button("Гарах", 280, 600, 150, 70, (255, 220, 220), (240, 200, 200)):
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(30)


def generate_platforms(platforms, min_y):
    MAX_JUMP_HEIGHT = 100  

    while len(platforms) < 12:
        last_platform = platforms[-1]
        x = random.randint(10, WIDTH - PLATFORM_WIDTH - 10)

        # хүрч болохуйц зайтай байх
        y = last_platform.rect.y - random.randint(50, MAX_JUMP_HEIGHT - 20)

        kind = random.choices(['normal', 'broken', 'spring'], weights=[70, 20, 10])[0]
        platforms.append(Platform(x, y, kind))
    return platforms


def game_loop():
    player_x = 100
    player_y = 550 - PLAYER_HEIGHT
    y_change = 0
    x_change = 0
    jump = False
    score = 0
    highest_y = player_y

    platforms = [Platform(100, 550, 'normal')]
    for i in range(10):
        x = random.randint(10, 420)
        y = 700 - i * 60
        kind = random.choices(['normal', 'broken', 'spring'], weights=[70, 20, 10])[0]
        platforms.append(Platform(x, y, kind))

    running = True
    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # үйлдлүүд
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -3
                if event.key == pygame.K_RIGHT:
                    x_change = 3
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_change = 0

        # Gravity
        if jump:
            y_change = -12
            jump = False
        y_change += 0.3
        player_y += y_change
        player_x += x_change

        # булангаа мөргөх
        if player_x < -PLAYER_WIDTH:
            player_x = WIDTH
        elif player_x > WIDTH:
            player_x = -PLAYER_WIDTH

       # амьтнаа хэт дээшээ болгохгүй
        if player_y < 280:
            scroll = 280 - player_y
            player_y = 280
            for plat in platforms:
                plat.rect.y += scroll
            score += int(scroll)

        # тавцангаа зурна
        screen.blit(player_img, (player_x, player_y))
        for plat in platforms:
            plat.draw(screen)

        # Тавцан дээр гарсанг шалгана.
        player_rect = pygame.Rect(player_x + 20, player_y + 60, 35, 5)
        for plat in platforms:
            if plat.rect.colliderect(player_rect) and y_change > 0:
                if plat.kind == 'broken':
                    if not plat.broken_once:
                        plat.broken_once = True
                        broken_plat.play()
                        continue
                elif plat.kind == 'spring':
                    y_change = -18
                    spring_sound.play()
                else:
                    jump = True
                    jump_sound.play()

        
        platforms = [plat for plat in platforms if plat.rect.y < HEIGHT]
        platforms = generate_platforms(platforms, min([p.rect.y for p in platforms]))        
        show_text(f"Score: {score}", 10, 10, font)        
        if player_y > HEIGHT:
            fall_sound.play()
            pygame.time.delay(1000)
            return score

        pygame.display.flip()


def main():

    in_menu = True
    score_history = []
    while in_menu:
        result = draw_menu()
        if result:
            while True:
                score = game_loop()
                if score is False:
                    return
                score_history.append(score)
                result = game_over_screen(score, score_history)
                if result == "restart":
                    continue
                else:
                    return

main()

