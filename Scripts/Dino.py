import pygame, random
from DinoType import DinoType
from DinoEmotion import DinoEmotion
from DinoState import DinoState

from GetPos import get_ran_pos
# from CheckNearby import check_nearby
# from Item import item_list
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

        self.attack_range = 10

        self.type_manager = DinoType()
        self.type = self.type_manager.undefined

        self.emotional_manager = DinoEmotion()
        self.emotional_state = self.emotional_manager.happy

        self.state_manager = DinoState()

        self.nearby_dino = []
        self.has_target = False
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
        if self.hunger < 10 or self.health < 30 or self.thirst < 10:
            self.state_manager.set_state(self.state_manager.sleep)
        elif self.type_manager.get_state() == self.type_manager.herbivore:
            for each in self.nearby_dino:
                if isinstance(each, Dino):
                    if each.type_manager.get_state() == each.type_manager.carnivore:
                        self.state_manager.set_state(self.state_manager.run)
        elif self.type_manager.get_state() == self.type_manager.carnivore:
            for each in self.nearby_dino:
                if isinstance(each, Dino):
                    if each.type_manager.get_state() == each.type_manager.herbivore:
                        self.state_manager.set_state(self.state_manager.chase)
        else:
            self.state_manager.set_state(self.state_manager.wander)

    def state_move(self):
        if self.state_manager.get_state() == self.state_manager.run:
            closest = self.check_in_range(Trex)
            target = closest
            if self.has_target:
                ...
                #instead of running to eachother he needs to run
                # self.move_towards_target(self.get_direction(target))
        elif self.state_manager.get_state() == self.state_manager.chase:
            closest = self.check_in_range(Triceratops)
            target = closest
            if self.has_target:
                dist = self.get_distance(target)
                if dist.x < 0:
                    dist.x *= -1
                if dist.y < 0:
                    dist.y *= -1

                if dist.x < self.attack_range and dist.y < self.attack_range:
                    kill_list = []
                    self.add_nearby(dino_list, kill_list, 10)
                    for each in kill_list:
                        if isinstance(each, Triceratops):
                            each.is_alive = False
                        else: kill_list.remove(each)
                    self.has_target = False
                    print(f'attacking')
                    #attack logic
                else:
                    self.move_towards_target(self.get_direction(target))
            else:
                self.state_manager.set_state(self.state_manager.wander)
        elif self.state_manager.get_state() == self.state_manager.sleep:
            ...
            #chase logic
        else:
            print(f'self: {self.rect.center}, target: {self.target}')
            #check if reached end
            distance = self.get_distance(self.target)
            if distance.x < 1 and distance.y < 1:
                self.wander()
                self.finished_path = True
            else:
                self.finished_path = False

            self.move_towards_target(self.get_direction(self.target))

        # from main import CURRENT_TICKS
        # print(f'{CURRENT_TICKS}: state from [{self.name}]: {self.state_manager.get_state()} type: {self.type_manager.get_state()}')

    def wander(self):
        self.target = get_ran_pos()

    def chase(self):
        self.target = self.chasing

    def check_in_range(self, target_type):
        nearby_targets = []

        # check if its target type then add to list else skip
        for each in self.nearby_dino:
            if isinstance(each, target_type):
                nearby_targets.append(each)
            else:
                continue

        #check if nearby target list is empty then stop else closest is first
        if len(nearby_targets) <= 0:
            self.state_manager.set_state(self.state_manager.chase)
            self.has_target = False
            return
        else:
            closest = nearby_targets[0]

        # loop through of all nearby targets
        # check if new target is closer then current closest target
        # if closer then make new closest
        for target in nearby_targets:
            dist = self.get_distance(target.rect.center)
            if dist.x < closest.rect.centerx and dist.y < closest.rect.centery:
                closest = target

        self.has_target = True
        return closest.rect.center

    def get_distance(self, target):
        distance = target - self.pos
        return distance

    def get_direction(self, target):
        distance = self.get_distance(target)
        distance.normalize_ip()
        direction = distance
        return direction

    def move_towards_target(self, direction):
        from main import DELTATIME
        self.move = direction * self.speed
        self.pos += self.move * DELTATIME
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
    #     for each in self.nearby_dino:
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

    def add_nearby(self, check_list, add_list, max_dist):
        # check through list of all dinos if any are nearby then add to nearby list
        for other in check_list:
            distance = other.rect.center - self.pos

            # makes negative positive
            if distance.x < 0:
                distance.x *= -1
            if distance.y < 0:
                distance.y *= -1

            if distance.x < max_dist and distance.y < max_dist:
                add_list.append(other)

    def draw_nearby(self):
        # draw lines for every dino and what is in his range
        for each in self.nearby_dino:
            from main import SCREEN
            pygame.draw.line(SCREEN, "Dark Grey", self.rect.center, each.rect.center, 3)

    def remove_nearby(self):
        # check through nearby list if dino is still nearby other remove
        for nearby in self.nearby_dino:
            distance = nearby.rect.center - self.pos

            # makes negative positive
            if distance.x < 0:
                distance.x *= -1
            if distance.y < 0:
                distance.y *= -1

            if distance.x > 100 and distance.y > 100:
                # print(f'removed {nearby.name} from nearby list from {self.name}')
                self.nearby_dino.remove(nearby)
        #     print(f'list from: {self}, with nearby: {nearby.name}')
        # print(len(self.nearby_dino))

    def update(self):
        if self.health <= 0 or self.thirst <= 0 or self.hunger <= 0:
            self.is_alive = False

        self.state_check()
        self.state_move()

        self.add_nearby(dino_list, self.nearby_dino, 100)
        self.draw_nearby()
        self.remove_nearby()

        # #check nearby and add to list
        # try:
        #     for each in check_nearby(self, 100, dino_list):
        #         self.nearby_dino.append(each)
        #
        #     for each in check_nearby(self, 100, item_list):
        #         self.nearby_dino.append(each)
        #
        #     print(f'type: {self.name}, nearby: {len(self.nearby_dino)}')
        # except TypeError:
        #     ...
        #     # Not sure why this happens i think it has to do with the fact there is nothing else to append or maybe its trying to append twice?

        self.draw()

#region --- subclasses ---
class Triceratops(Dino):
    def __init__(self):
        super().__init__("Triceratops", triceratops_img, 5, 50, 60, 10, random.randint(10, 100), random.randint(10, 100), random.randint(10, 100))
        self.type_manager.set_state(self.type_manager.herbivore)


class Trex(Dino):
    def __init__(self):
        super().__init__("Trex", trex_img, 10, 35, 50, 25, random.randint(10, 100), random.randint(10, 100), random.randint(10, 100))
        self.type_manager.set_state(self.type_manager.carnivore)
#endregion

#region -- creating instances --
for _ in range(10):
    dino_list.append(Triceratops())

for _ in range(10):
    dino_list.append(Trex())
#endregion

