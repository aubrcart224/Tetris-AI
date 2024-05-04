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
        self.next_peice = self.bag.pop()
        self._new_round = 0 
        self.score = 0

        return self._get_board_props(self.board)

    def _get_rotated_peice(self):
        '''Return the current peice rotated'''
        return Tetris.TETRIMINOS[self.current_piece][self.current_rotation]

    def _get_complete_board(self):
        '''Return the complete board including the current peice'''
        peice = self._get_rotated_peice()
        peice = [np.add( x, self.current_pos) for x in peice]
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

    def _height(self, board):
        '''Return the height of the board'''

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
    
        return sum_height, max_height, min_height
        
    def _get_board_props(self, board):
        '''Return the board properties'''

        lines = self._clear_lines(board)
        board = self._clear_lines(board) 
        holes = self._number_of_holes(board)
        total_bunpiness, max_bumpiness = self._bumpiness(board)
        sum_height, max_height, min_height = self._height(board)
        return [lines, holes, total_bunpiness, max_bumpiness, sum_height, max_height, min_height]

    def get_next_states(self):
        '''Return all the possible next states'''
        states = {}
        piece_id = self.current_piece

        if piece_id == 6: 
            rotations = [0]
        elif piece_id == 0: 
            rotations = [0, 90]
        else:
            rotations = [0, 90, 180, 270]
    
        # All possible rotations 

        for rotation in rotations: 
            piece = Tetris.TETRIMINOS[piece_id][rotation]
            min_x = min([x for x, y in piece])
            max_x = max([x for x, y in piece])
        
        # For all possible positions
        for x in range(-min_x, Tetris.BOARD_WIDTH - max_x):
            pos = [x, 0]

            #drop the piece
            while not self._collision(piece, pos):
                pos[1] += 1
            pos[1] -= 1
            
            #valid move 
            if pos[1] >= 0:
                board = self._add_piece_to_board(piece, pos)
                states[(x, rotation)] = self._get_board_props(board)
                
                return states

    def get_state_size(self): 
        '''Size of the state''' 
        return 4 
 
    def play(self, x, rotation, render = False, render_delay = None): 
        '''Play a move'''

        self.current_pos = [x, 0]
        self.current_rotation = rotation 

        #drop the piece 
        while not self._check_collision(self._get_rotated_piece(), self.current_pos):
            if render:
                self.render()
                if render_delay:
                    sleep(render_delay)
            self.current_pos[1] += 1
        self.current_pos[1] -= 1 

        # Update the board and calc score 
        self.board = self._add_piece_to_board(self._get_rotated_peice(), self.current_pos)
        lines_cleared, self.board = self._clear_lines(self.board)
        score = 1 + (lines_cleared ** 2) * Tetris.BOARD_WIDTH
        self.score += score

        #start new round 
        self._new_round()
        if self.game_over:
            score -= 2 
    
        return score, self.game_over

    def render(self):

            ''' render current board'''
            img = [Tetris.COLORS[p] for row in self._get_complete_board() for p in row]
            img = np.array(img).reshape(Tetris.BOARD_HEIGHT, Tetris.BOARD_WIDTH, 3).astype(np.uint8)
            img = img[..., ::-1] # Convert RRG to BGR (used by cv2)
            img = Image.fromarray(img, 'RGB')
            img = img.resize((Tetris.BOARD_WIDTH * 25, Tetris.BOARD_HEIGHT * 25), Image.NEAREST)
            img = np.array(img)
            cv2.putText(img, str(self.score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            cv2.imshow('image', np.array(img))
            cv2.waitKey(1)

