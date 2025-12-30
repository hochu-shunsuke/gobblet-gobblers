"""
Gobblet Gobblers - Game Engine
ゲームのコアロジックを実装
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
import copy


class PieceSize(Enum):
    """コマのサイズ"""
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __lt__(self, other):
        return self.value < other.value


class Player(Enum):
    """プレイヤー"""
    PLAYER1 = 1
    PLAYER2 = 2
    
    def opponent(self):
        return Player.PLAYER2 if self == Player.PLAYER1 else Player.PLAYER1


@dataclass
class Piece:
    """コマ"""
    player: Player
    size: PieceSize
    
    def __repr__(self):
        p = "1" if self.player == Player.PLAYER1 else "2"
        s = {PieceSize.SMALL: "S", PieceSize.MEDIUM: "M", PieceSize.LARGE: "L"}[self.size]
        return f"{p}{s}"


@dataclass
class Cell:
    """マス目（コマのスタック）"""
    stack: list[Piece] = field(default_factory=list)
    
    def top(self) -> Optional[Piece]:
        """一番上のコマを返す"""
        return self.stack[-1] if self.stack else None
    
    def can_place(self, piece: Piece) -> bool:
        """このコマを置けるか"""
        top = self.top()
        if top is None:
            return True
        return piece.size > top.size
    
    def place(self, piece: Piece):
        """コマを置く"""
        self.stack.append(piece)
    
    def remove_top(self) -> Optional[Piece]:
        """一番上のコマを取り除く"""
        return self.stack.pop() if self.stack else None
    
    def is_empty(self) -> bool:
        return len(self.stack) == 0
    
    def __repr__(self):
        top = self.top()
        return str(top) if top else "  "


@dataclass 
class Move:
    """手を表すクラス"""
    piece_size: PieceSize
    to_pos: tuple[int, int]  # (row, col)
    from_pos: Optional[tuple[int, int]] = None  # Noneなら手持ちから
    
    def is_from_hand(self) -> bool:
        return self.from_pos is None
    
    def __repr__(self):
        s = {PieceSize.SMALL: "S", PieceSize.MEDIUM: "M", PieceSize.LARGE: "L"}[self.piece_size]
        if self.from_pos:
            return f"{s}:({self.from_pos[0]},{self.from_pos[1]})->({self.to_pos[0]},{self.to_pos[1]})"
        return f"{s}:hand->({self.to_pos[0]},{self.to_pos[1]})"


class GameResult(Enum):
    """ゲーム結果"""
    ONGOING = 0
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    DRAW = 3


class GobbletGobblers:
    """Gobblet Gobblersのゲームエンジン"""
    
    MAX_TURNS = 50
    
    def __init__(self):
        # 3x3ボード
        self.board: list[list[Cell]] = [[Cell() for _ in range(3)] for _ in range(3)]
        
        # 各プレイヤーの手持ちコマ {サイズ: 残り個数}
        self.hands = {
            Player.PLAYER1: {PieceSize.SMALL: 2, PieceSize.MEDIUM: 2, PieceSize.LARGE: 2},
            Player.PLAYER2: {PieceSize.SMALL: 2, PieceSize.MEDIUM: 2, PieceSize.LARGE: 2},
        }
        
        # 現在の手番
        self.current_player = Player.PLAYER1
        
        # ターン数
        self.turn_count = 0
        
        # ゲーム結果
        self.result = GameResult.ONGOING
        
        # 手の履歴
        self.move_history: list[tuple[Player, Move]] = []
    
    def get_cell(self, row: int, col: int) -> Cell:
        """指定位置のセルを取得"""
        return self.board[row][col]
    
    def get_legal_moves(self, player: Optional[Player] = None) -> list[Move]:
        """合法手をすべて取得"""
        if player is None:
            player = self.current_player
            
        moves = []
        
        # 1. 手持ちから置く手
        for size, count in self.hands[player].items():
            if count > 0:
                for row in range(3):
                    for col in range(3):
                        if self.board[row][col].can_place(Piece(player, size)):
                            moves.append(Move(size, (row, col), None))
        
        # 2. 盤上のコマを移動する手
        for from_row in range(3):
            for from_col in range(3):
                cell = self.board[from_row][from_col]
                top = cell.top()
                if top and top.player == player:
                    for to_row in range(3):
                        for to_col in range(3):
                            if (from_row, from_col) != (to_row, to_col):
                                if self.board[to_row][to_col].can_place(top):
                                    moves.append(Move(top.size, (to_row, to_col), (from_row, from_col)))
        
        return moves
    
    def make_move(self, move: Move) -> bool:
        """手を実行"""
        player = self.current_player
        
        # 手持ちから置く
        if move.is_from_hand():
            if self.hands[player][move.piece_size] <= 0:
                return False
            piece = Piece(player, move.piece_size)
            if not self.board[move.to_pos[0]][move.to_pos[1]].can_place(piece):
                return False
            self.hands[player][move.piece_size] -= 1
            self.board[move.to_pos[0]][move.to_pos[1]].place(piece)
        
        # 盤上から移動
        else:
            from_cell = self.board[move.from_pos[0]][move.from_pos[1]]
            top = from_cell.top()
            if top is None or top.player != player or top.size != move.piece_size:
                return False
            if not self.board[move.to_pos[0]][move.to_pos[1]].can_place(top):
                return False
            piece = from_cell.remove_top()
            self.board[move.to_pos[0]][move.to_pos[1]].place(piece)
        
        # 履歴に追加
        self.move_history.append((player, move))
        
        # 勝敗判定
        self._check_winner()
        
        # ターン交代
        if self.result == GameResult.ONGOING:
            self.current_player = player.opponent()
            self.turn_count += 1
            
            # 最大ターン数チェック
            if self.turn_count >= self.MAX_TURNS:
                self.result = GameResult.DRAW
        
        return True
    
    def _check_winner(self):
        """勝者をチェック"""
        # 勝利ライン
        lines = [
            # 横
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # 縦
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # 斜め
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        
        for line in lines:
            pieces = [self.board[r][c].top() for r, c in line]
            if all(p is not None for p in pieces):
                if all(p.player == Player.PLAYER1 for p in pieces):
                    self.result = GameResult.PLAYER1_WIN
                    return
                if all(p.player == Player.PLAYER2 for p in pieces):
                    self.result = GameResult.PLAYER2_WIN
                    return
    
    def is_game_over(self) -> bool:
        """ゲーム終了か"""
        return self.result != GameResult.ONGOING
    
    def get_winner(self) -> Optional[Player]:
        """勝者を取得"""
        if self.result == GameResult.PLAYER1_WIN:
            return Player.PLAYER1
        elif self.result == GameResult.PLAYER2_WIN:
            return Player.PLAYER2
        return None
    
    def clone(self) -> 'GobbletGobblers':
        """ゲーム状態をディープコピー"""
        return copy.deepcopy(self)
    
    def get_board_state(self) -> list[list[Optional[str]]]:
        """盤面状態を簡易形式で取得（AI学習用）"""
        state = []
        for row in range(3):
            row_state = []
            for col in range(3):
                top = self.board[row][col].top()
                row_state.append(str(top) if top else None)
            state.append(row_state)
        return state
    
    def get_full_state(self) -> dict:
        """完全な盤面状態を取得（AI学習用）"""
        board_state = []
        for row in range(3):
            row_state = []
            for col in range(3):
                cell = self.board[row][col]
                stack = [str(p) for p in cell.stack]
                row_state.append(stack)
            board_state.append(row_state)
        
        return {
            "board": board_state,
            "hands": {
                "player1": {s.name: c for s, c in self.hands[Player.PLAYER1].items()},
                "player2": {s.name: c for s, c in self.hands[Player.PLAYER2].items()},
            },
            "current_player": self.current_player.value,
            "turn": self.turn_count,
        }
    
    def display(self):
        """盤面を表示"""
        print(f"\n--- Turn {self.turn_count} | Player {self.current_player.value}'s turn ---")
        print("    0    1    2")
        print("  +----+----+----+")
        for row in range(3):
            print(f"{row} |", end="")
            for col in range(3):
                cell = self.board[row][col]
                print(f" {cell} |", end="")
            print()
            print("  +----+----+----+")
        
        # 手持ち表示
        print(f"P1 hand: S={self.hands[Player.PLAYER1][PieceSize.SMALL]} M={self.hands[Player.PLAYER1][PieceSize.MEDIUM]} L={self.hands[Player.PLAYER1][PieceSize.LARGE]}")
        print(f"P2 hand: S={self.hands[Player.PLAYER2][PieceSize.SMALL]} M={self.hands[Player.PLAYER2][PieceSize.MEDIUM]} L={self.hands[Player.PLAYER2][PieceSize.LARGE]}")


# テスト用
if __name__ == "__main__":
    game = GobbletGobblers()
    game.display()
    
    # テスト: 合法手を表示
    moves = game.get_legal_moves()
    print(f"\nLegal moves ({len(moves)}):")
    for m in moves[:5]:
        print(f"  {m}")
    print("  ...")
