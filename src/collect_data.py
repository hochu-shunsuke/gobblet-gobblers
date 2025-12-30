"""
データ収集スクリプト
Minimax vs Random で高品質な学習データを生成
"""

import sys
import time
sys.path.insert(0, '.')

from game import GobbletGobblers, Player
from players import RandomPlayer, MinimaxPlayer
from arena import Arena


def main():
    print("=" * 60)
    print("📊 Data Collection for AI Training")
    print("=" * 60)
    
    # 設定
    MINIMAX_DEPTH = 4  # 深度4で十分強く、高速
    N_GAMES = 100      # 片側100ゲームずつ（計200ゲーム）
    
    # 1. Minimax (先手) vs Random (後手)
    print(f"\n📍 Collecting: Minimax vs Random ({N_GAMES} games)")
    print("   Minimax as Player 1...")
    
    minimax = MinimaxPlayer(max_depth=MINIMAX_DEPTH)
    random_player = RandomPlayer()
    
    start_time = time.time()
    arena1 = Arena(minimax, random_player, verbose=False)
    stats1 = arena1.play_games(N_GAMES, save_dir="../data/games")
    elapsed1 = time.time() - start_time
    
    print(f"   ✅ Completed in {elapsed1:.1f}s")
    print(f"   Minimax wins: {stats1['player1_wins']} ({stats1['player1_wins']/N_GAMES*100:.1f}%)")
    print(f"   Random wins:  {stats1['player2_wins']} ({stats1['player2_wins']/N_GAMES*100:.1f}%)")
    print(f"   Avg turns:    {stats1['avg_turns']:.1f}")
    
    # 2. Random (先手) vs Minimax (後手)
    print(f"\n📍 Collecting: Random vs Minimax ({N_GAMES} games)")
    print("   Minimax as Player 2...")
    
    start_time = time.time()
    arena2 = Arena(random_player, minimax, verbose=False)
    stats2 = arena2.play_games(N_GAMES, save_dir="../data/games")
    elapsed2 = time.time() - start_time
    
    print(f"   ✅ Completed in {elapsed2:.1f}s")
    print(f"   Random wins:  {stats2['player1_wins']} ({stats2['player1_wins']/N_GAMES*100:.1f}%)")
    print(f"   Minimax wins: {stats2['player2_wins']} ({stats2['player2_wins']/N_GAMES*100:.1f}%)")
    print(f"   Avg turns:    {stats2['avg_turns']:.1f}")
    
    # サマリー
    total_games = N_GAMES * 2
    minimax_total_wins = stats1['player1_wins'] + stats2['player2_wins']
    random_total_wins = stats1['player2_wins'] + stats2['player1_wins']
    
    print("\n" + "=" * 60)
    print("📈 Summary")
    print("=" * 60)
    print(f"Total games collected: {total_games}")
    print(f"Minimax win rate: {minimax_total_wins/total_games*100:.1f}%")
    print(f"Random win rate:  {random_total_wins/total_games*100:.1f}%")
    print(f"Total time: {elapsed1 + elapsed2:.1f}s")
    print("\n✅ Data saved to: data/games/")
    print("\nNext step: Train neural network with this data!")


if __name__ == "__main__":
    main()
