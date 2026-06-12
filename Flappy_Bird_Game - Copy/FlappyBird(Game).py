import pygame
import random
import sys
import ctypes

# Fix for Windows scaling cutting off the bottom of the Pygame window on laptops
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

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
GRAY = (50, 50, 50)
RED = (255, 0, 50)  

#===============BACKGROUNDS CYCLE LOADING============
bgs = [
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgcityday.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgcitynight.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgforestday.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgforestnight.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgsnowday.png").convert(), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/images/BACKGROUND/bgsnownight.png").convert(), (WIDTH, HEIGHT))
]

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

start_img, start_hover_img = load_button("assets/images/BUTTONS/STARTPNG.png")
exit_img, exit_hover_img = load_button("assets/images/BUTTONS/EXITPNG.png")
again_img, again_hover_img = load_button("assets/images/BUTTONS/AGAINPNG.png")

start_rect = start_img.get_rect(center=(WIDTH//2, 320))
exit_rect = exit_img.get_rect(center=(WIDTH//2, 430))

#========IMAGES============

mute_img = pygame.transform.scale(pygame.image.load("assets/images/ICONS/mutesound.png").convert_alpha(), (55,55))
unmute_img = pygame.transform.scale(pygame.image.load("assets/images/ICONS/unmutesound.png").convert_alpha(), (55,55))
question_img = pygame.transform.scale(pygame.image.load("assets/images/ICONS/questionmark.png").convert_alpha(), (55,55))
pause_img = pygame.transform.scale(pygame.image.load("assets/images/ICONS/pause.png").convert_alpha(), (55,55))
hanger_img = pygame.transform.scale(pygame.image.load("assets/images/ICONS/hanger.png").convert_alpha(), (55,55))

# Team Logo configuration
team_logo_img = pygame.image.load("assets/images/ICONS/teamname.png").convert_alpha()
team_logo_img = pygame.transform.scale(team_logo_img, (350, 350)) 
team_logo_rect = team_logo_img.get_rect(center=(WIDTH//2, HEIGHT//2))

sound_rect = unmute_img.get_rect(bottomright=(WIDTH - 30, HEIGHT - 40))
hanger_rect = hanger_img.get_rect(bottomright=(WIDTH - 30, sound_rect.top - 20))
question_rect = question_img.get_rect(bottomleft=(30, HEIGHT - 40))
pause_rect = pause_img.get_rect(topleft=(20, 20))

#========BIRD SKINS SETUP============
skin_paths = [
    "assets/images/BIRD_SKINS/bird1.png",
    "assets/images/BIRD_SKINS/bird2.png",
    "assets/images/BIRD_SKINS/bird3.png"
]
current_skin_index = 0
show_skins_menu = False

#======GAME_STATES============

INTRO, MENU, GAME = -1, 0, 1
game_state = INTRO  

high_score = 0
sound_on = True
show_help = False

pygame.mixer.music.load("assets/music/themesong.mp3")
score_sound = pygame.mixer.Sound("assets/music/scoresound.wav")
score_sound.set_volume(0.8)

try:
    intro_sound = pygame.mixer.Sound("assets/music/introsound.wav") 
    intro_sound.set_volume(0.7)
except:
    intro_sound = None

#=====OUTLINE=========

def draw_text_outline(surface, text, font, color, outline_color, center):
    offsets = [(-2,0),(2,0),(0,-2),(0,2),(-2,-2),(2,-2),(-2,2),(2,2)]
    for ox,oy in offsets:
        surf = font.render(text, True, outline_color)
        surface.blit(surf, surf.get_rect(center=(center[0]+ox,center[1]+oy)))
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=center))

#=======(UNSKIPPABLE)==========

def run_intro():
    """ Runs a dramatic teamname style opening animation - Unskippable """
    if intro_sound:
        intro_sound.play()

    intro_clock = pygame.time.Clock()
    
    # Phase 1: Developer Logo
    logo_duration = 120 
    for frame in range(logo_duration):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        screen.fill(BLACK)
        
        if frame < 40:
            alpha = int((frame / 40) * 255)
        elif frame > 80:
            alpha = int(((logo_duration - frame) / 40) * 255)
        else:
            alpha = 255
            
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        temp_surface.blit(team_logo_img, team_logo_rect)
        temp_surface.set_alpha(alpha)
        
        screen.blit(temp_surface, (0,0))
        pygame.display.update()
        intro_clock.tick(FPS)

    # Phase 2: Cinematic Flash
    flash_duration = 90 
    for frame in range(flash_duration):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill(BLACK)
        
        scale_factor = 1.0 + (max(0, 30 - frame) / 10.0) 
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        current_title_font = pygame.font.Font("assets/fonts/Press_Start_2P/PressStart2P-Regular.ttf", int(32 * scale_factor))
        draw_text_outline(temp_surface, "FLAP IT", current_title_font, WHITE, BLACK, (WIDTH//2, HEIGHT//2 - 40))
        
        if frame > 20: 
            draw_text_outline(temp_surface, "FLY HIGH!", instruction_font, YELLOW, BLACK, (WIDTH//2, HEIGHT//2 + 20))
            
        if 28 <= frame <= 33:
            flash_layer = pygame.Surface((WIDTH, HEIGHT))
            flash_layer.fill(WHITE)
            flash_layer.set_alpha(150)
            screen.blit(flash_layer, (0,0))

        temp_surface.set_alpha(min(255, int((frame / 15) * 255)))
        screen.blit(temp_surface, (0,0))
        
        pygame.display.update()
        intro_clock.tick(FPS)
        
    fade()

#========MENU==========

def draw_menu():
    if sound_on and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    screen.blit(bgs[0],(0,0))
    draw_text_outline(screen,"FLAP IT",title_font,WHITE,BLACK,(WIDTH//2,120))
    draw_text_outline(screen,f"HIGH SCORE: {high_score}",score_font,WHITE,BLACK,(WIDTH//2,180))

    mouse = pygame.mouse.get_pos()

    screen.blit(unmute_img if sound_on else mute_img, sound_rect)
    screen.blit(hanger_img, hanger_rect)
    screen.blit(question_img, question_rect)

    screen.blit(start_hover_img if start_rect.collidepoint(mouse) else start_img,start_rect)
    screen.blit(exit_hover_img if exit_rect.collidepoint(mouse) else exit_img,exit_rect)

    if show_skins_menu:
        skins_surf = pygame.Surface((500,340))
        skins_surf.set_alpha(240)
        skins_surf.fill((20, 20, 20))
        skins_rect = skins_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(skins_surf, skins_rect)

        draw_text_outline(screen, "CHOOSE SKIN", score_font, YELLOW, BLACK, (WIDTH//2, HEIGHT//2 - 110))

        for i, path in enumerate(skin_paths):
            raw_bird = pygame.image.load(path).convert_alpha()
            display_bird = pygame.transform.scale(raw_bird, (85, 85))
            bird_pos_x = WIDTH//2 + (i - 1) * 120
            bird_pos_y = HEIGHT//2
            bird_preview_rect = display_bird.get_rect(center=(bird_pos_x, bird_pos_y))
            
            if i == current_skin_index:
                pygame.draw.rect(screen, YELLOW, bird_preview_rect.inflate(20, 20), 4)
            else:
                pygame.draw.rect(screen, GRAY, bird_preview_rect.inflate(15, 15), 2)
                
            screen.blit(display_bird, bird_preview_rect)

        draw_text_outline(screen, "CLICK SKIN TO SELECT", instruction_font, WHITE, BLACK, (WIDTH//2, HEIGHT//2 + 90))
        draw_text_outline(screen, "CLICK HANGER TO CLOSE", instruction_font, WHITE, BLACK, (WIDTH//2, HEIGHT//2 + 120))

    elif show_help:
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
    global high_score, current_skin_index

    bird_x, bird_y, bird_speed = 80, HEIGHT//2, 0
    gravity = 0.5

    pipe_width, pipe_gap, pipe_speed = 120, 180, 7
    score = 0
    lives = 3          
    started = False
    paused = False
    game_over = False
    pipes = []

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1350)

    bird_img = pygame.transform.scale(
        pygame.image.load(skin_paths[current_skin_index]).convert_alpha(),
        (75, 75)
    )

    pipe_styles = [
        {
            "up": pygame.transform.scale(pygame.image.load("assets/images/PIPES/normalpipeup.png").convert_alpha(), (pipe_width, HEIGHT)),
            "down": pygame.transform.scale(pygame.image.load("assets/images/PIPES/normalpipedown.png").convert_alpha(), (pipe_width, HEIGHT))
        },
        {
            "up": pygame.transform.scale(pygame.image.load("assets/images/PIPES/forestpipeup.png").convert_alpha(), (pipe_width, HEIGHT)),
            "down": pygame.transform.scale(pygame.image.load("assets/images/PIPES/forestpipedown.png").convert_alpha(), (pipe_width, HEIGHT))
        },
        {
            "up": pygame.transform.scale(pygame.image.load("assets/images/PIPES/icepipeup.png").convert_alpha(), (pipe_width, HEIGHT)),
            "down": pygame.transform.scale(pygame.image.load("assets/images/PIPES/icepipedown.png").convert_alpha(), (pipe_width, HEIGHT))
        }
    ]

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

    def draw_pipes(current_style_idx):
        for p in pipes:
            screen.blit(pipe_styles[current_style_idx]["up"], p["top"], (0,HEIGHT-p["top"].height,pipe_width,p["top"].height))
            screen.blit(pipe_styles[current_style_idx]["down"], p["bottom"], (0,0,pipe_width,p["bottom"].height))

    def check_collision():
        bird_rect = pygame.Rect(bird_x - 27, bird_y - 27, 54, 54)
        for p in pipes:
            if bird_rect.colliderect(p["top"]) or bird_rect.colliderect(p["bottom"]):
                return False
        return 37 < bird_y < HEIGHT - 37

    def draw_hearts(num_lives):
        """ FIXED: Accurately aligns left and right arches with the bottom point """
        for i in range(num_lives):
            x = WIDTH - 40 - (i * 38)  # Widened gap slightly so hearts don't overlap
            y = 35
            # Draw left/right circles of heart arches perfectly balanced
            pygame.draw.circle(screen, RED, (x - 6, y), 7)
            pygame.draw.circle(screen, RED, (x + 6, y), 7)
            # Draw bottom point spanning perfectly under both circles
            pygame.draw.polygon(screen, RED, [(x - 13, y + 2), (x + 13, y + 2), (x, y + 16)])

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
                lives -= 1
                if lives > 0:
                    bird_y = HEIGHT // 2
                    bird_speed = 0
                    pipes.clear()
                    started = False  
                else:
                    game_over = True
                    high_score = max(high_score, int(score))

        bg_index = (score // 5) % len(bgs)
        screen.blit(bgs[bg_index], (0, 0))
        
        pipe_style_index = bg_index // 2

        if not started and not game_over:
            draw_text_outline(screen, "PRESS SPACE", instruction_font, YELLOW, BLACK, (WIDTH//2, HEIGHT//2 - 15))
            draw_text_outline(screen, "OR CLICK TO FLY", instruction_font, YELLOW, BLACK, (WIDTH//2, HEIGHT//2 + 15))

        draw_pipes(pipe_style_index)

        rotated = pygame.transform.rotate(bird_img, max(-45, min(45, -bird_speed * 3)))
        screen.blit(rotated, rotated.get_rect(center=(bird_x, int(bird_y))))

        draw_text_outline(screen, f"{int(score)}", score_font, WHITE, BLACK, (WIDTH//2, 60))
        
        if not game_over:
            draw_hearts(lives)

        if paused:
            pause_copy = pause_img.copy()
            pause_copy.set_alpha(120)
            screen.blit(pause_copy, pause_rect)
            draw_text_outline(screen, "PAUSED", menu_font, WHITE, BLACK, (WIDTH//2, HEIGHT//2))
        else:
            screen.blit(pause_img, pause_rect)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            draw_text_outline(screen, "GAME OVER", title_font, WHITE, BLACK, (WIDTH//2, 180))
            draw_text_outline(screen, f"SCORE: {int(score)}", menu_font, YELLOW, BLACK, (WIDTH//2, 280))
            draw_text_outline(screen, f"BEST: {high_score}", menu_font, WHITE, BLACK, (WIDTH//2, 340))

            mouse = pygame.mouse.get_pos()
            screen.blit(again_hover_img if again_rect.collidepoint(mouse) else again_img, again_rect)
            screen.blit(exit_hover_img if exit_game_rect.collidepoint(mouse) else exit_img, exit_game_rect)

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

            if show_skins_menu:
                if hanger_rect.collidepoint(pos):
                    show_skins_menu = False
                else:
                    for i in range(len(skin_paths)):
                        bird_pos_x = WIDTH//2 + (i - 1) * 120
                        bird_pos_y = HEIGHT//2
                        click_area = pygame.Rect(0, 0, 90, 90)
                        click_area.center = (bird_pos_x, bird_pos_y)
                        if click_area.collidepoint(pos):
                            current_skin_index = i
                continue

            if sound_rect.collidepoint(pos):
                sound_on = not sound_on
                pygame.mixer.music.unpause() if sound_on else pygame.mixer.music.pause()

            elif hanger_rect.collidepoint(pos):
                show_skins_menu = True
                show_help = False

            elif question_rect.collidepoint(pos):
                show_help = not show_help
                show_skins_menu = False

            elif start_rect.collidepoint(pos):
                pygame.mixer.music.stop()
                fade()
                game_state = GAME

            elif exit_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()

    if game_state == INTRO:
        run_intro()
        game_state = MENU 

    elif game_state == MENU:
        draw_menu()

    elif game_state == GAME:
        result = run_game()
        if result == "MENU":
            game_state = MENU
        elif result == "RESTART":
            game_state = GAME

    pygame.display.update()

pygame.quit()

