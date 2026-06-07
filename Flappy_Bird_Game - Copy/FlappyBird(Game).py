import pygame
import random
import sys

pygame.init()

#=======SCREEN==========

WIDTH, HEIGHT = 580, 840
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FLAP IT")
clock = pygame.time.Clock()
FPS = 60

#=======COLORS=========

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)


#===============BACKGROUND============
bg_image = pygame.image.load("assets/images/bgpic3.png").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))


#=======FONTS=========
title_font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 32)
score_font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 18)
instruction_font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 12)
menu_font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", 22)

 
#========BUTTONS===========

def load_button(path, size=(220,90), hover_size=(235,100)):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    img_hover = pygame.transform.scale(img, hover_size)
    return img, img_hover

start_img, start_hover_img = load_button("assets/images/STARTPNG.png")
exit_img, exit_hover_img = load_button("assets/images/EXITPNG.png")
again_img, again_hover_img = load_button("assets/images/AGAINPNG.png")

start_rect = start_img.get_rect(center=(WIDTH//2,320))
exit_rect = exit_img.get_rect(center=(WIDTH//2,430))


#========IMAGES============

mute_img = pygame.transform.scale(pygame.image.load("assets/images/mutesound.png").convert_alpha(), (55,55))
unmute_img = pygame.transform.scale(pygame.image.load("assets/images/unmutesound.png").convert_alpha(), (55,55))
question_img = pygame.transform.scale(pygame.image.load("assets/images/questionmark.png").convert_alpha(), (55,55))
pause_img = pygame.transform.scale(pygame.image.load("assets/images/pause.png").convert_alpha(), (55,55))

sound_rect = unmute_img.get_rect(bottomright=(WIDTH-20, HEIGHT-20))
question_rect = question_img.get_rect(bottomleft=(20, HEIGHT-20))
pause_rect = pause_img.get_rect(topleft=(20,20))

#======GAME_STATES============

MENU, GAME = 0, 1
game_state = MENU

high_score = 0
sound_on = True
show_help = False

pygame.mixer.music.load("assets/music/themesong.mp3")
score_sound = pygame.mixer.Sound("assets/music/scoresound.wav")
score_sound.set_volume(0.8)


#=====OUTLINE=========

def draw_text_outline(surface, text, font, color, outline_color, center):
    offsets = [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,-2),(-2,2),(2,2)]
    for ox,oy in offsets:
        surf = font.render(text, True, outline_color)
        surface.blit(surf, surf.get_rect(center=(center[0]+ox,center[1]+oy)))
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=center))

#========MENU==========

def draw_menu():
    if sound_on and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    screen.blit(bg_image,(0,0))
    draw_text_outline(screen,"FLAP IT",title_font,WHITE,BLACK,(WIDTH//2,120))
    draw_text_outline(screen,f"HIGH SCORE: {high_score}",score_font,WHITE,BLACK,(WIDTH//2,180))

    mouse = pygame.mouse.get_pos()

    screen.blit(unmute_img if sound_on else mute_img, sound_rect)
    screen.blit(question_img, question_rect)

    screen.blit(start_hover_img if start_rect.collidepoint(mouse) else start_img,start_rect)
    screen.blit(exit_hover_img if exit_rect.collidepoint(mouse) else exit_img,exit_rect)

    if show_help:
        help_surf = pygame.Surface((500,320))
        help_surf.set_alpha(230)
        help_surf.fill((0,0,0))
        screen.blit(help_surf, help_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))

        draw_text_outline(screen,"CONTROLS",score_font,WHITE,BLACK,(WIDTH//2,300))
        draw_text_outline(screen,"SPACE / CLICK = JUMP",score_font,WHITE,BLACK,(WIDTH//2,360))
        draw_text_outline(screen,"P = PAUSE",score_font,WHITE,BLACK,(WIDTH//2,410))
        draw_text_outline(screen,"DEVELOPED BY:",score_font,WHITE,BLACK,(WIDTH//2,470))
        draw_text_outline(screen,"AEROPARK",score_font,YELLOW,BLACK,(WIDTH//2,530))


#======TRANSITION==========

def fade():
    surf = pygame.Surface((WIDTH,HEIGHT))
    surf.fill((0,0,0))
    for alpha in range(0,255,8):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        surf.set_alpha(alpha)
        draw_menu()
        screen.blit(surf,(0,0))
        pygame.display.update()
        clock.tick(60)


# ==========GAME===========

def run_game():
    global high_score

    bird_x, bird_y, bird_speed = 80, HEIGHT//2, 0
    gravity = 0.5

    pipe_width, pipe_gap, pipe_speed = 120, 180, 7
    score = 0
    started = False
    paused = False
    game_over = False
    pipes = []

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1350)

    bird_img = pygame.transform.scale(
        pygame.image.load("assets/images/bird1.png").convert_alpha(),
        (50,50)
    )

    pipe_up_img = pygame.transform.scale(
        pygame.image.load("assets/images/pipeup.png").convert_alpha(),
        (pipe_width, HEIGHT)
    )

    pipe_down_img = pygame.transform.scale(
        pygame.image.load("assets/images/pipedown.png").convert_alpha(),
        (pipe_width, HEIGHT)
    )

    again_rect = again_img.get_rect(center=(WIDTH//2,520))
    exit_game_rect = exit_img.get_rect(center=(WIDTH//2,640))

    def create_pipe():
        gap_y = random.randint(190,600)
        top = pygame.Rect(WIDTH,0,pipe_width,gap_y-pipe_gap//2)
        bottom = pygame.Rect(WIDTH,gap_y+pipe_gap//2,pipe_width,HEIGHT-(gap_y+pipe_gap//2))
        return {"top":top,"bottom":bottom,"scored":False}

    def move_pipes():
        nonlocal score
        for p in pipes:
            p["top"].x -= pipe_speed
            p["bottom"].x -= pipe_speed

            if not p["scored"] and p["top"].centerx < bird_x:
                p["scored"] = True
                score += 1
                if sound_on:
                    score_sound.play()

        pipes[:] = [p for p in pipes if p["top"].right > 0]

    def draw_pipes():
        for p in pipes:
            screen.blit(pipe_up_img, p["top"], (0,HEIGHT-p["top"].height,pipe_width,p["top"].height))
            screen.blit(pipe_down_img, p["bottom"], (0,0,pipe_width,p["bottom"].height))

    def check_collision():
        bird_rect = pygame.Rect(bird_x-25,bird_y-25,50,50)
        for p in pipes:
            if bird_rect.colliderect(p["top"]) or bird_rect.colliderect(p["bottom"]):
                return False
        return 25 < bird_y < HEIGHT-25

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == SPAWNPIPE and started and not paused and not game_over:
                pipes.append(create_pipe())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not paused and not game_over:
                    bird_speed = -9
                    started = True
                if event.key == pygame.K_p:
                    paused = not paused

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over and not paused:
                    bird_speed = -9
                    started = True

                if pause_rect.collidepoint(event.pos):
                    paused = not paused
                    continue

                if game_over:
                    if again_rect.collidepoint(event.pos):
                        pygame.time.set_timer(SPAWNPIPE, 0)
                        return "RESTART"
                    if exit_game_rect.collidepoint(event.pos):
                        pygame.time.set_timer(SPAWNPIPE, 0)
                        return "MENU"

        if started and not paused and not game_over:
            bird_speed += gravity
            bird_y += bird_speed
            move_pipes()

            if not check_collision():
                game_over = True
                high_score = max(high_score, int(score))

                        
        screen.blit(bg_image, (0, 0))

        
        if not started:
            draw_text_outline(
                screen,
                "PRESS SPACE",
                instruction_font,
                YELLOW,
                BLACK,
                (WIDTH//2, HEIGHT//2 - 15)
            )

            draw_text_outline(
                screen,
                "OR CLICK TO FLY",
                instruction_font,
                YELLOW,
                BLACK,
                (WIDTH//2, HEIGHT//2 + 15)
            )

        #Pipes
        draw_pipes()

        #Bird
        rotated = pygame.transform.rotate(
            bird_img,
            max(-45, min(45, -bird_speed * 3))
        )

        screen.blit(
            rotated,
            rotated.get_rect(center=(bird_x, int(bird_y)))
        )

        #Score
        draw_text_outline(
            screen,
            f"{int(score)}",
            score_font,
            WHITE,
            BLACK,
            (WIDTH//2, 60)
        )

        
        if paused:
            pause_copy = pause_img.copy()
            pause_copy.set_alpha(120)
            screen.blit(pause_copy, pause_rect)

            draw_text_outline(
                screen,
                "PAUSED",
                menu_font,
                WHITE,
                BLACK,
                (WIDTH//2, HEIGHT//2)
            )
        else:
            screen.blit(pause_img, pause_rect)

        #GameOverOverlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            draw_text_outline(
                screen,
                "GAME OVER",
                title_font,
                WHITE,
                BLACK,
                (WIDTH//2, 180)
            )

            draw_text_outline(
                screen,
                f"SCORE: {int(score)}",
                menu_font,
                YELLOW,
                BLACK,
                (WIDTH//2, 280)
            )

            draw_text_outline(
                screen,
                f"BEST: {high_score}",
                menu_font,
                WHITE,
                BLACK,
                (WIDTH//2, 340)
            )

            mouse = pygame.mouse.get_pos()

            screen.blit(
                again_hover_img if again_rect.collidepoint(mouse)
                else again_img,
                again_rect
            )

            screen.blit(
                exit_hover_img if exit_game_rect.collidepoint(mouse)
                else exit_img,
                exit_game_rect
            )

        pygame.display.update()


#==========MAIN_LOOP===========

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == MENU and event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if sound_rect.collidepoint(pos):
                sound_on = not sound_on
                pygame.mixer.music.unpause() if sound_on else pygame.mixer.music.pause()

            elif question_rect.collidepoint(pos):
                show_help = not show_help

            elif start_rect.collidepoint(pos):
                pygame.mixer.music.stop()
                fade()
                game_state = GAME

            elif exit_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()

    if game_state == MENU:
        draw_menu()

    elif game_state == GAME:
        result = run_game()
        if result == "MENU":
            game_state = MENU
        elif result == "RESTART":
            game_state = GAME

    pygame.display.update()

pygame.quit()