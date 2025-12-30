"""
NNPlayer デモ - 学習済みモデルで対戦
"""

import sys
sys.path.insert(0, '.')

from game import GobbletGobblers, Player
from players import RandomPlayer, MinimaxPlayer

# PyTorchチェック
try:
    from players import NNPlayer
    print("✅ PyTorch available!")
except ImportError:
    print("❌ PyTorch not installed. Run: pip install torch")
    sys.exit(1)


def demo_game(player1, player2, verbose=True):
    """1ゲームのデモ"""
    game = GobbletGobblers()
    
    if verbose:
        print(f"\n🎮 {player1.name} vs {player2.name}")
        print("=" * 40)
    
    while not game.is_game_over():
        current = player1 if game.current_player == Player.PLAYER1 else player2
        move = current.choose_move(game)
        
        if verbose:
            print(f"Turn {game.turn_count}: {current.name} plays {move}")
        
        game.make_move(move)
    
    if verbose:
        game.display()
        winner = game.get_winner()
        if winner:
            winner_name = player1.name if winner == Player.PLAYER1 else player2.name
            print(f"\n🎉 Winner: {winner_name}!")
        else:
            print("\n🤝 Draw!")
    
    return game.get_winner()


def main():
    print("=" * 50)
    print("🤖 Gobblet Gobblers - NN Player Demo")
    print("=" * 50)
    
    # モデル読み込み
    model_path = "../models/gobblet_model.pt"
    try:
        nn_player = NNPlayer(model_path=model_path)
        print(f"✅ Model loaded: {model_path}")
    except FileNotFoundError:
        print(f"❌ Model not found: {model_path}")
        print("   Please download from Colab and place in models/ folder")
        return
    
    random_player = RandomPlayer()
    minimax = MinimaxPlayer(max_depth=3)
    
    # デモ1: NN vs Random（1ゲーム詳細表示）
    print("\n" + "=" * 50)
    print("📍 Demo 1: NN vs Random (1 game, verbose)")
    demo_game(nn_player, random_player, verbose=True)
    
    # デモ2: NN vs Random（10ゲーム）
    print("\n" + "=" * 50)
    print("📍 Demo 2: NN vs Random (10 games)")
    nn_wins = 0
    for i in range(10):
        winner = demo_game(nn_player, random_player, verbose=False)
        if winner == Player.PLAYER1:
            nn_wins += 1
    print(f"   NN wins: {nn_wins}/10 ({nn_wins*10}%)")
    
    # デモ3: NN vs Minimax（5ゲーム）
    print("\n" + "=" * 50)
    print("📍 Demo 3: NN vs Minimax (5 games)")
    nn_wins_vs_minimax = 0
    for i in range(5):
        winner = demo_game(nn_player, minimax, verbose=False)
        if winner == Player.PLAYER1:
            nn_wins_vs_minimax += 1
        print(f"   Game {i+1}: {'NN wins!' if winner == Player.PLAYER1 else 'Minimax wins' if winner else 'Draw'}")
    print(f"   NN vs Minimax: {nn_wins_vs_minimax}/5")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    main()
