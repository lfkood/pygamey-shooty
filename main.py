"""
Main game module for Space Fighter game.

This module contains the main Game class which controls the game loop,
handles events, updates game state, and renders all game elements.
"""
import pygame
from pygame.math import Vector2
import sys
from src.entities.player import Player
import src.entities.bullet
import src.entities.enemy
import settings
import src.utils.upgrades as upgrades


class Game:
    """
    Main game class that controls the game loop and all game elements.
    
    This class initializes the game, handles user input, updates game state,
    and renders all game elements to the screen.
    """
    def __init__(self):
        """
        Initialize the game with default settings.
        
        Sets up pygame, loads assets, and initializes game state variables.
        """
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        pygame.display.set_caption("Space Fighter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = settings.MENU
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 74)

        self.start_btn_rect = None
        self.diff_rects = []
        self.last_press = 0
        
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
        """
        Initialize or reset the game state for a new game.
        
        Creates player and enemy groups, resets timers, score, and other game variables.
        """
        self.player = Player((settings.SCREEN_SIZE[0] // 2, settings.SCREEN_SIZE[1] - 50), 0)
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_timer_2 = 0

        self.spawn_delay = 1000
        self.spawn_delay_2 = 3000

        self.score = 0
        self.auto_shoot_timer = 0
        self.player.upgrade_points = 0
        self.has_upgrade_available = False


    def handle_events(self):
        """
        Process all game events and user input.
        
        Handles mouse clicks, keyboard input, and pygame events based on current game state.
        """
        event_queue = pygame.event.get()
        for event in event_queue:
            if event.type == pygame.QUIT:
                self.running = False
            
            # Debounce
            mouse_pos = Vector2(pygame.mouse.get_pos())
            debounce = 0.2
            button_pressed = False
            if pygame.mouse.get_pressed()[0] and self.last_press + debounce < pygame.time.get_ticks():
                button_pressed = True
                self.last_press = pygame.time.get_ticks()
                        
            # Menu highlighting
            if self.state == settings.MENU: # Because mouse button isnt a KEYDOWN event
                if button_pressed and self.start_btn_rect.collidepoint(mouse_pos):
                    self.state = settings.DIFF_SELECT
            
            if self.state == settings.DIFF_SELECT:
                if button_pressed:
                    mouse_rect = pygame.Rect(mouse_pos.x, mouse_pos.y, 1, 1)
                    self.difficulty = mouse_rect.collidelist(self.diff_rects)
                    if self.difficulty != -1:
                        self.state = settings.PLAYING
            
            if event.type == pygame.KEYDOWN:
                if self.state == settings.MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = settings.PLAYING


                elif self.state == settings.PLAYING:
                    if event.key == pygame.K_u:
                        self.upgrade_menu_active = not self.upgrade_menu_active



                elif self.state == settings.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.init_game()
                        self.state = settings.PLAYING

    def update(self, dt):
        """
        Update game state for the current frame.
        
        Args:
            dt (float): Delta time in seconds since the last frame.
        
        Updates player, enemies, bullets, checks for collisions, handles level progression,
        and updates game state.
        """
        if self.state != settings.PLAYING or self.upgrade_menu_active:
            return

        current_time = pygame.time.get_ticks()

        # Check for level up
        if self.score >= settings.LEVEL_UP_SCORE * self.level:
            self.level += 1
            self.spawn_delay = max(200, self.spawn_delay - 100)
            self.spawn_delay_2 = max(200, self.spawn_delay_2 - 100)
            
            self.has_upgrade_available = True
            self.upgrade_menu_active = True

        if pygame.mouse.get_pressed()[0]:
            self.player.shoot()


        # Enemy spawning with difficulty settings
        if current_time - self.spawn_timer >= self.spawn_delay:
            self.enemies.add(src.entities.enemy.Enemy_1(settings.SCREEN_SIZE[0], self.player, self.difficulty, self.level/2))
            self.spawn_timer = current_time
        if current_time - self.spawn_timer_2 >= self.spawn_delay_2 and self.level > 3:
            self.enemies.add(src.entities.enemy.Enemy_2(settings.SCREEN_SIZE[0], self.player, self.difficulty, self.level/2))
            self.spawn_timer_2 = current_time

        self.player.handle_movement(dt)
        self.enemies.update(dt)
        self.player.bullets.update(dt)
        
        # Update damage indicators
        src.entities.enemy.Enemy_1.damage_indicators.update(dt)

        # Check bullet-enemy collisions with health system
        for bullet in self.player.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
            if hits:
                bullet.delete()
                for enemy in hits:
                    if enemy.take_damage(bullet.damage):
                        self.score += enemy.score_value  # Score based on difficulty and level
                        enemy.kill()

        self.check_player_collision()

    def check_player_collision(self):
        """
        Check for collisions between the player and enemies.
        
        Reduces player lives on collision and updates game state if player runs out of lives.
        """
        current_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            distance = self.player.position.distance_to(enemy.position)
            if distance < self.player.radius + 15:
                self.player.get_hit(current_time)
                enemy.kill()
                if self.player.lives <= 0:
                    self.state = settings.GAME_OVER


    def draw_menu(self):
        """
        Draw the main menu screen.
        
        Displays title and start button with hover effects.
        """
        title = pygame.image.load("assets/title.png").convert_alpha()
        title = pygame.transform.scale(title, Vector2(64,12)*8)
        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//3))
        
        start_btn = pygame.image.load("assets/start-btn.png").convert_alpha()
        start_btn = pygame.transform.scale(start_btn, Vector2(39,13)*8)
        start_btn_rect = start_btn.get_rect(center=(settings.SCREEN_SIZE[0]//2, (settings.SCREEN_SIZE[1]//3)*2))
        self.start_btn_rect = start_btn_rect
        
        start_selected_btn = pygame.image.load("assets/start-btn-sel.png").convert_alpha()
        start_selected_btn = pygame.transform.scale(start_selected_btn, Vector2(39,13)*8)
            
        self.screen.blit(title, title_rect)
        if start_btn_rect.collidepoint(Vector2(pygame.mouse.get_pos())):
            self.screen.blit(start_selected_btn, start_btn_rect)
        else:
            self.screen.blit(start_btn, start_btn_rect)
    
    def draw_diff_sel(self):
        """
        Draw the difficulty selection screen.
        
        Displays difficulty options (Easy, Medium, Hard) with hover effects.
        """
        title = pygame.image.load("assets/diff-title.png").convert_alpha()
        title = pygame.transform.scale(title, Vector2(34,12)*8)
        title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//6))
        
        difficulty_btns = [
            [pygame.image.load("assets/diff-easy.png").convert_alpha(), Vector2(28, 10)],
            [pygame.image.load("assets/diff-medium.png").convert_alpha(), Vector2(41, 10)],
            [pygame.image.load("assets/diff-hard.png").convert_alpha(), Vector2(31, 10)],
        ]
        difficulty_btns = [pygame.transform.scale(x, y*8) for x, y in difficulty_btns]
        
        difficulty_selected_btns = [
            [pygame.image.load("assets/diff-easy-sel.png").convert_alpha(), Vector2(28, 10)],
            [pygame.image.load("assets/diff-medium-sel.png").convert_alpha(), Vector2(41, 10)],
            [pygame.image.load("assets/diff-hard-sel.png").convert_alpha(), Vector2(31, 10)],
        ]
        difficulty_selected_btns = [pygame.transform.scale(x, y*8) for x, y in difficulty_selected_btns]
               
        self.diff_rects = []
        for i, x in enumerate(difficulty_btns):
            self.diff_rects.append(x.get_rect(center=(settings.SCREEN_SIZE[0]//2, (settings.SCREEN_SIZE[1]//3) + 50 + 120*i)))
        
        mouse_pos = Vector2(pygame.mouse.get_pos())
        
        self.screen.blit(title, title_rect)
        for i, x in enumerate(self.diff_rects):
            if x.collidepoint(mouse_pos):
                self.screen.blit(difficulty_selected_btns[i], x)
            else:
                print(difficulty_btns)
                print(self.diff_rects)
                self.screen.blit(difficulty_btns[i], x)

    def draw_game_over(self):
        """
        Draw the game over screen.
        
        Displays final score and restart instructions.
        """
        game_over = self.big_font.render("GAME OVER", True, settings.WHITE)
        score_text = self.big_font.render(f"Score: {self.score}", True, settings.WHITE)
        restart_text = self.font.render("Press SPACE to Restart", True, settings.WHITE)

        game_over_rect = game_over.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//3))
        score_rect = score_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]//2))
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_SIZE[0]//2, settings.SCREEN_SIZE[1]*2//3))

        self.screen.blit(game_over, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def draw_level_progress_bar(self):
        """
        Draw a progress bar showing progress toward the next level.
        
        Visualizes current score progress as a percentage toward leveling up.
        """
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
        """
        Render all game elements to the screen based on current game state.
        
        Handles rendering for different game states (menu, playing, game over).
        """
        # Draw background
        self.screen.blit(self.background, (0, 0))

        if self.state == settings.MENU:
            self.draw_menu()
        elif self.state == settings.DIFF_SELECT:
            self.draw_diff_sel()
        elif self.state == settings.PLAYING:
            # Draw game elements
            self.player.update(pygame.time.get_ticks(), self.screen, self.player_model)
            self.player.bullets.draw(self.screen)
            self.enemies.draw(self.screen)
            
            # Draw health bars for all enemies
            for enemy in self.enemies:
                enemy.draw_health_bar(self.screen)
            
            # Draw damage indicators
            src.entities.enemy.Enemy_1.damage_indicators.draw(self.screen)

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

            # Draw upgrade menu if active
            if self.upgrade_menu_active:
                if upgrades.draw_upgrade_menu(self.screen, self.player):
                    self.upgrade_menu_active = False
        elif self.state == settings.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def run(self):
        """
        Start the main game loop.
        
        Controls the game timing, updates, rendering, and handles exit conditions.
        """
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