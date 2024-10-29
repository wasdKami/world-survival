import pygame
from Images import triceratops_img, trex_img
from GetPos import get_ran_pos

item_list = []
item_types = ["building", "resource", "food", "water"]

class Item:
    def __init__(self, name, img, color, item_type):
        self.name = name
        self.img = img
        self.color = color
        self.object_type = item_type

        self.pos = get_ran_pos()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    def draw(self):
        from main import SCREEN
        # pygame.Surface.blit(SCREEN, self.img, self.rect)
        pygame.draw.rect(SCREEN, self.color, self.rect, 35, 10)


    def update(self):
        self.draw()

class Water(Item):
    def __init__(self):
        super().__init__("water", triceratops_img, "Blue", item_types[3])

class Meat(Item):
    def __init__(self):
        super().__init__("meat", trex_img, "Dark Red", item_types[2])


for _ in range(5):
    item_list.append(Water())

for _ in range(5):
    item_list.append(Meat())