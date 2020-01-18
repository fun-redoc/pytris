# globals
TITLE = "Py-Tris"
SCORE_LABEL = "Score: "
LABEL_FONT = "comicsans"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GAUSS_GRID_SUM = (GRID_WIDTH-1) * GRID_WIDTH / 2
GRID_HEIGHT = 20
INITIAL_FALL_SPEED = 0.25
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_COLOR = (127, 127, 127)
SHAPE_START_X, SHAPE_START_Y = 5, 0
NEXT_SHAPE_START_X, NEXT_SHAPE_START_Y = GRID_WIDTH + 3, 5
SHAPE_OFFSET_X, SHAPE_OFFSET_Y = -2, -4
NOT_OCCUPIED = -99
STATE_PLAYING = 'playing'
STATE_FALLING = 'falling'
STATE_GAME_OVER = 'game over'
game_field_width = GRID_WIDTH * BLOCK_SIZE
game_field_height = GRID_HEIGHT * BLOCK_SIZE

top_left_x = (SCREEN_WIDTH - game_field_width) // 2
top_left_y = SCREEN_HEIGHT - game_field_height

# shape templates incl. rotations
S = [['.....',
      '......',
      '..XX..',
      '.XX...',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '...X.',
      '.....']]

Z = [['.....',
      '.....',
      '.XX..',
      '..XX.',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '.X...',
      '.....']]

I = [['..X..',
      '..X..',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      'XXXX.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.XX..',
      '.XX..',
      '.....']]

J = [['.....',
      '.X...',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..XX.',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '...X.',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '.XX..',
      '.....']]

L = [['.....',
      '...X.',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '..XX.',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '.X...',
      '.....'],
     ['.....',
      '.XX..',
      '..X..',
      '..X..',
      '.....']]

T = [['.....',
      '..X..',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 128, 0), (0, 0, 255), (128, 0, 128)]
