"""
Arena - 自動対戦システム
2つのAIを対戦させてデータを収集
"""

import json
import os
from datetime import datetime
from typing import Optional
from game import GobbletGobblers, GameResult, Player, Move
from players import BasePlayer, RandomPlayer


class Arena:
    """自動対戦を管理するクラス"""
    
    def __init__(self, player1: BasePlayer, player2: BasePlayer, verbose: bool = False):
        self.player1 = player1
        self.player2 = player2
        self.verbose = verbose
    
    def play_game(self) -> dict:
        """
        1ゲームを実行
        
        Returns:
            ゲーム記録（盤面履歴、手、結果など）
        """
        game = GobbletGobblers()
        
        # ゲーム記録
        record = {
            "player1": self.player1.name,
            "player2": self.player2.name,
            "moves": [],
            "states": [game.get_full_state()],
            "result": None,
            "winner": None,
            "total_turns": 0,
        }
        
        if self.verbose:
            game.display()
        
        while not game.is_game_over():
            # 現在のプレイヤーを取得
            current = self.player1 if game.current_player == Player.PLAYER1 else self.player2
            
            # 手を選択
            move = current.choose_move(game)
            
            # 手を記録
            move_record = {
                "player": game.current_player.value,
                "size": move.piece_size.name,
                "from": move.from_pos,
                "to": move.to_pos,
            }
            record["moves"].append(move_record)
            
            # 手を実行
            game.make_move(move)
            
            # 状態を記録
            record["states"].append(game.get_full_state())
            
            if self.verbose:
                print(f"\n{current.name} plays: {move}")
                game.display()
        
        # 結果を記録
        record["result"] = game.result.name
        record["total_turns"] = game.turn_count
        
        winner = game.get_winner()
        if winner:
            record["winner"] = winner.value
            if self.verbose:
                winner_name = self.player1.name if winner == Player.PLAYER1 else self.player2.name
                print(f"\n🎉 Winner: {winner_name} (Player {winner.value})")
        else:
            if self.verbose:
                print(f"\n🤝 Draw!")
        
        return record
    
    def play_games(self, n_games: int, save_dir: Optional[str] = None) -> dict:
        """
        複数ゲームを実行
        
        Args:
            n_games: ゲーム数
            save_dir: 保存先ディレクトリ（Noneなら保存しない）
        
        Returns:
            統計情報
        """
        stats = {
            "total_games": n_games,
            "player1_wins": 0,
            "player2_wins": 0,
            "draws": 0,
            "avg_turns": 0,
        }
        
        all_records = []
        total_turns = 0
        
        for i in range(n_games):
            if self.verbose or (i + 1) % 100 == 0:
                print(f"Game {i + 1}/{n_games}...")
            
            record = self.play_game()
            all_records.append(record)
            
            # 統計を更新
            if record["result"] == "PLAYER1_WIN":
                stats["player1_wins"] += 1
            elif record["result"] == "PLAYER2_WIN":
                stats["player2_wins"] += 1
            else:
                stats["draws"] += 1
            
            total_turns += record["total_turns"]
        
        stats["avg_turns"] = total_turns / n_games if n_games > 0 else 0
        
        # ファイルに保存
        if save_dir:
            os.makedirs(save_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"games_{self.player1.name}_vs_{self.player2.name}_{timestamp}.json"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "stats": stats,
                    "games": all_records
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Saved to: {filepath}")
        
        return stats


def main():
    """メイン関数 - デモ対戦"""
    print("=" * 50)
    print("Gobblet Gobblers - Arena")
    print("=" * 50)
    
    # ランダムAI同士で対戦
    player1 = RandomPlayer()
    player2 = RandomPlayer()
    
    arena = Arena(player1, player2, verbose=True)
    
    # 1ゲームのデモ
    print("\n📍 Demo: 1 game with verbose output")
    record = arena.play_game()
    
    # 100ゲーム実行してデータ保存
    print("\n" + "=" * 50)
    print("📊 Running 100 games...")
    arena_quiet = Arena(player1, player2, verbose=False)
    stats = arena_quiet.play_games(100, save_dir="../data/games")
    
    print("\n📈 Statistics:")
    print(f"  Player 1 ({player1.name}) wins: {stats['player1_wins']}")
    print(f"  Player 2 ({player2.name}) wins: {stats['player2_wins']}")
    print(f"  Draws: {stats['draws']}")
    print(f"  Average turns: {stats['avg_turns']:.1f}")


if __name__ == "__main__":
    main()
