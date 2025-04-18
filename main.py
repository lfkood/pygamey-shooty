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

        # Set these before init_game
        self.difficulty = settings.NORMAL
        self.level = 1
        self.upgrade_menu_active = False

        self.init_game()

    def init_game(self):
        self.player = Player((settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] - 50), 0)
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_delay = 1000
        self.score = 0
        self.auto_shoot_timer = 0
        self.player.upgrade_points = 100


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == settings.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = settings.PLAYING
                    elif event.key == pygame.K_1:
                        self.difficulty = settings.EASY
                    elif event.key == pygame.K_2:
                        self.difficulty = settings.NORMAL
                    elif event.key == pygame.K_3:
                        self.difficulty = settings.HARD

                elif self.state == settings.PLAYING:
                    if event.key == pygame.K_u:
                        self.upgrade_menu_active = not self.upgrade_menu_active
                    if self.upgrade_menu_active:
                        if event.key == pygame.K_1:
                            self.player.apply_upgrade("fire_rate")
                        elif event.key == pygame.K_2:
                            self.player.apply_upgrade("speed")
                        elif event.key == pygame.K_3:
                            self.player.apply_upgrade("health")

                elif self.state == settings.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.init_game()
                        self.state = settings.PLAYING

    def update(self, dt):
        if self.state != settings.PLAYING or self.upgrade_menu_active:
            return

        current_time = pygame.time.get_ticks()

        # Check for level up
        if self.score >= self.level * settings.LEVEL_UP_SCORE:
            self.level += 1
            self.spawn_delay = max(200, self.spawn_delay - 100)  # Increase difficulty
            self.player.upgrade_points += 100  # Award upgrade points on level up
            # Auto show upgrade menu on level up
            self.upgrade_menu_active = True

        # Auto-shooting
        if current_time - self.auto_shoot_timer >= self.player.shoot_delay:
            bullet = Bullet(self.player.center, self.player.rotation)
            self.player.bullets.add(bullet)
            self.auto_shoot_timer = current_time

        # Enemy spawning with difficulty settings
        if current_time - self.spawn_timer >= self.spawn_delay:
            self.enemies.add(Enemy(settings.SCREEN_SIZE[0], self.player, self.difficulty))
            self.spawn_timer = current_time

        self.player.handle_movement(dt)
        self.enemies.update(dt)
        self.player.bullets.update(dt)

        # Check bullet-enemy collisions with health system
        for bullet in self.player.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if hits:
                bullet.kill()
                for enemy in hits:
                    if enemy.take_damage():
                        self.score += enemy.score_value * self.level  # Score based on difficulty and level
                        enemy.kill()

        self.check_player_collision()

    def check_player_collision(self):
        current_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            distance = self.player.position.distance_to(enemy.position)
            if distance < self.player.radius + 15:
                self.player.get_hit(current_time)
                enemy.kill()
                if self.player.lives <= 0:
                    self.state = settings.GAME_OVER


    def draw_menu(self):
        title = self.big_font.render("SPACE FIGHTER", True, settings.WHITE)
        start_text = self.font.render("Press SPACE to Start", True, settings.WHITE)

        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//3))
        start_rect = start_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//2))

        self.screen.blit(title, title_rect)
        self.screen.blit(start_text, start_rect)
        title = self.big_font.render("SPACE FIGHTER", True, settings.WHITE)
        start_text = self.font.render("Press SPACE to Start", True, settings.WHITE)
        diff_text = self.font.render("Select Difficulty: 1-Easy, 2-Normal, 3-Hard", True, settings.WHITE)

        difficulty_name = ["EASY", "NORMAL", "HARD"][self.difficulty]
        selected_text = self.font.render(f"Current: {difficulty_name}", True, settings.WHITE)

        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] // 3))
        start_rect = start_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] // 2))
        diff_rect = diff_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] // 2 + 50))
        selected_rect = selected_text.get_rect(
            center=(settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] // 2 + 100))

        self.screen.blit(title, title_rect)
        self.screen.blit(start_text, start_rect)
        self.screen.blit(diff_text, diff_rect)
        self.screen.blit(selected_text, selected_rect)

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

    def draw_upgrade_menu(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Draw upgrade options
        title = self.big_font.render("UPGRADES", True, settings.WHITE)
        points_text = self.font.render(f"Upgrade Points: {self.player.upgrade_points}", True, settings.WHITE)

        upgrade_options = [
            f"1. Fire Rate (Level {self.player.upgrades['fire_rate']}/{settings.UPGRADES['fire_rate']['levels']}) - {settings.UPGRADES['fire_rate']['cost']} pts",
            f"2. Speed (Level {self.player.upgrades['speed']}/{settings.UPGRADES['speed']['levels']}) - {settings.UPGRADES['speed']['cost']} pts",
            f"3. Health (Level {self.player.upgrades['health']}/{settings.UPGRADES['health']['levels']}) - {settings.UPGRADES['health']['cost']} pts"
        ]

        close_text = self.font.render("Press U to close", True, settings.WHITE)

        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0] // 2, 100))
        points_rect = points_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, 160))

        self.screen.blit(title, title_rect)
        self.screen.blit(points_text, points_rect)

        y_pos = 220
        for option in upgrade_options:
            option_text = self.font.render(option, True, settings.WHITE)
            option_rect = option_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, y_pos))
            self.screen.blit(option_text, option_rect)
            y_pos += 50

        close_rect = close_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, y_pos + 30))
        self.screen.blit(close_text, close_rect)

    def draw_level_progress_bar(self):
        # Calculate progress percentage
        next_level_threshold = self.level * settings.LEVEL_UP_SCORE
        previous_level_threshold = (self.level - 1) * settings.LEVEL_UP_SCORE
        progress = (self.score - previous_level_threshold) / (next_level_threshold - previous_level_threshold)

        # Draw progress bar
        bar_width = 400
        bar_height = 20
        border = 2

        # Bar position
        x = (settings.SCREEN_SIZE[0] - bar_width) // 2
        y = settings.SCREEN_SIZE[1] - 30

        # Draw border
        pygame.draw.rect(self.screen, settings.WHITE,
                         (x - border, y - border, bar_width + 2 * border, bar_height + 2 * border))

        # Draw background
        pygame.draw.rect(self.screen, settings.BLACK, (x, y, bar_width, bar_height))

        # Draw progress
        progress_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, progress_width, bar_height))

        # Draw text
        progress_text = self.font.render(f"Level Progress: {int(progress * 100)}%", True, settings.WHITE)
        text_rect = progress_text.get_rect(center=(settings.SCREEN_SIZE[0] // 2, y - 15))
        self.screen.blit(progress_text, text_rect)

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))

        if self.state == settings.MENU:
            self.draw_menu()
        elif self.state == settings.PLAYING:
            # Draw game elements
            self.player.update(pygame.time.get_ticks(), self.screen, self.player_model)
            self.player.bullets.draw(self.screen)
            self.enemies.draw(self.screen)

            # Draw lives, score, level
            lives_text = self.font.render(f'Lives: {self.player.lives}', True, settings.WHITE)
            score_text = self.font.render(f'Score: {self.score}', True, settings.WHITE)
            level_text = self.font.render(f'Level: {self.level}', True, settings.WHITE)
            self.screen.blit(lives_text, (10, 10))
            self.screen.blit(score_text, (10, 50))
            self.screen.blit(level_text, (10, 90))

            # Draw level progress bar
            self.draw_level_progress_bar()

            # Upgrade key hint
            upgrade_hint = self.font.render("Press U for upgrades", True, settings.WHITE)
            self.screen.blit(upgrade_hint, (settings.SCREEN_SIZE[0] - 200, 10))

            # Draw upgrade menu if active
            if self.upgrade_menu_active:
                self.draw_upgrade_menu()
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