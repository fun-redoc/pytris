from definitions import *
from logic import shape_to_grid
import pygame


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


def draw_game(win, state):  # ,  occupied_positions, current_shape, next_shape):
    win.fill(BLACK)

    # draw TITLE label
    font = pygame.font.SysFont(LABEL_FONT, 60, bold=True, italic=False)
    label = font.render(TITLE, True, WHITE)
    win.blit(label, (top_left_x + GRID_WIDTH / 2 - (label.get_width() / 2), 2 * BLOCK_SIZE - (label.get_height() / 2)))

    # draw Score label
    font = pygame.font.SysFont(LABEL_FONT, 40, bold=True, italic=False)
    label = font.render(SCORE_LABEL + str(state.score), True, WHITE)
    win.blit(label, (
    top_left_x + GRID_WIDTH * BLOCK_SIZE - (label.get_width() / 2), 2 * BLOCK_SIZE - (label.get_height() / 2)))

    draw_shapes(win, state.occupied_positions, state.current_shape)
    draw_next_shape(win, state.next_shape)
    draw_grid(win)

    pygame.display.update()


def draw_game_over(win, state):
    win.fill(BLACK)

    # draw TITLE label
    font = pygame.font.SysFont(LABEL_FONT, 60, bold=True, italic=False)
    label = font.render(TITLE, True, WHITE)
    win.blit(label, (top_left_x + GRID_WIDTH / 2 - (label.get_width() / 2), 2 * BLOCK_SIZE - (label.get_height() / 2)))

    # draw Score label
    font = pygame.font.SysFont(LABEL_FONT, 40, bold=True, italic=False)
    label = font.render(SCORE_LABEL + str(state.score), True, WHITE)
    win.blit(label, (
    top_left_x + GRID_WIDTH * BLOCK_SIZE - (label.get_width() / 2), 2 * BLOCK_SIZE - (label.get_height() / 2)))

    # draw Score label
    font = pygame.font.SysFont(LABEL_FONT, 60, bold=True, italic=False)
    label = font.render("Any Key to start a new Game", True, GREEN)
    win.blit(label, (SCREEN_WIDTH/2 - (label.get_width() / 2), SCREEN_HEIGHT/2 - (label.get_height() / 2)))
    pygame.display.update()
