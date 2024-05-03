import cv2 
from Tetris import Tetris

def main():
    game = Tetris()
    while not game.game_over:
        game.render()
        key = cv2.waitKey(100)  & 0xFF # 100 ms delay

        #awsd
        if key == ord('a'):  #move left
            game.play(-1, 0)
        elif key == ord('d'): #move right
            game.play(1, 0)
        elif key == ord('w'): #rotate
            game.play(0, 90)
        elif key == ord('q'): #drop faster
            game.play(0, 0, True)

        #arrow keys migth not work on all systems
        if key == 2424832:  #move left
            game.play(-1, 0)
        elif key == 2555904: #move right
            game.play(1, 0)
        elif key == 2490368: #rotate
            game.play(0, 90)
        elif key == 2621440: #drop faster
            game.play(0, 0, True)
            
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
