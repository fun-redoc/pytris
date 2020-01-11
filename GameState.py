from typing import ForwardRef

import pygame
from dataclasses import dataclass
from typing import *
import copy

from Shape import *
from logic import *


@dataclass()
class GameState(object):
    occupied_positions: Dict[Tuple[int, int], Shape]
    need_new_shape: bool
    running: bool
    current_shape: Shape
    next_shape: Shape
    falling: bool
    fall_time: int
    fall_speed: float


class StateProtocol(Protocol):
    @no_type_check
    def handle_event(self, state: GameState, event: int) -> Tuple[ForwardRef("StateProtocol"), GameState]:
        raise NotImplementedError

    @no_type_check
    def update(self, state: GameState) -> Tuple[ForwardRef("StateProtocol"), GameState]:
        raise NotImplementedError


class PlayingState(StateProtocol):
    def handle_event(self, state: GameState, event: Any) -> Tuple[StateProtocol, GameState]:
        """
        :param state: will be mutated
        :param event:
        :return: Tuple new state handler, mutated state
        """
        if event.type == pygame.KEYDOWN:
            # quit
            if event.key == pygame.K_ESCAPE:
                game_state.running = False
                # mutating state
            if event.key == pygame.K_SPACE:
                state.falling = True

            # stearing the shape
            if not state.falling:
                state.current_shape_copy = copy.copy(state.current_shape)
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
        # state

        # accelerate when falling
        if state.falling:
            state.fall_speed *= 0.9

        # move current shape
        if state.fall_time / 1000 > state.fall_speed:
            state.fall_time = 0
            state.current_shape.y += 1
            if not space_valid_for_shape(state.current_shape, state.occupied_positions) and not is_spawn_pos(
                    (state.current_shape.x, state.current_shape.y)):
                state.current_shape.y -= 1
                state.need_new_shape = True

        # update grid
        shape_coord = shape_to_grid(state.current_shape)

        if state.need_new_shape:
            for coord in shape_coord:
                state.occupied_positions[copy.copy(coord)] = state.current_shape
            state.current_shape = state.next_shape
            state.next_shape = new_shape()
            state.need_new_shape = False
            state.falling = False
            state.fall_speed = INITIAL_FALL_SPEED

        if check_lost(state.occupied_positions):
            state.running = False

        return self, state
