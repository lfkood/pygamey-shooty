import pygame
import random
import settings
from pygame.math import Vector2
import src.entities.weapons as weapons

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
    elif upgrade_type == "sniper":
        player.weapon = weapons.Weapon_sniper()
    elif upgrade_type == "laser":
        player.weapon = weapons.Weapon_laser()
    elif upgrade_type == "shotgun":
        player.weapon = weapons.Weapon_shotgun()
    return True

def draw_upgrade_menu(screen, player):
    global upgrade_cache

    overlay = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    bg = pygame.image.load("assets/upgrade-bg.png").convert_alpha()
    bg = pygame.transform.scale(bg, settings.SCREEN_SIZE)
    screen.blit(bg, (0, 0))

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    all_upgrade_types = ["fire_rate", "speed", "health", "damage"]
    weapon_upgrades = ["sniper", "shotgun", "laser"]
    #new_weapon = bool(round(random.random()/2))
    new_weapon = 1
    if not upgrade_cache:
        if new_weapon:
            upgrade_cache = random.sample(all_upgrade_types, 2) + random.sample(weapon_upgrades, 1) 
        else:
            upgrade_cache = random.sample(all_upgrade_types, 3)
    

    icons = {
        "fire_rate": pygame.image.load("assets/upgrade-rate.png"),
        "speed": pygame.image.load("assets/upgrade-speed.png"),
        "health": pygame.image.load("assets/upgrade-health.png"),
        "damage": pygame.image.load("assets/upgrade-dmg.png"),
        "sniper": pygame.image.load("assets/weapon_sniper.png"),
        "shotgun": pygame.image.load("assets/weapon_shotgun.png"),
        "laser": pygame.image.load("assets/weapon_laser.png"),
    }

    descriptions = {
        "fire_rate": "+50% fire rate",
        "speed": "+50% speed",
        "health": "+1 life",
        "damage": "+50% bullet damage",
        "sniper": "sniper weapon",
        "laser": "laser weapon",
        "shotgun": "shotgun weapon",
    }

    box_size = 100
    padding = 40
    start_x = (settings.SCREEN_SIZE[0] - (len(upgrade_cache) * (box_size + padding) - padding)) // 2
    y = 300

    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    for idx, upgrade_type in enumerate(upgrade_cache):
        x = start_x + idx * (box_size + padding)
        rect = pygame.Rect(x, y, box_size, box_size)

        icon = pygame.transform.scale(icons[upgrade_type], (box_size - 20, box_size - 20))
        screen.blit(icon, (x + 10, y + 10))

        hovered = rect.collidepoint(mouse_pos)
        if rect.collidepoint(mouse_pos):
            selection_overlay = pygame.image.load("assets/upgrade-sel.png")
            selection_overlay = pygame.transform.scale(selection_overlay, (box_size - 20, box_size - 20))
            screen.blit(selection_overlay, (x + 10, y + 10))

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

