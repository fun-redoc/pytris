from definitions import *
# from Shape import *
from GameState import *
from logic import *
from drawing import *

translation_tab = { pygame.K_SPACE: EVENT_FALL
                  , pygame.K_LEFT: EVENT_LEFT
                  , pygame.K_RIGHT: EVENT_RIGHT
                  , pygame.K_UP: EVENT_ROT_LEFT
                  , pygame.K_DOWN: EVENT_ROT_RIGHT
                  , pygame.K_ESCAPE: EVENT_QUIT
                  }


def translate_key_to_event(key: int) -> EventType:
    try:
        return translation_tab[key]
    except KeyError:
        return EVENT_NONE


def pygame_main(game_state):
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.font.init()

    # set framewor dependent drawing functions
    game_state.state_handlers[STATE_GAME_OVER].set_draw(lambda state: draw_game_over(win, state))
    game_state.state_handlers[STATE_PLAYING].set_draw(lambda state: draw_game(win, state))
    game_state.state_handlers[STATE_FALLING].set_draw(lambda state: draw_game(win, state))

    clock = pygame.time.Clock()

    while game_state.running:
        game_state.fall_time += clock.get_rawtime()
        clock.tick()

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state.running = False
            else:
                if event.type == pygame.KEYDOWN:
                    game_state = game_state.current_handler.handle_event(game_state, translate_key_to_event(event.key))

        game_state = game_state.current_handler.update(game_state)

        # draw
        game_state.current_handler.draw(game_state)
#        draw_game(win, game_state) #.occupied_positions, game_state.current_shape, game_state.next_shape)

    pygame.display.quit()


if __name__ == '__main__':
    state_handlers = {   STATE_PLAYING:   PlayingState()
                        ,STATE_FALLING:   FallingState()
                        ,STATE_GAME_OVER: GameOverState()
                      }

    game_state = GameState( state_handlers=state_handlers
                           #, current_handler= state_handlers[STATE_GAME_OVER].enter(state_handlers[STATE_GAME_OVER])
                           , current_handler= state_handlers[STATE_GAME_OVER]
                           , occupied_positions={}
                           , running=True
                           , current_shape=new_shape()
                           , next_shape=new_shape()
                           , fall_time=0
                           , fall_speed=INITIAL_FALL_SPEED
                           )
    game_state = game_state.current_handler.enter(game_state)
    pygame_main(game_state)
