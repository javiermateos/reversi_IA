from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import Heuristic
from javier_adrian_heuristic import (evaluation_function,
                                     MinimaxAlphaBetaStrategy)
from strategy import ManualStrategy
from reversi import Reversi

heuristic = Heuristic(
    name='Teo va en avion',
    evaluation_function=evaluation_function,
)

player_1 = Player(
    name='player_1',
    strategy=ManualStrategy(verbose=0),
)

player_2 = Player(
    name='player_2',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)

player_a, player_b = player_1, player_2

initial_player = player_a

initial_board = None

game = Reversi(
    player1=player_a,
    player2=player_b,
    height=8,
    width=8,
)

game_state = TwoPlayerGameState(
    game=game,
    board=initial_board,
    initial_player=initial_player,
)

match = TwoPlayerMatch(
    game_state,
    max_sec_per_move=300,
    gui=True,
)

scores = match.play_match()
input('Press any key to finish.')
