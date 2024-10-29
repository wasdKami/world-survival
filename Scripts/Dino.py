import pygame
from GetPos import get_ran_pos
from Images import triceratops_img, trex_img

dino_list = []
dino_types = ["herbivore", "carnivore", "omnivore"]

class Dino:
    def __init__(self, name, img, age, speed, damage, dino_type):
        self.img = img
        self.name = name
        self.age = age
        self.health = 100
        self.food = 100
        self.thirst = 100
        self.speed = speed
        self.damage = damage
        self.dino_type = dino_type
        self.states = ["Wander", "Chase"]
        self.state = self.states[0]

        self.target = get_ran_pos()
        self.move = pygame.Vector2(0, 0)
        self.pos = get_ran_pos()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    def get_direction(self):
        if self.state == self.states[1]:
            distance = self.target - self.pos
            distance.normalize_ip()
            direction = distance
            return direction
        else:
            distance = self.target - self.pos
            if distance.x < 1 and distance.y < 1:
                self.target = get_ran_pos()
            distance.normalize_ip()
            direction = distance
            return direction


    def move_towards_target(self):
        direction = self.get_direction()
        self.move = direction * self.speed
        self.pos += self.move
        self.rect.center = self.pos

    def check_nearby(self):
        from main import SCREEN
        for dino in dino_list:
            distance = dino.rect.center - self.pos

            if distance.x < 0:
                distance.x *= -1
            if distance.y < 0:
                distance.y *= -1

            fov = 100
            if distance.x < fov and distance.y < fov:
                pygame.draw.line(SCREEN, "Red", self.rect.center, dino.rect.center)
                if isinstance(self, Trex):
                    if isinstance(dino, Trex):
                        ...
                    if isinstance(dino, Triceratops):
                        self.state = self.states[1]
                        self.target = dino.rect.center

    def draw(self):
        from main import SCREEN
        pygame.Surface.blit(SCREEN, self.img, self.rect)

    def update(self):
        self.draw()
        self.move_towards_target()
        self.check_nearby()

class Triceratops(Dino):
    def __init__(self):
        super().__init__("Triceratops", triceratops_img, 5, 0.3, 10, "Herbivore")

class Trex(Dino):
    def __init__(self):
        super().__init__("Trex", trex_img, 10, 0.5, 25, "Carnivore")

for _ in range(10):
    dino_list.append(Triceratops())

for _ in range(10):
    dino_list.append(Trex())

