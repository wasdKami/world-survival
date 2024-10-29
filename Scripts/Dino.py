import pygame, random
from DinoType import DinoType
from DinoEmotion import DinoEmotion
from DinoState import DinoState

from GetPos import get_ran_pos
from CheckNearby import check_nearby
from Item import item_list
from Images import triceratops_img, trex_img

dino_list = []

class Dino:
    def __init__(self, name, img, age, level, speed, damage, health = 100, hunger = 100, thirst = 100):
        self.is_alive = True
        self.img = img
        self.name = name
        self.age = age
        self.level = level
        self.health = health
        self.hunger = hunger
        self.thirst = thirst
        self.speed = speed
        self.damage = damage

        self.type_manager = DinoType()
        self.type = self.type_manager.undefined

        self.emotional_manager = DinoEmotion()
        self.emotional_state = self.emotional_manager.happy

        self.state_manager = DinoState()

        self.nearby_list = []
        self.chasing = None
        self.target = get_ran_pos()
        self.finished_path = True

        self.move = pygame.Vector2(0, 0)
        self.pos = get_ran_pos()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.img.get_width(), self.img.get_height())

    #region -- new movement script --
    #step 1: if happy always wander
    #step 2: if angry wander but chase when prey is in range
    #step 3: if sad stand still/sleep or wander small parts
    #step 4: if scared wander but run when predator is in range
    #step 5: get current pos, target pos, distance and direction

    def state_check(self):
        if self.hunger < 30 or self.health < 30 or self.thirst < 30:
            self.state_manager.set_state(self.state_manager.sleep)
        elif self.type_manager.get_state() == self.type_manager.herbivore:
            for each in self.nearby_list:
                if isinstance(each, Dino):
                    if each.type_manager.get_state() == each.type_manager.carnivore:
                        self.state_manager.set_state(self.state_manager.run)
        elif self.type_manager.get_state() == self.type_manager.carnivore:
            for each in self.nearby_list:
                if isinstance(each, Dino):
                    if each.type_manager.get_state() == each.type_manager.herbivore:
                        self.state_manager.set_state(self.state_manager.chase)
        else:
            self.state_manager.set_state(self.state_manager.wander)

        # from main import CURRENT_TICKS
        # print(f'{CURRENT_TICKS}: state from [{self.name}]: {self.state_manager.get_state()} type: {self.type_manager.get_state()}')

    def wander(self):
        self.target = get_ran_pos()

    def chase(self):
        self.target = self.chasing

    def check_prey_in_range(self):
        for each in self.nearby_list:
            if isinstance(each, Triceratops):
                self.chasing = each


    def get_distance(self):
        distance = self.target - self.pos
        return distance

    def get_direction(self, target):
        distance = target - self.pos
        distance.normalize_ip()
        direction = distance
        return direction

    def move_towards_target(self, direction):
        self.move = direction * self.speed
        self.pos += self.move
        self.rect.center = self.pos

    #region -- old movement script --
    #this is not working starting from zero
    #
    # def get_direction(self, target):
    #     target = get_ran_pos()
    #     distance = target - self.pos
    #     try:
    #         distance.normalize_ip()
    #     except ValueError:
    #         ...
    #         #cant normalize Vector of length zero
    #     direction = distance
    #     return direction
    #
    # def is_prey_in_range(self):
    #     for each in self.nearby_list:
    #         if self.type == self.dino_types[2] and each == self.dino_types[1]:
    #             self.target = each.rect.center
    #             return each
    #         else:
    #             return get_ran_pos()
    #
    # def get_target(self):
    #     target = self.get_direction()
    #     return target
    #
    # def move_towards_target(self):
    #     self.move = target_direction * self.speed
    #     self.pos += self.move
    #     self.rect.center = self.pos
    #endregion

    def draw(self):
        from main import SCREEN
        #easier to see what state it is
        if self.state_manager.get_state() == self.state_manager.run:
            pygame.draw.rect(SCREEN, "Yellow", self.rect, 5)
        elif self.state_manager.get_state() == self.state_manager.chase:
            pygame.draw.rect(SCREEN, "Red", self.rect, 5)
        elif self.state_manager.get_state() == self.state_manager.sleep:
            pygame.draw.rect(SCREEN, "Black", self.rect, 5)
        else:
            pygame.draw.rect(SCREEN, "white", self.rect, 5)

        pygame.Surface.blit(SCREEN, self.img, self.rect)

    def update(self):
        if self.health <= 0 or self.thirst <= 0 or self.hunger <= 0:
            self.is_alive = False

        self.state_check()
        self.check_prey_in_range()

        if self.state_manager.get_state() == self.state_manager.run:
            ...
            #run logic
        elif self.state_manager.get_state() == self.state_manager.chase:
            ...
            #chase logic
        elif self.state_manager.get_state() == self.state_manager.sleep:
            ...
            #chase logic
        else:
            #check if reached end
            distance = self.get_distance()
            if distance.x < 1 and distance.y < 1:
                self.wander()
                self.finished_path = True
            else:
                self.finished_path = False

            print(self.state_manager.get_state())
            self.move_towards_target(self.get_direction(self.target))


        #check nearby and add to list
        try:
            for each in check_nearby(self, 100, dino_list):
                self.nearby_list.append(each)

            for each in check_nearby(self, 100, item_list):
                self.nearby_list.append(each)
        except TypeError:
            ...
            # Not sure why this happens i think it has to do with the fact there is nothing else to append or maybe its trying to append twice?

        # self.move_towards_target()
        self.draw()

#region --- subclasses ---
class Triceratops(Dino):
    def __init__(self):
        super().__init__("Triceratops", triceratops_img, 5, 50, 0.6, 10, random.randint(10, 100), random.randint(10, 100), random.randint(10, 100))
        self.type_manager.set_state(self.type_manager.herbivore)


class Trex(Dino):
    def __init__(self):
        super().__init__("Trex", trex_img, 10, 35, 0.5, 25, random.randint(10, 100), random.randint(10, 100), random.randint(10, 100))
        self.type_manager.set_state(self.type_manager.carnivore)
#endregion

#region -- creating instances --
for _ in range(10):
    dino_list.append(Triceratops())

for _ in range(10):
    dino_list.append(Trex())
#endregion

