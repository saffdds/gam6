import pygame
import random

# --- COSTANTI ---
WIDTH, HEIGHT = 500, 600
WHITE, RED, BLUE, BLACK, GREEN, GRAY = (255, 255, 255), (200, 0, 0), (0, 0, 200), (0, 0, 0), (0, 200, 0), (100, 100, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gam6 Version 3.0")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
title_font = pygame.font.SysFont(None, 80)

high_score = 0

# --- CLASSI ---

class Auto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-70))
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 100:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 100:
            self.rect.x += self.speed

class Ostacolo(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(random.randint(100, WIDTH-150), -100))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        # Non mettiamo self.kill() qui, lo gestiamo nel game_loop per il punteggio!

# --- MENÙ ---

def main_menu():
    global high_score
    while True:
        screen.fill(BLACK)
        title_text = title_font.render("GAME /IO!", True, GREEN)
        screen.blit(title_text, (WIDTH//2 - 150, HEIGHT//2 - 200))

        buttons = [
            ("Gioca", HEIGHT//2 - 40, GREEN),
            ("Istruzioni", HEIGHT//2 + 40, BLUE),
            ("Esci", HEIGHT//2 + 120, RED)
        ]
        
        button_rects = []
        for text, y, color in buttons:
            rect = pygame.draw.rect(screen, color, (WIDTH//2 - 100, y, 200, 50))
            button_rects.append(rect)
            txt_surf = font.render(text, True, WHITE)
            screen.blit(txt_surf, (WIDTH//2 - 40 if text != "Istruzioni" else WIDTH//2 - 60, y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if button_rects[0].collidepoint(pos): game_loop()
                if button_rects[1].collidepoint(pos): instructions_screen()
                if button_rects[2].collidepoint(pos): 
                    pygame.quit()
                    return

def instructions_screen():
    showing = True
    while showing:
        screen.fill(BLACK)
        instr_title = game_over_font.render("ISTRUZIONI", True, GREEN)
        screen.blit(instr_title, (WIDTH//2 - 150, 80))
        lines = ["Usa le Frecce per muoverti.", "Evita i blocchi rossi.", "La velocità aumenta!", "Premi ESC per tornare."]
        for i, line in enumerate(lines):
            screen.blit(font.render(line, True, WHITE), (50, 200 + i*50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                showing = False

# --- GAME LOOP ---

def game_loop():
    global high_score
    player = Auto()
    all_sprites = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()
    score = 0
    obs_speed = 5
    running = True

    while running:
        clock.tick(60)
        screen.fill(GRAY)
        
        # Sfondo Strada
        pygame.draw.rect(screen, BLACK, (100, 0, 300, HEIGHT)) 
        for i in range(0, HEIGHT, 40): 
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i, 10, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return

        all_sprites.update()

        # Generatore ostacoli
        if random.randint(1, 30) == 1:
            new_obs = Ostacolo(obs_speed)
            all_sprites.add(new_obs)
            obstacles.add(new_obs)

        # --- GESTIONE PUNTEGGIO E RIMOZIONE ---
        for o in list(obstacles): # Usiamo list() per evitare errori durante la rimozione
            if o.rect.top > HEIGHT:
                score += 1
                o.kill() # Rimuove dallo sprite group e libera RAM
                if score % 5 == 0:
                    obs_speed += 1

        # Collisioni
        if pygame.sprite.spritecollide(player, obstacles, False):
            running = False

        all_sprites.draw(screen)
        
        # Testo Punteggio
        score_surf = font.render(f"Punteggio: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        
        pygame.display.flip()

    if score > high_score: 
        high_score = score
    game_over_screen(score)

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        over_text = game_over_font.render("GAME OVER", True, RED)
        res_text = font.render(f"Punteggio: {score}  Record: {high_score}", True, WHITE)
        screen.blit(over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        screen.blit(res_text, (WIDTH//2 - 120, HEIGHT//2 + 30))
        
        btn = pygame.draw.rect(screen, GREEN, (WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50))
        screen.blit(font.render("Ricomincia", True, WHITE), (WIDTH//2 - 65, HEIGHT//2 + 110))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(event.pos):
                    return # Torna al main_menu

if __name__ == "__main__":
    main_menu()