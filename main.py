import pygame
import sys
from src.entities.player import Player
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
import settings

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        pygame.display.set_caption("Space Fighter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = settings.MENU
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 74)

        # Load background
        self.background = pygame.image.load("assets/bg.jpg").convert()
        self.background = pygame.transform.scale(self.background, settings.SCREEN_SIZE)
        self.player_model = pygame.image.load("assets/mc.png").convert_alpha()

        self.init_game()

    def init_game(self):
        self.player = Player((settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] - 50), 0)
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_delay = 1000
        self.score = 0
        self.auto_shoot_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == settings.MENU:
                        self.state = settings.PLAYING
                    elif self.state == settings.GAME_OVER:
                        self.init_game()
                        self.state = settings.PLAYING

    def check_player_collision(self):
        current_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            distance = self.player.position.distance_to(enemy.position)
            if distance < self.player.radius + 15:
                self.player.get_hit(current_time)
                enemy.kill()
                if self.player.lives <= 0:
                    self.state = settings.GAME_OVER

    def update(self, dt):
        if self.state != settings.PLAYING:
            return

        current_time = pygame.time.get_ticks()

        # Auto-shooting
        if current_time - self.auto_shoot_timer >= self.player.shoot_delay:
            bullet = Bullet(self.player.center, self.player.rotation)
            self.player.bullets.add(bullet)
            self.auto_shoot_timer = current_time

        # Enemy spawning
        if current_time - self.spawn_timer >= self.spawn_delay:
            self.enemies.add(Enemy(settings.SCREEN_SIZE[0]))
            self.spawn_timer = current_time

        self.player.handle_movement(dt)
        self.enemies.update(dt)

        self.player.bullets.update(dt)

        # Check collisions and update score
        hits = pygame.sprite.groupcollide(self.player.bullets, self.enemies, True, True)
        self.score += len(hits)
        self.check_player_collision()

    def draw_menu(self):
        title = self.big_font.render("SPACE FIGHTER", True, settings.WHITE)
        start_text = self.font.render("Press SPACE to Start", True, settings.WHITE)

        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//3))
        start_rect = start_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//2))

        self.screen.blit(title, title_rect)
        self.screen.blit(start_text, start_rect)

    def draw_game_over(self):
        game_over = self.big_font.render("GAME OVER", True, settings.WHITE)
        score_text = self.big_font.render(f"Score: {self.score}", True, settings.WHITE)
        restart_text = self.font.render("Press SPACE to Restart", True, settings.WHITE)

        game_over_rect = game_over.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//3))
        score_rect = score_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//2))
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]*2//3))

        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        current_time = pygame.time.get_ticks()
        if self.state == settings.MENU:
            self.draw_menu()
        elif self.state == settings.PLAYING:
            # Draw game elements
            #pygame.draw.circle(self.screen, settings.WHITE, self.player.position, self.player.radius)
            self.player.update(current_time, self.screen, self.player_model)

            self.player.bullets.draw(self.screen)
            self.enemies.draw(self.screen)

            # Draw lives and score
            lives_text = self.font.render(f'Lives: {self.player.lives}', True, settings.WHITE)
            score_text = self.font.render(f'Score: {self.score}', True, settings.WHITE)
            self.screen.blit(lives_text, (10, 10))
            self.screen.blit(score_text, (10, 50))
        elif self.state == settings.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()