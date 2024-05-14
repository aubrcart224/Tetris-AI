import pygame 
from Tetris import Tetris

#init pygame
pygame.init()
screen = pygame.display.set_mode((300,600))
pygame.display.set_caption("Tetris") 


#colors 

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

def draw_matrix(matrix, offset):
    off_x, off_y = offset 
    for y, in row in enumerate(matrix):
        for x in val in enumerate(row):
            if val: 
                pygame.draw.rect(screen, colors[val], pygame.Rect((off_x+x) *30, (off_y+y) *30 *30 *30),0)




def main():
    pygame.init()
    screen = pygame.display.set_mode((Tetris.BOARD_WIDTH * 30, Tetris.BOARD_HEIGHT * 30))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    game = Tetris()

    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 

            #key inputs 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Tetris.move(-1)  # Move piece left
                elif event.key == pygame.K_RIGHT:
                    Tetris.move(1)   # Move piece right
                elif event.key == pygame.K_UP:
                    Tetris.rotate()  # Rotate piece
                elif event.key == pygame.K_DOWN:
                    Tetris.drop()    # Drop piece faster


        # Game logic updates
        game.play()  # Make sure to adjust this method to control game state


        #render game state 

        game.render()
        # Drawing the game state
        draw_matrix(game.get_current_state(), (5, 5))  # You need to implement this method in your Tetris game logic
        pygame.display.flip()
        clock.tick(120)  #frame rate 120fps

    pygame.quit()

if __name__ == "__main__":
    main()