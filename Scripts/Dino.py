import pygame, random
from Images import triceratops_img

dino_list = []

class Dino:
    def __init__(self, name, img, age, speed, damage):
        self.img = img
        self.name = name
        self.age = age
        self.health = 100
        self.food = 100
        self.thirst = 100
        self.speed = speed
        self.damage = damage

        self.move = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(((pygame.display.Info().current_w / 2) - (self.img.get_width() / 2),
                                   (pygame.display.Info().current_h / 2) - (self.img.get_height() / 2)))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())
        self.target = self.get_target()

    def get_target(self):
        target = pygame.Vector2(random.randint(100, pygame.display.Info().current_w - 100), random.randint(100, pygame.display.Info().current_h - 100))
        return target

    def get_direction(self):
        print(f'rect.center: {self.rect.center}')
        print(f'target: {self.target}')
        distance = self.target - self.pos
        if distance.x < 1 and distance.y < 1:
            self.target = self.get_target()
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

triceratops = Dino("triceratops", triceratops_img, 23, 100, 0.3, 10)
