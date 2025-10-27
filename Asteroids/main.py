import pygame
from constants import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame
    pygame.init()

    # Drawing GUI
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    black = (0, 0 , 0) # Solid black colour
    screen.fill(black) # Fill screen with colour black

    # Game Loop
    running = True
    while running:


        # Display updates
        pygame.display.flip()


if __name__ == "__main__":
    main()
