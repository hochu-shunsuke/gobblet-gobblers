# 🎮 Gobblet Gobblers AI

Gobblet Gobblersのゲームエンジンと複数のAIプレイヤー

## 🎯 プロジェクト概要

| Phase | 内容 | 状態 |
|-------|------|------|
| 1 | ゲームエンジン + ランダムAI | ✅ 完成 |
| 2 | Minimax AI | ✅ 完成 |
| 3 | ニューラルネットワークAI | ✅ 完成 |
| 4 | 強化学習AI | 🔜 次のステップ |

## 📊 AI性能比較

| AI | vs Random | vs Minimax |
|----|-----------|------------|
| **Minimax** | 100% | - |
| **NNPlayer** | 82% | 0% |
| Random | 50% | 0% |

## 📁 プロジェクト構造

```
gobblet-gobblers/
├── README.md
├── requirements.txt
├── notebooks/
│   └── train_ai.ipynb      # Colab用ノートブック
├── models/
│   └── gobblet_model.pt    # 学習済みモデル
├── data/games/             # 対戦ログ
└── src/
    ├── game.py             # ゲームエンジン
    ├── arena.py            # 自動対戦システム
    ├── collect_data.py     # データ収集
    └── players/
        ├── base_player.py
        ├── random_player.py
        ├── minimax_player.py
        └── nn_player.py    # ニューラルネット
```

## 🚀 使い方

### インストール

```bash
pip install -r requirements.txt
```

### ゲームエンジンのテスト

```bash
cd src
python game.py
```

### 自動対戦

```python
from game import GobbletGobblers
from players import RandomPlayer, MinimaxPlayer
from arena import Arena

minimax = MinimaxPlayer(max_depth=4)
random_ai = RandomPlayer()

arena = Arena(minimax, random_ai)
stats = arena.play_games(100)
print(stats)
```

### NNプレイヤーの使用

```python
from players import NNPlayer

nn_player = NNPlayer(model_path='models/gobblet_model.pt')
```

## 📏 ゲームルール

- **ボード**: 3×3
- **コマ**: 各プレイヤー S×2, M×2, L×2
- **勝利条件**: 見えているコマで3つ並べる
- **Gobble**: 大きいコマで小さいコマを覆える
- **移動**: 盤上のどこへでも移動可能

## 🔜 次のステップ

- [ ] 強化学習（自己対戦）の実装
- [ ] より深いネットワークの試行
- [ ] Web UIの作成
