import pygame
import random
import settings

upgrade_cache = []

def apply_upgrade(player, upgrade_type):
    upgrade = settings.UPGRADES.get(upgrade_type)
    if not upgrade:
        return False

    max_level = upgrade["levels"]
    current_level = player.upgrades.get(upgrade_type, 0)

    if current_level >= max_level:
        return False

    player.upgrades[upgrade_type] = current_level + 1

    if upgrade_type == "fire_rate":
        player.shoot_delay = max(100, player.shoot_delay - 50)
    elif upgrade_type == "speed":
        player.base_acceleration += 20
    elif upgrade_type == "health":
        player.lives += 1
    elif upgrade_type == "damage":
        pass        
    return True

def draw_upgrade_menu(screen, player):
    global upgrade_cache

    overlay = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 24)

    title = big_font.render("LEVEL UP!", True, settings.WHITE)
    subtitle = font.render("Choose an upgrade:", True, settings.WHITE)

    title_rect = title.get_rect(center=(settings.SCREEN_SIZE[0] // 2, 80))
    subtitle_rect = subtitle.get_rect(center=(settings.SCREEN_SIZE[0] // 2, 140))

    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)

    all_upgrade_types = ["fire_rate", "speed", "health", "damage"]
    if not upgrade_cache:
        upgrade_cache = random.sample(all_upgrade_types, 3)

    icons = {
        "fire_rate": pygame.image.load("assets/fire_rate.png"),
        "speed": pygame.image.load("assets/speed.png"),
        "health": pygame.image.load("assets/health.png"),
        "damage": pygame.image.load("assets/damage.png")
    }

    descriptions = {
        "fire_rate": "+50% fire rate",
        "speed": "+50% speed",
        "health": "+1 life",
        "damage": "+50% bullet damage"
    }

    box_size = 100
    padding = 40
    start_x = (settings.SCREEN_SIZE[0] - (len(upgrade_cache) * (box_size + padding) - padding)) // 2
    y = 200

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    for idx, upgrade_type in enumerate(upgrade_cache):
        x = start_x + idx * (box_size + padding)
        rect = pygame.Rect(x, y, box_size, box_size)

        hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (200, 200, 200) if hovered else settings.WHITE, rect, 2)

        icon = pygame.transform.scale(icons[upgrade_type], (box_size - 20, box_size - 20))
        screen.blit(icon, (x + 10, y + 10))

        level = player.upgrades.get(upgrade_type, 0)
        max_level = settings.UPGRADES[upgrade_type]["levels"]

        text = font.render(f"{level}/{max_level}", True, settings.WHITE)
        text_rect = text.get_rect(center=(x + box_size // 2, y + box_size + 20))
        screen.blit(text, text_rect)

        title_text = font.render(upgrade_type.replace("_", " ").title(), True, settings.WHITE)
        title_rect = title_text.get_rect(center=(x + box_size // 2, y - 30))
        screen.blit(title_text, title_rect)

        desc_text = small_font.render(descriptions[upgrade_type], True, settings.WHITE)
        desc_rect = desc_text.get_rect(center=(x + box_size // 2, y + box_size + 80))
        screen.blit(desc_text, desc_rect)

        if hovered and mouse_clicked:
            if apply_upgrade(player, upgrade_type):
                upgrade_cache = []
                return True
    return False 

