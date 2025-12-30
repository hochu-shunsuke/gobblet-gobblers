"""
Random Player - ランダムに手を選ぶAI
"""

import random
import sys
sys.path.append('..')
from game import GobbletGobblers, Move
from .base_player import BasePlayer


class RandomPlayer(BasePlayer):
    """ランダムに合法手を選ぶプレイヤー"""
    
    def __init__(self, seed: int = None):
        super().__init__(name="RandomPlayer")
        if seed is not None:
            random.seed(seed)
    
    def choose_move(self, game: GobbletGobblers) -> Move:
        """ランダムに手を選択"""
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            raise ValueError("No legal moves available")
        return random.choice(legal_moves)
