import pygame
import random
import typing
import copy

# globals
TITLE = "Py-Tris"
LABEL_FONT = "comicsans"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
INITIAL_FALL_SPEED = 0.25
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_COLOR = (127, 127, 127)
SHAPE_START_X, SHAPE_START_Y = 5, 0
NEXT_SHAPE_START_X, NEXT_SHAPE_START_Y = GRID_WIDTH + 3, 5
SHAPE_OFFSET_X, SHAPE_OFFSET_Y = -2, -4
NOT_OCCUPIED = -99
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


class Shape(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.shapeIdx = shapes.index(shape)
        self.color = shape_colors[self.shapeIdx]
        self.rotation = 0

    def __copy__(self):
        cp = Shape(self.x, self.y, self.shape)
        cp.rotation = self.rotation
        cp.shapeIdx = self.shapeIdx
        return cp


def grid_pos(x, y):
    assert not to_grid_pos(x, y) is None
    return x + (y * GRID_WIDTH)


def to_grid_pos(x: int, y: int) -> typing.Optional[int]:
    if not 0 <= x < GRID_WIDTH:
        return None
    if not 0 <= y < GRID_HEIGHT:
        return None
    return x + (y * GRID_WIDTH)


def shape_to_grid(shape: Shape) -> typing.List[typing.Tuple[int, int]]:
    coords = []
    templ = shapes[shape.shapeIdx]
    templ_rotated = templ[shape.rotation % len(templ)]
    for (y, row) in enumerate(templ_rotated):
        for (x, cell) in enumerate(row):
            if cell == 'X':
                coords.append((shape.x + x + SHAPE_OFFSET_X, shape.y + y + SHAPE_OFFSET_Y))
    return coords


def is_spawn_pos(acoord: typing.Tuple[int, int]) -> bool:
    return acoord[1] < 0


def is_within_grid(x: int, y: int) -> bool:
    return 0 <= x < GRID_WIDTH and y < GRID_HEIGHT


def space_valid_for_shape(shape: Shape, occupied_positions: typing.Dict[typing.Tuple[int, int], Shape]) -> bool:
    shape_coords = shape_to_grid(shape)
    for (x, y) in shape_coords:
        if (x, y) in occupied_positions:
            return False
        if not is_within_grid(x, y):
            return False
    return True


def check_lost(positions: typing.Tuple[int, int]) -> bool:
    """
    check if any position is above the screen
    """
    for (x, y) in positions:
        if 0 > y:
            return True
    return False


def new_shape():
    return Shape(SHAPE_START_X, SHAPE_START_Y, random.choice(shapes))

def draw_grid(win):
    for y in range(GRID_HEIGHT):
        # horizontal lines
        ylevel = top_left_y + y * BLOCK_SIZE
        pygame.draw.line(win, LINE_COLOR, (top_left_x, ylevel), (top_left_x + GRID_WIDTH * BLOCK_SIZE, ylevel))
    for x in range(GRID_WIDTH):
        # vertical lines
        xlevel = top_left_x + x * BLOCK_SIZE
        pygame.draw.line(win, LINE_COLOR, (xlevel, top_left_y), (xlevel, top_left_y + GRID_HEIGHT * BLOCK_SIZE))

    # draw red frame
    pygame.draw.rect(win, RED, (top_left_x, top_left_y, game_field_width, game_field_height), 4)


def draw_shapes(win, occupied_positions, current_shape):
    for ((x, y), shape) in occupied_positions.items():
        xcoord = top_left_x + x * BLOCK_SIZE
        ycoord = top_left_y + y * BLOCK_SIZE
        pygame.draw.rect(win, shape.color, (xcoord, ycoord, BLOCK_SIZE, BLOCK_SIZE), 0)

    current_shape_positions = shape_to_grid(current_shape)
    for (x, y) in current_shape_positions:
        xcoord = top_left_x + x * BLOCK_SIZE
        ycoord = top_left_y + y * BLOCK_SIZE
        pygame.draw.rect(win, current_shape.color, (xcoord, ycoord, BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_next_shape(win, shape):
    coords = []
    templ = shapes[shape.shapeIdx][0]
    for (y, row) in enumerate(templ):
        for (x, cell) in enumerate(row):
            if cell == 'X':
                coords.append((NEXT_SHAPE_START_X + x + SHAPE_OFFSET_X, NEXT_SHAPE_START_Y + y + SHAPE_OFFSET_Y))
    for (x, y) in coords:
        xcoord = top_left_x + x * BLOCK_SIZE
        ycoord = top_left_y + y * BLOCK_SIZE
        pygame.draw.rect(win, shape.color, (xcoord, ycoord, BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_game(win, occupied_positions, current_shape, next_shape):
    win.fill(BLACK)

    # draw TITLE label
    font = pygame.font.SysFont(LABEL_FONT, 60, bold=True, italic=False)
    label = font.render(TITLE, True, WHITE)
    win.blit(label, (top_left_x + GRID_WIDTH / 2 - (label.get_width() / 2), BLOCK_SIZE))

    draw_shapes(win, occupied_positions, current_shape)
    draw_next_shape(win, next_shape)
    draw_grid(win)

    pygame.display.update()


def main(win):
    occupied_positions = {}
    need_new_shape = False
    running = True
    current_shape = new_shape()
    next_shape = new_shape()

    clock = pygame.time.Clock()
    falling = False
    fall_time = 0
    fall_speed = INITIAL_FALL_SPEED

    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        if falling:
            fall_speed *= 0.9

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1
            if not space_valid_for_shape(current_shape, occupied_positions) and not is_spawn_pos(
                    (current_shape.x, current_shape.y)):
                current_shape.y -= 1
                need_new_shape = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # quit
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    falling = True

                # stearing the shape
                if not falling:
                    current_shape_copy = copy.copy(current_shape)
                    if event.key == pygame.K_LEFT:
                        current_shape.x -= 1
                    if event.key == pygame.K_RIGHT:
                        current_shape.x += 1
                    if event.key == pygame.K_UP:
                        current_shape.rotation -= 1
                    if event.key == pygame.K_DOWN:
                        current_shape.rotation += 1
                    if not (space_valid_for_shape(current_shape, occupied_positions)):
                        current_shape = current_shape_copy

        # update grid
        shape_coord = shape_to_grid(current_shape)

        if need_new_shape:
            for coord in shape_coord:
                occupied_positions[copy.copy(coord)] = current_shape
            current_shape = next_shape
            next_shape = new_shape()
            need_new_shape = False
            falling = False
            fall_speed = INITIAL_FALL_SPEED

        draw_game(win, occupied_positions, current_shape, next_shape)

        if check_lost(occupied_positions):
            running = False

    pygame.display.quit()

if __name__ == '__main__':
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.font.init()
    main(surface)
