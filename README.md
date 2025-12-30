# 🎮 Gobblet Gobblers AI

3x3ボードで戦う「Gobblet Gobblers」のゲームエンジンとAI

## ゲームルール

- 各プレイヤーは **S（小）×2、M（中）×2、L（大）×2** のコマを持つ
- 大きいコマで小さいコマを **Gobble（飲み込み）** できる
- **3つ並べたら勝ち**（見えているコマのみカウント）

## 📊 AI性能

| AI | vs Random | vs Minimax | 手法 |
|----|-----------|------------|------|
| **Minimax** | 100% | - | 探索 |
| **NNPlayer V2** | ~95% | 挑戦中 | ニューラルネット |
| Random | 50% | 0% | ランダム |

## 🚀 クイックスタート

```bash
git clone https://github.com/hochu-shunsuke/gobblet-gobblers.git
cd gobblet-gobblers

# Python環境セットアップ
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# デモ実行
cd src && python demo_nn.py
```

## 📁 プロジェクト構造

```
gobblet-gobblers/
├── go-engine/              # 高速データ収集（Go言語）
│   ├── game.go
│   ├── player.go
│   └── main.go
├── src/                    # ゲームエンジン & AI（Python）
│   ├── game.py
│   ├── arena.py
│   ├── demo_nn.py
│   └── players/
│       ├── random_player.py
│       ├── minimax_player.py
│       └── nn_player.py
└── models/
    └── gobblet_model_v2.pt  # 学習済みモデル (88.9%)
```

## ⚡ 高速データ収集（Go）

```bash
cd go-engine
go run .
# → 1500ゲームを約100秒で収集
```

## 🧠 AI訓練

1. Go版でデータ収集
2. JSONファイルをColab等にアップロード
3. PyTorchで訓練

## 📈 開発履歴

| バージョン | 精度 | 内容 |
|-----------|------|------|
| V1 | 80.1% | Minimax vs Random で学習 |
| **V2** | **88.9%** | Minimax vs Minimax + Go高速化 |

## License

MIT
