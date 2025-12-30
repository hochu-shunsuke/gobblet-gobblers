# 🎮 Gobblet Gobblers AI

Gobblet Gobblersのゲームエンジンと自動対戦AIシステム

## 🎯 プロジェクト概要

1. **Phase 1**: ゲームエンジン + ランダムAI ✅
2. **Phase 2**: Minimax AI（予定）
3. **Phase 3**: ニューラルネットワークAI（予定）
4. **Phase 4**: 強化学習AI（予定）

## 📁 プロジェクト構造

```
gobblet-gobblers/
├── src/
│   ├── game.py           # ゲームエンジン
│   ├── arena.py          # 自動対戦システム
│   └── players/
│       ├── base_player.py
│       └── random_player.py
├── data/
│   └── games/            # 対戦ログ（JSON）
├── models/               # 学習済みモデル（予定）
└── requirements.txt
```

## 🚀 使い方

### ゲームエンジンのテスト

```bash
cd src
python game.py
```

### 自動対戦の実行

```bash
cd src
python arena.py
```

これにより:
- 1ゲームのデモ（詳細表示）
- 100ゲームの自動対戦
- `data/games/` にJSON形式で保存

## 📏 ゲームルール

- **ボード**: 3×3
- **コマ**: 各プレイヤー S×2, M×2, L×2
- **勝利条件**: 見えているコマで3つ並べる
- **Gobble**: 大きいコマで小さいコマを覆える
- **移動**: 盤上のどこへでも移動可能

## 📊 データ形式

保存されるJSONの構造:

```json
{
  "stats": {
    "total_games": 100,
    "player1_wins": 52,
    "player2_wins": 45,
    "draws": 3,
    "avg_turns": 12.5
  },
  "games": [
    {
      "player1": "RandomPlayer",
      "player2": "RandomPlayer",
      "moves": [...],
      "states": [...],
      "result": "PLAYER1_WIN",
      "winner": 1,
      "total_turns": 9
    }
  ]
}
```

## 🔜 次のステップ

- [ ] Minimax AIの実装
- [ ] Alpha-Beta枝刈りの追加
- [ ] ニューラルネットワークの訓練
- [ ] Web UIの作成
