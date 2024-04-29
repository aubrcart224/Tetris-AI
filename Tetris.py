import random  
import cv2 
import numpy as np 
from PIL import Image 
from time import sleep


# Tetris game class 

class Tetris:

    '''Tetris game class'''

# Board 

MAP_EMPTY = 0
MAP_BLOCK = 1
MAP_PLAYER = 2
BOARD_WIDTH = 10
BOARD_HEIGHT = 20 

TETRIMINOS = {
    0: { 'shape': [[1, 1, 1, 1]], 'color': (255, 128, 0) }, # I
    1: { 'shape': [[1, 1, 1], [0, 1, 0]], 'color': (0, 0, 255) }, # T
    2: { 'shape': [[1, 1, 1], [1, 0, 0]], 'color': (255, 0, 0) }, # L
    3: { 'shape': [[1, 1, 1], [0, 0, 1]], 'color': (0, 255, 0) }, # J
    4: { 'shape': [[1, 1], [1, 1]], 'color': (255, 255, 0) }, # O
    5: { 'shape': [[0, 1, 1], [1, 1, 0]], 'color': (255, 0, 255) }, # Z
    6: { 'shape': [[1, 1, 0], [0, 1, 1]], 'color': (0, 255, 255) }, # S
}

COLORS = {
    0: (0, 0, 0),
    1: (255, 255, 255),
    2: (255, 255, 255),
}

def __init__(self):
    self.board = []
    self.score = 0
    self.reset()

def reset(self):
    '''Reset board and game return the current state'''
    self.board = [[0] * Tetris.BOARD_WIDTH for _ in range(Tetris.BOARD_HEIGHT)]
    self.game_over = False
    self.bag = list(range(len(Tetris.TETRIMINOS)))
    random.shuffle(self.bag)
    self.next_peice = self.pop()
    self._new_round = 0 
    self.score = 0

    return self._get_board_props(self.board)


def _get_rotated_peice(self):
    '''Return the current peice rotated'''
    return Tetris.TETROMINOS[self.current_piece][self.current_rotation]


def _get_complete_board(self):
    '''Return the complete board including the current peice'''
    peice = self._get_rotated_peice()
    peice = [np.add( x, self /current_pos) for x in peice]
    board = [x[:] for x in self.board]
    for x,y in peice:
        board[y][x] = Tetris.MAP_PLAYER 
    return board  

def _get_game_score(self):
    '''Return the current game score'''
    return self.score


def _new_round(self):
    '''Start a new round'''
# gen new bag 
    if len(self.bag) == 0:
        self.bag = list(range(len(Tetris.TETRIMINOS)))
        random.shuffle(self.bag)

    self.current_piece = self.next_peice
    self.next_peice = self.pop()
    self.current_pos = [3,0]
    self.current_rotation = 0

    if self._collision(self._get_rotated_peice(), self.current_pos):
        self.game_over = True
    
def _collision(self, peice, pos):
    '''Return True if the peice at pos collides with the board'''
    for x, y in peice:
        x += pos[0]
        y += pos[1]
        if x < 0 or x >= Tetris.BOARD_WIDTH or y >= Tetris.BOARD_HEIGHT: 
            return True
        if y >= 0 and self.board[y][x] == Tetris.MAP_BLOCK:
            return True
    return False

def _rotate(self, angle): 
    '''rotate peice'''
    r = self.current_rotation + angle

    if r == 360: 
        r = 0
    if r < 0:
        r += 360
    elif r > 360:
        r -= 360
    
    self.current_rotation = r

def _add_piece_to_board(self, piece, pos): 
    '''Add the current peice to the board'''

    board = [x[:] for x in self.board]
    for x,y in piece: 
        board[y + pos[1]][x + pos[0]] = Tetris.MAP_BLOCK
    return board


def _clear_lines(self, board):
    '''Clear completed lines from the board'''

    #check if lines can be cleared.
    lines= [i for i, row in enumerate(board) if sum(row) == Tetris.BOARD_WIDTH]
    if lines:
        board = [row for i, row in enumerate(board) if i not in lines]
        # Add new lines at the top
        for _ in lines:
            board.insert(0, [0 for _ in range(Tetris.BOARD_WIDTH)])
        self.score += len(lines)
    return board


def _number_of_holes(self, board):
    '''Return the number of holes in the board'''
    holes = 0
    for col in zip(*board):
        i = 0
        while i < Tetris.BOARD_HEIGHT and col[i] != Tetris.MAP_BLOCK:
            i += 1
        holes += len([x for x in col[i+1:] if x == Tetris.MAP_EMPTY])

    return holes

def _bumpiness(self, board):
    '''Return the bumpiness of the board'''

    sum_height = 0
    max_height = 0
    min_height = Tetris.BOARD_HEIGHT

    for col in zip(*board):
        i = 0 
        while i < Tetris.BOARD_HEIGHT and col[i] != Tetris.MAP_EMPTY:
            i += 1
        height = Tetris.BOARD_HEIGHT - i
        sum_height += height
        if height > max_height:
            max_height = height
        elif height < min_height:
            min_height = height 
        
    return sum_height, max_height - min_height



    
        








