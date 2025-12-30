"""
Base Player - すべてのプレイヤーの基底クラス
"""

from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from game import GobbletGobblers, Move, Player


class BasePlayer(ABC):
    """プレイヤーの基底クラス"""
    
    def __init__(self, name: str = "BasePlayer"):
        self.name = name
    
    @abstractmethod
    def choose_move(self, game: GobbletGobblers) -> Move:
        """
        手を選択する
        
        Args:
            game: 現在のゲーム状態
            
        Returns:
            選択した手
        """
        pass
    
    def __repr__(self):
        return f"{self.name}"
