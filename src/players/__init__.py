"""Players module"""
from .base_player import BasePlayer
from .random_player import RandomPlayer
from .minimax_player import MinimaxPlayer

# NNPlayer is optional (requires torch)
try:
    from .nn_player import NNPlayer, GobbletNet
except ImportError:
    pass  # torch not installed
