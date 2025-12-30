"""
Minimax Player (Optimized) - 高速化版
"""

import sys
from typing import Optional
from functools import lru_cache
sys.path.append('..')
from game import GobbletGobblers, Move, Player, GameResult, PieceSize
from .base_player import BasePlayer


class MinimaxPlayer(BasePlayer):
    """Minimaxアルゴリズムで最適手を選ぶプレイヤー（高速化版）"""
    
    def __init__(self, max_depth: int = 4):
        """
        Args:
            max_depth: 探索の最大深さ
        """
        super().__init__(name=f"MinimaxPlayer(d={max_depth})")
        self.max_depth = max_depth
        self.nodes_evaluated = 0
        self._cache = {}  # 盤面キャッシュ
    
    def choose_move(self, game: GobbletGobblers) -> Move:
        """最適な手を選択"""
        self.nodes_evaluated = 0
        self.my_player = game.current_player
        self._cache = {}  # キャッシュをリセット
        
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        legal_moves = game.get_legal_moves()
        
        # 手を評価順にソート（より良い枝刈りのため）
        legal_moves = self._order_moves(game, legal_moves)
        
        for move in legal_moves:
            game_copy = game.clone()
            game_copy.make_move(move)
            
            score = self._minimax(game_copy, self.max_depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            
            # 勝ちが見つかったら即座に返す
            if score > 900:
                break
        
        return best_move
    
    def _get_board_key(self, game: GobbletGobblers) -> str:
        """盤面のハッシュキーを生成"""
        key_parts = []
        for row in range(3):
            for col in range(3):
                top = game.board[row][col].top()
                key_parts.append(str(top) if top else ".")
        key_parts.append(str(game.current_player.value))
        return "".join(key_parts)
    
    def _minimax(self, game: GobbletGobblers, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        """Minimax with Alpha-Beta pruning"""
        self.nodes_evaluated += 1
        
        # 終端条件
        if game.is_game_over():
            return self._evaluate_terminal(game)
        
        if depth == 0:
            return self._evaluate_position(game)
        
        # キャッシュチェック
        board_key = self._get_board_key(game)
        cache_key = (board_key, depth, is_maximizing)
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        legal_moves = game.get_legal_moves()
        
        if not legal_moves:
            return 0
        
        # 手数が多い場合は上位のみ探索
        legal_moves = self._order_moves(game, legal_moves)
        if depth < self.max_depth - 1 and len(legal_moves) > 12:
            legal_moves = legal_moves[:12]
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                game_copy = game.clone()
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            self._cache[cache_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                game_copy = game.clone()
                game_copy.make_move(move)
                eval_score = self._minimax(game_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            self._cache[cache_key] = min_eval
            return min_eval
    
    def _evaluate_terminal(self, game: GobbletGobblers) -> float:
        """終端ノードの評価"""
        if game.result == GameResult.DRAW:
            return 0
        
        winner = game.get_winner()
        if winner == self.my_player:
            return 1000 - game.turn_count
        else:
            return -1000 + game.turn_count
    
    def _evaluate_position(self, game: GobbletGobblers) -> float:
        """盤面の評価関数"""
        score = 0
        
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        
        for line in lines:
            my_count = 0
            opp_count = 0
            empty_count = 0
            
            for r, c in line:
                top = game.board[r][c].top()
                if top is None:
                    empty_count += 1
                elif top.player == self.my_player:
                    my_count += 1
                else:
                    opp_count += 1
            
            if my_count == 2 and empty_count == 1:
                score += 10
            if opp_count == 2 and empty_count == 1:
                score -= 15
            if my_count == 1 and empty_count == 2:
                score += 1
        
        # 中央ボーナス
        center = game.board[1][1].top()
        if center:
            if center.player == self.my_player:
                score += 3
            else:
                score -= 3
        
        return score
    
    def _order_moves(self, game: GobbletGobblers, moves: list[Move]) -> list[Move]:
        """手の順序を調整"""
        def move_priority(move: Move) -> int:
            priority = 0
            if move.to_pos == (1, 1):
                priority += 10
            if move.to_pos in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                priority += 5
            priority += move.piece_size.value * 2
            if not move.is_from_hand():
                priority += 3
            return priority
        
        return sorted(moves, key=move_priority, reverse=True)
