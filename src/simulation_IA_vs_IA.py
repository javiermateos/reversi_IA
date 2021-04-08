from game import Player, TwoPlayerGameState, TwoPlayerMatch
from heuristic import Heuristic
from javier_adrian_heuristic import (evaluation_function,
                                     MinimaxAlphaBetaStrategy)
from reversi import Reversi

# TODO: Import your heuristic here
# from your_file import function_name

heuristic = Heuristic(
    name='Teo va en avion',
    evaluation_function=evaluation_function,
)

# TODO: After import you can instantiate a heuristic class
# heuristic = Heuristic(
#     name='your name',
#     evaluation_function=function_name,
# )

player_1 = Player(
    name='player_1',
    strategy=MinimaxAlphaBetaStrategy(
        heuristic=heuristic,
        max_depth_minimax=4,
        verbose=0,
    ),
)

# TODO: Create your player
# player_2 = Player(
#     name='player_2',
#     strategy=MinimaxAlphaBetaStrategy(
#         heuristic=heuristic_name,
#         max_depth_minimax=4,
#         verbose=0,
#     ),
# )

player_a, player_b = player_1  # TODO: Insert the name of the player here

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
