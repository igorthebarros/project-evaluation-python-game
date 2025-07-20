# TODO: Não está  dando para selecionar o personagem 

import math
import random

WIDTH = 800
HEIGHT = 600

# Game positions
top_center = (WIDTH // 2, 50)
center = (WIDTH // 2, HEIGHT // 2)
bottom_center = (WIDTH // 2, HEIGHT - 50)
left_center = (50, HEIGHT // 2)
right_center = (WIDTH - 50, HEIGHT // 2)

# Game variables
game_started = False
game_over = False
play_music = False
music_playing = False
game_state = "home"
world_offset = 0
run_frame = 0
frame_count = 0
velocity_y = 0
gravity = 1
jump_strength = -15
ground_y = 400

# Character variables
character_options = ['pink', 'blue', 'green', 'yellow', 'beige']
character_sprites = ['stand', 'select','hurt']
character_buttons = []
player_pos = [100, 400]
player_speed = 5
selected_character = None
character_action = 'stand'  # Default action
is_jumping = False

# Enemies variables
enemies = []
enemy_animation_frame = 0
min_enemy_distance = 150

# Game buttons
start_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 50))
play_music_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 0), (200, 50))
quit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 50))
confirm_character_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 150), (200, 50))

# Draw functions
def draw_button_exit():
    screen.draw.filled_rect(quit_button, (200, 0, 0))
    screen.draw.text("Fechar", center=quit_button.center, fontsize=36, color="white")

def draw_player(opt, pos, shape):
    global character_action, frame_count, is_jumping

    if character_action == 'run':
        shape = 'run'

    if is_jumping:
        shape = 'jump'

    filename = 'alien_' + shape + '_' + opt

    if shape == 'run':
        if frame_count == 0:
            filename += '_1'
        else:
            filename += '_2'

    alien = Actor(filename)
    alien.pos = pos
    alien.draw()

def draw_home():
    screen.clear()
    screen.blit('menu_background', (0, 0))
    screen.draw.text("Select an option:", center=top_center, fontsize=40, color="lightgray")

    screen.draw.filled_rect(start_button, (0, 0, 200))
    screen.draw.text("Start", center=start_button.center, fontsize=36, color="white")

    screen.draw.filled_rect(play_music_button, (0, 200, 0))
    screen.draw.text("Music ON/OFF", center=play_music_button.center, fontsize=36, color="white")
    
    draw_button_exit()

def draw_character_selection():
    global selected_character, character_buttons

    screen.fill((50, 50, 50))
    screen.draw.text("Choose your character:", center=(WIDTH // 2, 40), fontsize=40, color="white")

    characters = ['pink', 'blue', 'green', 'yellow', 'beige']
    shape = 'select'
    spacing = 150
    total_width = (len(characters) - 1) * spacing
    start_x = (WIDTH - total_width) // 2
    y_image = HEIGHT // 2 - 40
    y_text = y_image + 60  # Put name just below image

    global character_buttons
    character_buttons = []  # Clear existing

    for i, char in enumerate(characters):
        x = start_x + i * spacing
        pos = (x, y_image)

        # Draw the character image
        draw_player(char, pos, shape)

        # Highlight if selected
        if selected_character == char:
            highlight_rect = Rect((x - 40, y_image - 50), (80, 100))
            screen.draw.rect(highlight_rect, (255, 255, 0))

        # Draw character name centered below image
        screen.draw.text(char.capitalize(), center=(x, y_text), fontsize=24, color="white")

        # Store clickable rect for this character
        button_rect = Rect((x - 40, y_image - 50), (80, 100))
        character_buttons.append((char, button_rect))

    # Draw confirm button
    screen.draw.filled_rect(confirm_character_button, (0, 0, 200))
    screen.draw.text("Confirmar", center=confirm_character_button.center, fontsize=36, color="white")

def draw_starting():
    global game_state

    screen.clear()
    draw_character_selection()
    draw_button_exit()
    game_state = "start"

def draw_exiting():
    screen.clear()
    screen.draw.text("See you next time!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")

# Levels
def draw_first_level(character):
    global player_pos, enemies
    screen.clear()
    screen.blit('stage_background_first', (0, 0))

    background_width = images.stage_background_first.get_width()
    for i in range(-1, WIDTH // background_width + 2):
        screen.blit('stage_background_first', (i * background_width + world_offset % background_width, 0))

    draw_player(character, player_pos, character_action)

    for enemy in enemies:
        enemy.draw()

def spawn_enemy():
    global enemies, ground_y

    if enemies and (WIDTH + 50 - enemies[-1].x) < min_enemy_distance:
        return

    enemy = Actor("enemy_stand_spider")
    enemy.pos = (WIDTH + 100), ground_y
    enemies.append(enemy)

# PyGame Zero functions
def draw():
    global game_state, game_started, game_over

    screen.clear()

    if game_state == "home" and not game_started:
        draw_home()
    elif game_state == "start" and game_started:
        draw_starting()
    elif game_state == "playing" and game_started:
        draw_first_level(selected_character)
    elif game_state == "exit":
        draw_exiting()

def update():
    global game_state, play_music, music_playing, game_started, game_over, world_offset
    global run_frame, frame_count, character_action, player_speed, velocity_y, is_jumping
    global player_pos, enemies, selected_character, enemy_animation_frame

    moving = False

    if game_state == "exit":
        screen.clear()

    if game_state == "playing":

        clock.schedule_interval(spawn_enemy, 2.0)

        # Horizontal movement
        if keyboard.right:
            world_offset -= player_speed
            character_action = 'run'
            moving = True
        elif keyboard.left:
            world_offset += player_speed
            chracter_action = 'run'
            moving = True

        # Jump key
        if keyboard.up or keyboard.space and not is_jumping:
            is_jumping = True
            velocity_y = jump_strength

        # Apply Gravity
        velocity_y += gravity
        player_pos[1] += velocity_y

        # Prevent failing through the ground
        if player_pos[1] >= ground_y:
            player_pos[1] = ground_y
            is_jumping = False
            velocity_y = 0

        # Animation handling
        if not moving and not is_jumping:
            character_action = 'stand'
            run_frame = 0
        elif moving:
            frame_count += 1
            if frame_count >= 8:
                run_frame = (run_frame + 1) % 2
                frame_count = 0

    if game_state == "home":
        if not music_playing and play_music:
            sounds.home.play()
            music_playing = True

    if game_state == "start" and not game_started:
        game_started = True 

    # Enemies handling
    for enemy in enemies:
        enemy.x -= 2

    if frame_count % 10 == 0:
        enemy_animation_frame = (enemy_animation_frame + 1) % 2

    # Remove enemies off-screen
    enemies[:] = [e for e in enemies if e.right > 0]

    # Check for collision
    for enemy in enemies:
        enemy.image = "enemy_run_spider_1" if enemy_animation_frame == 0 else "enemy_run_spider_2"
        if enemy.colliderect(Actor("alien_run_" + selected_character + "_1", pos=player_pos)):
            print("Hit by enemy!")

def on_mouse_down(pos):
    global game_state, game_started, play_music, music_playing, selected_character, character_buttons

    for char, rect in character_buttons:
        if rect.collidepoint(pos):
            selected_character = char

    if confirm_character_button.collidepoint(pos):
        if game_state == "start" and not selected_character == None:
            game_state = "playing"
            draw_first_level(selected_character)
    
    if game_state == "start" and quit_button.collidepoint(pos):
        game_state = "exit"

    if game_state == "home" and quit_button.collidepoint(pos):
        game_state = "exit"

    if game_state == "home" and play_music_button.collidepoint(pos):

        if play_music == True and music_playing:
            sounds.home.stop()
            play_music = False
            music_playing = False
        elif play_music == False and not music_playing:
            sounds.home.play()
            play_music = True
            music_playing = True
        elif play_music == True and not music_playing:
            sounds.home.play()
            music_playing = True
        elif play_music == False and music_playing:
            sounds.home.stop()
            music_playing = False

    if game_state == "home":
        if start_button.collidepoint(pos) and not game_started:
            game_state = "start"
            game_started = True
            draw_starting()
