#import copy

# from definitions import *
# from Shape import *
from GameState import *
from logic import *
from drawing import *


def main(win):
    s = Shape(0, GRID_HEIGHT, I)
    s.rotation = 1
    testpos = {(0, GRID_HEIGHT-2): s, (0, GRID_HEIGHT-4):s
              ,(2, GRID_HEIGHT-2): s, (2, GRID_HEIGHT-5):s
              }
    game_state = GameState(occupied_positions={}
                           , running=True
                           , current_shape=new_shape()
                           , next_shape=new_shape()
                           , fall_time=0
                           , fall_speed=INITIAL_FALL_SPEED
                           )
    state_handler = PlayingState()

    clock = pygame.time.Clock()

    while game_state.running:
        game_state.fall_time += clock.get_rawtime()
        clock.tick()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            (state_handler, game_state) = state_handler.handle_event(game_state, event)

        (state_handler, game_state) = state_handler.update(game_state)

        # draw
        draw_game(win, game_state.occupied_positions, game_state.current_shape, game_state.next_shape)

    pygame.display.quit()


if __name__ == '__main__':
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.font.init()
    main(surface)
