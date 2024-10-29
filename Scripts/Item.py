import pygame
from Images import triceratops_img, trex_img
from GetPos import get_ran_pos

item_list = []
item_types = ["building", "resource", "hunger", "water"]

class Item:
    def __init__(self, name, img, color, item_type, amount):
        self.name = name
        self.img = img
        self.color = color
        self.object_type = item_type
        self.amount = amount

        self.pos = get_ran_pos()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width() / 2, self.img.get_height() / 2)

    def draw(self):
        from main import SCREEN
        # pygame.Surface.blit(SCREEN, self.img, self.rect)
        pygame.draw.rect(SCREEN, self.color, self.rect, 35, 10)


    def update(self):
        self.draw()

class Water(Item):
    def __init__(self):
        super().__init__("water", triceratops_img, "Blue", item_types[3], 100)

class Meat(Item):
    def __init__(self):
        super().__init__("meat", trex_img, "Dark Red", item_types[2], 100)

class Grass(Item):
    def __init__(self):
        super().__init__("Grass", trex_img, "Green", item_types[1], 1)

class Tree(Item):
    def __init__(self):
        super().__init__("Tree", trex_img, "Dark Green", item_types[1], 1)

class Rock(Item):
    def __init__(self):
        super().__init__("Rock", trex_img, "Grey", item_types[1], 100)


for _ in range(5):
    item_list.append(Water())

for _ in range(5):
    item_list.append(Meat())

for _ in range(25):
    item_list.append(Grass())

for _ in range(5):
    item_list.append(Tree())

for _ in range(5):
    item_list.append(Rock())