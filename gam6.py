import pygame
import random

pygame.init()

# Dimensioni finestra
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("game /io!")

# Colori
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# Font
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
title_font = pygame.font.SysFont(None, 80)

clock = pygame.time.Clock()

# Record
high_score = 0

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)

        # Titolo
        title_text = title_font.render("GAME /IO!", True, GREEN)
        screen.blit(title_text, (WIDTH//2 - 150, HEIGHT//2 - 200))

        # Pulsanti
        button_width, button_height = 200, 50
        play_button_x = WIDTH // 2 - button_width // 2
        play_button_y = HEIGHT // 2 - 40
        instr_button_x = WIDTH // 2 - button_width // 2
        instr_button_y = HEIGHT // 2 + 40
        quit_button_x = WIDTH // 2 - button_width // 2
        quit_button_y = HEIGHT // 2 + 120

        # Disegna pulsante Play
        pygame.draw.rect(screen, GREEN, (play_button_x, play_button_y, button_width, button_height))
        play_text = font.render("Gioca", True, WHITE)
        screen.blit(play_text, (play_button_x + 60, play_button_y + 10))

        # Disegna pulsante Istruzioni
        pygame.draw.rect(screen, BLUE, (instr_button_x, instr_button_y, button_width, button_height))
        instr_text = font.render("Istruzioni", True, WHITE)
        screen.blit(instr_text, (instr_button_x + 40, instr_button_y + 10))

        # Disegna pulsante Quit
        pygame.draw.rect(screen, RED, (quit_button_x, quit_button_y, button_width, button_height))
        quit_text = font.render("Esci", True, WHITE)
        screen.blit(quit_text, (quit_button_x + 70, quit_button_y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Play
                if (play_button_x <= mouse_x <= play_button_x + button_width and
                    play_button_y <= mouse_y <= play_button_y + button_height):
                    game_loop()
                # Istruzioni
                if (instr_button_x <= mouse_x <= instr_button_x + button_width and
                    instr_button_y <= mouse_y <= instr_button_y + button_height):
                    instructions_screen()
                # Quit
                if (quit_button_x <= mouse_x <= quit_button_x + button_width and
                    quit_button_y <= mouse_y <= quit_button_y + button_height):
                    menu_running = False

def instructions_screen():
    showing = True
    while showing:
        screen.fill(BLACK)

        # Titolo
        instr_title = game_over_font.render("ISTRUZIONI", True, GREEN)
        screen.blit(instr_title, (WIDTH//2 - 150, 80))

        # Testo istruzioni
        lines = [
            "Usa le Tasti freccia per muovere l'auto.",
            "Evita gli ostacoli rossi.",
            "Ogni ostacolo superato aumenta il punteggio.",
            "La velocità aumenta col tempo!",
            "Premi ESC per tornare al menu."
        ]
        y = 200
        for line in lines:
            text = font.render(line, True, WHITE)
            screen.blit(text, (50, y))
            y += 50

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing = False

def game_loop():
    global high_score
    car_width, car_height = 50, 80
    car_x = WIDTH // 2 - car_width // 2
    car_y = HEIGHT - car_height - 20
    car_speed = 7

    obstacle_width, obstacle_height = 50, 80
    obstacle_speed = 5
    obstacles = []

    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(30)
        screen.fill(GRAY)

        # Disegna strada
        pygame.draw.rect(screen, BLACK, (100, 0, 300, HEIGHT))
        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i, 10, 20))

        # Eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controlli
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 100:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width - 100:
            car_x += car_speed

        # Genera ostacoli
        if random.randint(1, 30) == 1:
            obstacles.append([random.randint(100, WIDTH - 100 - obstacle_width), -obstacle_height])

        # Muovi ostacoli
        for obs in obstacles[:]:
            obs[1] += obstacle_speed
            if obs[1] > HEIGHT:
                obstacles.remove(obs)
                score += 1
                if score % 5 == 0:
                    obstacle_speed += 1

        # Disegna auto
        pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))

        # Disegna ostacoli
        for obs in obstacles:
            pygame.draw.rect(screen, RED, (obs[0], obs[1], obstacle_width, obstacle_height))
            if (car_x < obs[0] + obstacle_width and
                car_x + car_width > obs[0] and
                car_y < obs[1] + obstacle_height and
                car_y + car_height > obs[1]):
                game_over = True
                running = False

        # Mostra punteggio
        score_text = font.render(f"Punteggio: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    if game_over:
        if score > high_score:
            high_score = score
        game_over_screen(score, high_score)

def game_over_screen(score, high_score):
    button_width, button_height = 200, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 + 80

    waiting = True
    while waiting:
        screen.fill(BLACK)

        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        final_score = font.render(f"Punteggio finale: {score}", True, WHITE)
        record_text = font.render(f"Record: {high_score}", True, GREEN)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(final_score, (WIDTH//2 - 120, HEIGHT//2 + 30))
        screen.blit(record_text, (WIDTH//2 - 80, HEIGHT//2 + 60))

        pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
        button_text = font.render("Ricomincia", True, WHITE)
        screen.blit(button_text, (button_x + 40, button_y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (button_x <= mouse_x <= button_x + button_width and
                    button_y <= mouse_y <= button_y + button_height):
                    main_menu()

# Avvio dal menu
main_menu()
pygame.quit()
