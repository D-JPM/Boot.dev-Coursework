import pygame
from constants import *
from player import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0


    # Drawing GUI
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    black = (0, 0 , 0) # Solid black colour
    screen.fill(black) # Fill screen with colour black

        # Instantiate Player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
        # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game state update
        dt = clock.tick(60) / 1000.0
        
        screen.fill("black")          # clear
        # test circle at exact center
        #pygame.draw.circle(screen, "yellow", (640, 360), PLAYER_RADIUS, 1)
        player.draw(screen)           # render player
        # Display updates
        pygame.display.flip()         # present

        
if __name__ == "__main__":
    main()
