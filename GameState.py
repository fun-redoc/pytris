# from typing import ForwardRef

from copy import copy
from dataclasses import dataclass

import pygame

from logic import *


@dataclass()
class GameState(object):
    occupied_positions: Dict[Tuple[int, int], Shape]
    #    need_new_shape: bool
    running: bool
    current_shape: Shape
    next_shape: Shape
    fall_time: int
    fall_speed: float


def glue_current_shape(state: GameState) -> GameState:
    shape_coord = shape_to_grid(state.current_shape)
    for coord in shape_coord:
        state.occupied_positions[copy(coord)] = state.current_shape
    return state


def move_shape(state: GameState) -> Tuple[bool, GameState]:
    if state.fall_time / 1000 > state.fall_speed:
        state.fall_time = 0
        state.current_shape.y += 1
        if not space_valid_for_shape(state.current_shape, state.occupied_positions) and not is_spawn_pos(
                (state.current_shape.x, state.current_shape.y)):
            state.current_shape.y -= 1
            return False, state
    return True, state


class StateProtocol(Protocol):
    def enter(self, state: GameState) -> GameState:
        raise NotImplementedError

    def leave(self, state: GameState) -> GameState:
        raise NotImplementedError

    def handle_event(self, state: GameState, event: int) -> Tuple[ForwardRef("StateProtocol"), GameState]:
        raise NotImplementedError

    def update(self, state: GameState) -> Tuple[ForwardRef("StateProtocol"), GameState]:
        raise NotImplementedError


class GameOverState(StateProtocol):
    def leave(self, state: GameState) -> GameState:
        return state

    def enter(self, state: GameState) -> GameState:
        state.running = False
        return state

    def handle_event(self, state: GameState, event: Any) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutated
        :param event:
        :return: Tuple new state handler, mutated state
        """
        return self, state

    def update(self, state: GameState) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutates
        :return: Tuple new state handler, mutated state
        """
        return self, state


class PlayingState(StateProtocol):
    def leave(self, state: GameState) -> GameState:
        return state

    def enter(self, state: GameState) -> GameState:
        state.current_shape = state.next_shape
        state.next_shape = new_shape()
        # state.need_new_shape = False
        state.fall_speed = INITIAL_FALL_SPEED
        return state

    def handle_event(self, state: GameState, event: Any) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutated
        :param event:
        :return: Tuple new state handler, mutated state
        """
        # mutating state
        if event.type == pygame.KEYDOWN:
            # quit
            if event.key == pygame.K_ESCAPE:
                new_state_handler = GameOverState()
                return new_state_handler, new_state_handler.enter(self.leave(state))
            else:
                if event.key == pygame.K_SPACE:
                    new_state_handler = FallingState()
                    return new_state_handler, new_state_handler.enter(self.leave(state))
                else:
                    # stearing the shape
                    state.current_shape_copy = copy(state.current_shape)
                    if event.key == pygame.K_LEFT:
                        state.current_shape.x -= 1
                    if event.key == pygame.K_RIGHT:
                        state.current_shape.x += 1
                    if event.key == pygame.K_UP:
                        state.current_shape.rotation -= 1
                    if event.key == pygame.K_DOWN:
                        state.current_shape.rotation += 1
                    if not (space_valid_for_shape(state.current_shape, state.occupied_positions)):
                        state.current_shape = state.current_shape_copy

        return self, state

    def update(self, state: GameState) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutates
        :return: Tuple new state handler, mutated state
        """

        shape_move_successful, state = move_shape(state)

        if not shape_move_successful:
            state = glue_current_shape(state)
            if check_lost(state.occupied_positions):
                state.running = False
            else:
                state.current_shape = state.next_shape
                state.next_shape = new_shape()
                state.need_new_shape = False
                state.fall_speed = INITIAL_FALL_SPEED

        return self, state


class FallingState(StateProtocol):
    def enter(self, state: GameState) -> GameState:
        return state

    def leave(self, state: GameState) -> GameState:
        return state

    def handle_event(self, state: GameState, event: Any) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutated
        :param event:
        :return: Tuple new state handler, mutated state
        """
        return self, state

    def update(self, state: GameState) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutates
        :return: Tuple new state handler, mutated state
        """
        state.fall_speed *= 0.9

        shape_move_successful, state = move_shape(state)

        if not shape_move_successful:
            state = glue_current_shape(state)
            if check_lost(state.occupied_positions):
                state.running = False
            else:
                new_state_handler = PlayingState()
                state = new_state_handler.enter(self.leave(state))
                return new_state_handler, state

        return self, state