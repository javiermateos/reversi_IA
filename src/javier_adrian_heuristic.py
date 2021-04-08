from game import TwoPlayerGameState
from strategy import Strategy
from heuristic import Heuristic

import numpy as np


class MinimaxAlphaBetaStrategy(Strategy):
    """Minimax alpha-beta strategy."""
    def __init__(
            self,
            heuristic: Heuristic,
            max_depth_minimax: int,
            verbose: int = 0,
    ) -> None:
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
            self,
            state: TwoPlayerGameState,
            gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next state in the game."""

        successors = self.generate_successors(state)

        minimax_value = -np.inf

        for successor in successors:
            if self.verbose > 1:
                print('{}: {}'.format(state.board, minimax_value))

            successor_minimax_value = self._min_value(successor,
                                                      self.max_depth_minimax)
            if (successor_minimax_value > minimax_value):
                minimax_value = successor_minimax_value
                next_state = successor

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Minimax value = {:.2g}'.format(minimax_value))

        return next_state

    def _cutoff_test(self, state, depth) -> bool:
        """Determine when to cut off search"""
        if state.end_of_game or depth == 0:
            return True

        return False

    def _min_value(
            self,
            state: TwoPlayerGameState,
            depth: int,
            alfa: int = -np.inf,
            beta: int = np.inf,
    ) -> float:
        """Min step of the minimax algorithm."""
        if self._cutoff_test(state, depth):
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._max_value(
                    successor, depth - 1, alfa, beta)

                minimax_value = min(minimax_value, successor_minimax_value)

                if minimax_value <= alfa:
                    break

                beta = min(beta, minimax_value)

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value

    def _max_value(self, state: TwoPlayerGameState, depth: int, alfa: int,
                   beta: int) -> float:
        """Max step of the minimax algorithm."""
        if self._cutoff_test(state, depth):
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = -np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._min_value(
                    successor, depth - 1, alfa, beta)

                minimax_value = max(minimax_value, successor_minimax_value)

                if minimax_value >= beta:
                    break

                alfa = max(alfa, minimax_value)

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value


def evaluation_function(state: TwoPlayerGameState) -> float:
    scores = state.scores

    score_difference = scores[0] - scores[1]
    score_sum = scores[0] + scores[1]

    if state.end_of_game:
        if state.is_player_max(state.player1):
            state_value = score_difference
        elif state.is_player_max(state.player2):
            state_value = -score_difference
        else:
            raise ValueError('Player MAX not defined')
    else:
        # Calculamos el momento de la partida
        stage = ((state.game.height * state.game.width) - 4) / 60
        stab = stability(state)
        mob = mobility(state)
        cor = corner(state)
        score = 100 * score_difference / score_sum
        # Early game
        if score_sum <= (stage * 20):
            num = (45 * stab + 30 * mob + 5 * cor + 20 * score)
            if state.is_player_max(state.player1):
                state_value = num
            elif state.is_player_max(state.player2):
                state_value = -num
        # Late game
        elif score_sum >= (stage * 54):
            num = (20 * stab + 5 * mob + 30 * cor + 45 * score)
            if state.is_player_max(state.player1):
                state_value = num
            elif state.is_player_max(state.player2):
                state_value = -num
        # Mid game
        else:
            num = (30 * stab + 20 * mob + 45 * cor + 5 * score)
            if state.is_player_max(state.player1):
                state_value = num
            elif state.is_player_max(state.player2):
                state_value = -num

    return state_value


def corner(state: TwoPlayerGameState) -> float:
    state_value = 0
    corners_points = [(1, 1), (1, state.game.height), (state.game.width, 1),
                      (state.game.width, state.game.height)]

    corners = [state.board.get(x) for x in corners_points]
    my_corners = corners.count(state.player1.label)
    opponent_corners = corners.count(state.player2.label)

    if my_corners + opponent_corners != 0:
        state_value = 100 * (my_corners - opponent_corners) / (
            my_corners + opponent_corners)

    return state_value


def mobility(state: TwoPlayerGameState) -> float:
    state_value = 0

    my_mobility = len(
        state.game._get_valid_moves(state.board, state.player1.label))
    opponent_mobility = len(
        state.game._get_valid_moves(state.board, state.player2.label))

    if my_mobility + opponent_mobility != 0:
        state_value = 100 * (my_mobility - opponent_mobility) / (
            my_mobility + opponent_mobility)

    return state_value


def stability(state: TwoPlayerGameState) -> float:
    board = state.board
    state_value = 0

    player_stabilities = {state.player1.label: 0, state.player2.label: 0}

    row_direction = [1, -1, 0, 1]
    col_direction = [0, 1, 1, 1]
    row_inc = 0
    col_inc = 0

    # Miramos cada ficha de los jugadores recorriendo todo el mapa
    for row in range(state.game.height):
        for col in range(state.game.width):
            coin_stable = 2
            occupied_by = board.get((row, col))

            # Si esta vacia continuamos
            if occupied_by is None:
                continue
            # Miramos todas las direcciones
            for i in range(4):
                temp_row = row + row_inc
                temp_col = col + col_inc

                first_coin_encountered = occupied_by
                second_coin_encountered = occupied_by

                row_inc = row_direction[i]
                col_inc = col_direction[i]

                while (temp_row >= 1 and temp_row <= state.game.height
                       and temp_col >= 1 and temp_col <= state.game.width):
                    if board.get((temp_row, temp_col)) != occupied_by:
                        first_coin_encountered = board.get(temp_row, temp_col)
                        break
                    temp_row += row_inc
                    temp_col += col_inc

                # Estable
                if first_coin_encountered == occupied_by:
                    continue

                # Cambios a la direccion opuesta
                row_inc = -row_inc
                col_inc = -col_inc

                temp_row = row + row_inc
                temp_col = col + col_inc

                while (temp_row >= 1 and temp_row <= state.game.height
                       and temp_col >= 1 and temp_col <= state.game.width):
                    if board.get((temp_row, temp_col)) != occupied_by:
                        second_coin_encountered = board.get(temp_row, temp_col)
                        break
                    temp_row += row_inc
                    temp_col += col_inc

                # Estable
                if second_coin_encountered == occupied_by:
                    continue

                # Semi-Estable
                if first_coin_encountered == second_coin_encountered:
                    if coin_stable > 1:
                        coin_stable = 1
                # Inestable
                else:
                    coin_stable = 0
                    break

            player_stabilities[occupied_by] += coin_stable

    my_stability = player_stabilities[state.player1.label]
    opponent_stability = player_stabilities[state.player2.label]

    if my_stability + opponent_stability != 0:
        state_value = 100 * (my_stability - opponent_stability) / (
            my_stability + opponent_stability)

    return state_value
