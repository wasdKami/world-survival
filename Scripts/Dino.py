import pygame
from Images import triceratops_img

dino_list = []

class Dino:
    def __init__(self, name, img, age, health, speed, damage):
        self.img = img
        self.name = name
        self.age = age
        self.health = health
        self.speed = speed
        self.damage = damage

        self.move = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(((pygame.display.Info().current_w / 2) - (self.img.get_width() / 2),
                                   (pygame.display.Info().current_h / 2) - (self.img.get_height() / 2)))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        self.target = None

    def get_direction(self):
        target_pos = pygame.mouse.get_pos()
        distance = target_pos - self.pos
        distance.normalize_ip()
        direction = distance
        return direction

    def move_towards_target(self):
        direction = self.get_direction()
        self.move = direction * self.speed
        self.pos += self.move
        self.rect.center = self.pos

    def draw(self):
        from main import SCREEN
        pygame.Surface.blit(SCREEN, self.img, self.rect)

    def update(self):
        self.draw()
        self.move_towards_target()

triceratops = Dino("triceratops", triceratops_img, 23, 100, 2, 10)
