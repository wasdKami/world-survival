import pygame

def check_nearby(self, fov_range, check_list):
        from main import SCREEN
        from Dino import Trex, Triceratops
        from Item import Water, Meat, Tree, Grass, Rock

        nearby_list = []
        line_width = 3

        for other in check_list:
            distance = other.rect.center - self.pos

            #makes negative positive
            if distance.x < 0:
                distance.x *= -1
            if distance.y < 0:
                distance.y *= -1

            if distance.x < fov_range and distance.y < fov_range:
                nearby_list.append(other)

                if isinstance(other, Trex):
                    pygame.draw.line(SCREEN, "Orange", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Triceratops):
                    pygame.draw.line(SCREEN, "Yellow", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Water):
                    pygame.draw.line(SCREEN, "Blue", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Meat):
                    pygame.draw.line(SCREEN, "Dark Red", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Grass):
                    pygame.draw.line(SCREEN, "Green", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Tree):
                    pygame.draw.line(SCREEN, "Dark Green", self.rect.center, other.rect.center, line_width)

                if isinstance(other, Rock):
                    pygame.draw.line(SCREEN, "Grey", self.rect.center, other.rect.center, line_width)

                for nearby in nearby_list:
                    if distance.x > fov_range or distance.y > fov_range:
                        pygame.draw.line(SCREEN, "Grey", self.rect.center, nearby.rect.center, line_width)

                return nearby_list