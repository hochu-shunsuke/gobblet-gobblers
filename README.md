# 🎮 Gobblet Gobblers AI

3x3ボードで戦う「Gobblet Gobblers」のゲームエンジンと複数のAIプレイヤー

## ゲームルール

- 各プレイヤーは **S（小）×2、M（中）×2、L（大）×2** のコマを持つ
- 大きいコマで小さいコマを **Gobble（飲み込み）** できる
- **3つ並べたら勝ち**（見えているコマのみカウント）

## 📊 AI性能

| AI | vs Random | vs Minimax | 特徴 |
|----|-----------|------------|------|
| **Minimax** | 100% | - | 完璧な探索 |
| **NNPlayer** | 82-100% | 0% | Minimaxの手を学習 |
| Random | 50% | 0% | ランダム |

## 🚀 クイックスタート

```bash
# クローン
git clone https://github.com/hochu-shunsuke/gobblet-gobblers.git
cd gobblet-gobblers

# 仮想環境セットアップ
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# デモ実行
cd src
python demo_nn.py
```

## 📁 プロジェクト構造

```
gobblet-gobblers/
├── src/
│   ├── game.py             # ゲームエンジン
│   ├── arena.py            # 自動対戦
│   ├── demo_nn.py          # NNデモ
│   └── players/
│       ├── random_player.py
│       ├── minimax_player.py
│       └── nn_player.py
├── models/
│   └── gobblet_model.pt    # 学習済みモデル
└── notebooks/
    └── train_ai.ipynb      # Colab用訓練ノートブック
```

## 💻 使い方

### 基本対戦

```python
from game import GobbletGobblers
from players import RandomPlayer, MinimaxPlayer
from arena import Arena

arena = Arena(MinimaxPlayer(), RandomPlayer())
stats = arena.play_games(100)
print(f"Minimax win rate: {stats['player1_wins']}%")
```

### NNプレイヤー

```python
from players import NNPlayer

nn = NNPlayer(model_path='../models/gobblet_model.pt')
```

## 🧠 AI訓練（Colab）

1. `notebooks/train_ai.ipynb` を Colab で開く
2. データ収集を実行（Minimax vs Random 1000ゲーム）
3. ニューラルネットワークを訓練
4. `gobblet_model.pt` をダウンロード

## License

MIT
