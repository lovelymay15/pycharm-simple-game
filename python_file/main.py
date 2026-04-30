import random
import pygame

# Initialize Pygame
pygame.init()

# Screen settings
width, height = 790, 580
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('SHOOT, BABY, SHOOT!')
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# Images
player = pygame.image.load("baby.png")
background = pygame.image.load("background.jpg")
milk = pygame.image.load("milk.gif")
bazooka = pygame.image.load("bullet.png")
bad_guy_img = pygame.image.load("bad_baby.png")
player_health_bar = pygame.image.load("health_bar.png")
player_health = pygame.image.load("health.png")
game_over = pygame.image.load("game_over.png")
player_win = pygame.image.load("player_win.png")

# Sounds
hit_enemy = pygame.mixer.Sound("audio_hit_enemy.wav")
shoot = pygame.mixer.Sound("audio_shoot.wav")
lose = pygame.mixer.Sound("audio_game_over.mp3")
win = pygame.mixer.Sound("audio_player_win.mp3")
audio_welcome_text = pygame.mixer.Sound("audio_welcome_text.mp3")

hit_enemy.set_volume(0.1)
shoot.set_volume(0.1)
lose.set_volume(0.3)
win.set_volume(0.3)

# Game variables
keys = [False, False]
player_pos = [width // 8, height // 2]
bad_timer = 100
bad_timer1 = 0
bad_guys = []
health_value = 194
acc = [0, 0]
bullets = []
milk_health = [100, 100, 100, 100]
score = 0
milk_lanes = [70, 200, 340, 460]
enemy_speed = 7
max_enemies = 1000


def spawn_enemy():
    global bad_timer, bad_timer1, bad_guys, max_enemies

    bad_timer -= 1
    if bad_timer == 0 and len(bad_guys) < max_enemies:
        selected_lane = random.choice(milk_lanes)
        bad_guys.append([width, selected_lane])
        bad_timer = 100 - (bad_timer1 * 2)
        if bad_timer1 >= 35:
            bad_timer1 = 35
        else:
            bad_timer1 += 5


def update_enemy_speed(time_left):
    global enemy_speed
    enemy_speed = min(20, 10 + (60 - time_left) // 3)  # Increase the speed as time decreases


def draw_player(x, y):
    screen.blit(player, (x, y))


def draw_enemy(x, y):
    screen.blit(bad_guy_img, (x, y))


def draw_milk():
    for i, health_value in enumerate(milk_health):
        if health_value > 0:
            screen.blit(milk, (10, 50 + i * 130))
            pygame.draw.rect(screen, (255, 0, 0), (10, 170 + i * 130, 100, 4))
            pygame.draw.rect(screen, (0, 128, 0), (10, 170 + i * 130, health_value, 4))


def draw_health_bar():
    screen.blit(player_health_bar, (5, 5))
    for health_bar_x in range(health_value):
        screen.blit(player_health, (health_bar_x + 8, 8))


def draw_bullets():
    for bullet in bullets:
        vel_x = 20
        vel_y = 0
        bullet[0] += vel_x
        bullet[1] += vel_y
        screen.blit(bazooka, (bullet[0], bullet[1]))


def draw_score():
    font = pygame.font.Font(None, 24)
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (width - 400, 5))


def draw_timer():
    font = pygame.font.Font(None, 24)
    time_remaining = max(0, 60 - pygame.time.get_ticks() // 1000)
    time_text = font.render("Time Left: " + str(time_remaining), True, (0, 0, 0))
    screen.blit(time_text, (width - 150, 5))


def show_game_result(time_remaining):
    pygame.mixer.music.stop()  # Stop the bg.mp3 music

    # Display win or lose screen based on game outcome
    if time_remaining == 0 and any(hp > 0 for hp in milk_health):
        screen.fill(0)
        screen.blit(player_win, (0, 0))
        win.play()
    else:
        screen.fill(0)
        screen.blit(game_over, (0, 0))
        lose.play()

    # Display the player's score
    score_text = font.render("Your Score: " + str(score), True, (255, 255, 255))  # White text for player score
    score_rect = score_text.get_rect(center=(width // 2, height // 1.2))
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(0)


def render_text_lines(lines, y_offset=0):
    rendered_lines = []
    for i, line in enumerate(lines):
        if len(line) > len(rendered_lines):
            rendered_lines.append(font.render(line[:len(rendered_lines) + 1], True, (255, 255, 255)))

    for i, rendered_line in enumerate(rendered_lines):
        screen.blit(rendered_line, (100, 120 + y_offset + i * 30))


def main():
    global health_value, font, score
    # Load welcome screen music
    audio_welcome_text.play()

    # Show the welcome message and ask if the player wants to play
    font = pygame.font.Font(None, 24)
    message_lines = ["WELCOME BABY!",
                     "Zombie babies are attacking your house and want to steal your baby formulas.",
                     "Protect them with your poop bazooka.",
                     "SHOOT, BABY, SHOOT!",
                     "*Use the UP and DOWN keys to move the baby and SPACE to shoot bullets",
                     "Press ENTER to Play or ESC to Quit"]

    y_offsets = [0, 30, 60, 90, 220, 350]  # Vertical position of each line

    show_welcome = True
    typing_timer = pygame.time.get_ticks()
    typing_delay = 17  # Typing speed (increased to slow down the typing effect)
    text_lines_index = [0] * len(message_lines)

    while show_welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    audio_welcome_text.stop()
                    show_welcome = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(0)

        # Clear the screen
        screen.fill(0)

        # Render the welcome message
        current_time = pygame.time.get_ticks()
        for i, line in enumerate(message_lines):
            if text_lines_index[i] < len(line):
                if current_time - typing_timer > typing_delay:
                    text_lines_index[i] += 1
                    typing_timer = current_time

            rendered_text = font.render(line[:text_lines_index[i]], True, (255, 255, 255))
            screen.blit(rendered_text, (100, 120 + y_offsets[i]))

        pygame.display.flip()

    # Load game background music
    pygame.mixer.music.load("bg.mp3")
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.20)

    # Set up clock
    clock = pygame.time.Clock()

    spawn_delay = 5  # Milliseconds delay between enemy spawns
    last_spawn_time = pygame.time.get_ticks()  # Store the last spawn time

    running = True

    while running:
        clock.tick(60)  # Limit the frame rate to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    keys[0] = True
                elif event.key == pygame.K_DOWN:
                    keys[1] = True
                elif event.key == pygame.K_SPACE:
                    shoot.play()
                    bullets.append([player_pos[0] + 32, player_pos[1] + 32])
                elif event.key == pygame.K_ESCAPE:  # Exit the game if ESC key is pressed
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    keys[0] = False
                elif event.key == pygame.K_DOWN:
                    keys[1] = False

        player_speed = 20
        if keys[0] and player_pos[1] > milk_lanes[0]:
            player_pos[1] -= player_speed
        elif keys[1] and player_pos[1] < milk_lanes[-1]:
            player_pos[1] += player_speed

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= spawn_delay:
            spawn_enemy()
            last_spawn_time = current_time

        # Update enemy speed based on time remaining
        time_remaining = max(0, 60 - pygame.time.get_ticks() // 1000)
        update_enemy_speed(time_remaining)

        screen.fill(0)

        for x in range(width // background.get_width() + 1):
            for y in range(height // background.get_height() + 1):
                screen.blit(background, (x * 100, y * 100))

        draw_milk()
        draw_health_bar()
        draw_player(player_pos[0], player_pos[1])
        draw_bullets()

        index = 0
        for bad_guy in bad_guys:
            if bad_guy[0] < -79:
                hit_enemy.play()
                bad_guys.pop(index)
            bad_guy[0] -= enemy_speed

            bad_rect = pygame.Rect(bad_guy_img.get_rect())
            bad_rect.top = bad_guy[1]
            bad_rect.left = bad_guy[0]

            if bad_rect.left < -79:
                health_value -= 7
                bad_guys.pop(index)

            index1 = 0
            for bullet in bullets:
                bull_rect = pygame.Rect(bazooka.get_rect())
                bull_rect.left = bullet[0]
                bull_rect.top = bullet[1]
                if bad_rect.colliderect(bull_rect):
                    hit_enemy.play()
                    if health_value > 194:
                        health_value = 194
                    acc[0] += 1
                    bad_guys.pop(index)
                    bullets.pop(index1)
                    score += 10  # Increase score when the enemy is hit
                    health_value += 1
                index1 += 1

            for i, milk_y in enumerate(milk_lanes):
                milk_rect = milk.get_rect(topleft=(10, milk_y))
                if milk_health[i] > 0 and milk_rect.colliderect(bad_rect):
                    milk_health[i] -= 1  # Reduce castle health
                    if milk_health[i] <= 0:
                        milk_health[i] = 0
                    break

            index += 1

        for bad_guy in bad_guys:
            draw_enemy(bad_guy[0], bad_guy[1])

        draw_score()
        draw_timer()

        pygame.display.flip()

        if time_remaining <= 0 or all(hp <= 0 for hp in milk_health) or pygame.time.get_ticks() >= 90000 or health_value <= 0:
            show_game_result(time_remaining)


if __name__ == "__main__":
    main()
