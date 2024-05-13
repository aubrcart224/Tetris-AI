import pygame  
from Tetris import Tetris

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))  # Set the screen size for Tetris
    clock = pygame.time.Clock()
    game = Tetris()

    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    game.play(-1, 0)
                elif event.key == pygame.K_RIGHT: 
                    game.play(1, 0)
                elif event.key == pygame.K_UP: 
                    game.play(0, 90)
                elif event.key == pygame.K_DOWN: 
                    game.play(0, 0, True)

        game.render()
        pygame.display.flip()
        clock.tick(120)  # Run the game at 10 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()