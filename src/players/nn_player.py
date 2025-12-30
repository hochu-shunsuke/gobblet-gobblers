"""
Neural Network Player - 学習済みモデルで手を選ぶAI
"""

import sys
import numpy as np
sys.path.append('..')

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from .base_player import BasePlayer
from game import GobbletGobblers, Move, PieceSize


class GobbletNet(nn.Module):
    """Gobblet Gobblers用のニューラルネットワーク"""
    
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(6, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 3 * 3, 128)
        self.fc2 = nn.Linear(128, 81)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class NNPlayer(BasePlayer):
    """ニューラルネットワークで手を選ぶプレイヤー"""
    
    def __init__(self, model_path: str = None, model: nn.Module = None):
        """
        Args:
            model_path: 学習済みモデルのパス（.ptファイル）
            model: 直接モデルを渡す場合
        """
        super().__init__(name="NNPlayer")
        
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch is required for NNPlayer. Install with: pip install torch")
        
        if model is not None:
            self.model = model
        elif model_path is not None:
            self.model = GobbletNet()
            self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        else:
            raise ValueError("Either model_path or model must be provided")
        
        self.model.eval()
    
    def _board_to_tensor(self, game: GobbletGobblers) -> np.ndarray:
        """盤面をテンソルに変換"""
        state = game.get_full_state()
        tensor = np.zeros((6, 3, 3), dtype=np.float32)
        
        for row in range(3):
            for col in range(3):
                stack = state['board'][row][col]
                if stack:
                    piece_str = stack[-1]
                    player = 0 if piece_str[0] == '1' else 1
                    size = {'S': 0, 'M': 1, 'L': 2}[piece_str[1]]
                    channel = player * 3 + size
                    tensor[channel, row, col] = 1.0
        
        return tensor
    
    def _move_to_index(self, move: Move) -> int:
        """手をインデックスに変換"""
        size_idx = {PieceSize.SMALL: 0, PieceSize.MEDIUM: 1, PieceSize.LARGE: 2}[move.piece_size]
        to_idx = move.to_pos[0] * 3 + move.to_pos[1]
        
        if move.from_pos is None:
            return size_idx * 9 + to_idx  # 0-26
        else:
            return 27 + size_idx * 18 + to_idx  # 27-80
    
    def choose_move(self, game: GobbletGobblers) -> Move:
        """NNの出力に基づいて手を選択"""
        # 盤面をテンソルに変換
        tensor = self._board_to_tensor(game)
        
        # 推論
        with torch.no_grad():
            x = torch.FloatTensor(tensor).unsqueeze(0)
            logits = self.model(x)[0]
        
        # 合法手を取得
        legal_moves = game.get_legal_moves()
        
        # 合法手の中で最もスコアが高いものを選択
        best_move = None
        best_score = float('-inf')
        
        for move in legal_moves:
            idx = min(self._move_to_index(move), 80)
            score = logits[idx].item()
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
