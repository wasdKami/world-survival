import pygame

#You need to initialize the module. I see it as turning on the machine.
pygame.init()

from Dino import triceratops

#this is the title and image that you see at the top of the window
pygame.display.set_caption("ecosystem simulation")
# pygame.display.set_icon(pygame.image.load("icon.png"))

#I am creating a variable so i can use this variable instead of needing to write out the entire function
DISPLAY_INFO = pygame.display.Info()
#I am defining the window and giving it a size based on the screen size
SCREEN = pygame.display.set_mode((DISPLAY_INFO.current_w, DISPLAY_INFO.current_h))
#I am defining a clock so i can set a framerate so the tick rate is the same on every pc
CLOCK = pygame.time.Clock()
#Creating a bool to check if my game is running otherwise close the game
RUNNING = True

#my main loop that keeps looking, ending this loop will close the game
while RUNNING:
    #this checks all "events" for example in this instance it checks if the game is getting closed using the cross button then end the loop by setting bool to false. Another way it can be used is checking if the player is pressing any buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    #every frame i am drawing the background with a solid color to "reset" the display
    SCREEN.fill("Dark Green")

    #Here you can write your game AFTER the fill so you draw on top of the fresh screen and BEFORE the flip which draws the display to the screen
    triceratops.update()

    pygame.display.flip()

    #Creating a clock that makes sure the program wont run more then the framerate which i capped on 60
    CLOCK.tick(60)

#Uninitializing pygame
pygame.quit()
