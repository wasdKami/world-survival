import pygame, random

def get_ran_pos():
    pos = pygame.Vector2(random.randint(100, pygame.display.Info().current_w - 100),
                            random.randint(100, pygame.display.Info().current_h - 100))
    return pos