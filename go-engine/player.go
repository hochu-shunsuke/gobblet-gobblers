package main

import "math"

// MinimaxPlayer is an AI using minimax algorithm
type MinimaxPlayer struct {
	MaxDepth int
	MyPlayer Player
}

func NewMinimaxPlayer(maxDepth int) *MinimaxPlayer {
	return &MinimaxPlayer{MaxDepth: maxDepth}
}

func (p *MinimaxPlayer) ChooseMove(game *Game) Move {
	p.MyPlayer = game.CurrentPlayer
	moves := game.GetLegalMoves()
	
	if len(moves) == 0 {
		return Move{}
	}

	bestMove := moves[0]
	bestScore := math.Inf(-1)
	alpha := math.Inf(-1)
	beta := math.Inf(1)

	for _, move := range moves {
		gameCopy := game.Clone()
		gameCopy.MakeMove(move)
		score := p.minimax(gameCopy, p.MaxDepth-1, alpha, beta, false)
		
		if score > bestScore {
			bestScore = score
			bestMove = move
		}
		alpha = math.Max(alpha, score)
		
		if score > 900 {
			break
		}
	}

	return bestMove
}

func (p *MinimaxPlayer) minimax(game *Game, depth int, alpha, beta float64, isMaximizing bool) float64 {
	if game.IsGameOver() {
		return p.evaluateTerminal(game)
	}
	if depth == 0 {
		return p.evaluatePosition(game)
	}

	moves := game.GetLegalMoves()
	if len(moves) == 0 {
		return 0
	}

	if isMaximizing {
		maxEval := math.Inf(-1)
		for _, move := range moves {
			gameCopy := game.Clone()
			gameCopy.MakeMove(move)
			eval := p.minimax(gameCopy, depth-1, alpha, beta, false)
			maxEval = math.Max(maxEval, eval)
			alpha = math.Max(alpha, eval)
			if beta <= alpha {
				break
			}
		}
		return maxEval
	} else {
		minEval := math.Inf(1)
		for _, move := range moves {
			gameCopy := game.Clone()
			gameCopy.MakeMove(move)
			eval := p.minimax(gameCopy, depth-1, alpha, beta, true)
			minEval = math.Min(minEval, eval)
			beta = math.Min(beta, eval)
			if beta <= alpha {
				break
			}
		}
		return minEval
	}
}

func (p *MinimaxPlayer) evaluateTerminal(game *Game) float64 {
	if game.Result == Draw {
		return 0
	}
	winner := game.GetWinner()
	if winner == p.MyPlayer {
		return 1000 - float64(game.TurnCount)
	}
	return -1000 + float64(game.TurnCount)
}

func (p *MinimaxPlayer) evaluatePosition(game *Game) float64 {
	score := 0.0
	lines := [][3][2]int{
		{{0, 0}, {0, 1}, {0, 2}},
		{{1, 0}, {1, 1}, {1, 2}},
		{{2, 0}, {2, 1}, {2, 2}},
		{{0, 0}, {1, 0}, {2, 0}},
		{{0, 1}, {1, 1}, {2, 1}},
		{{0, 2}, {1, 2}, {2, 2}},
		{{0, 0}, {1, 1}, {2, 2}},
		{{0, 2}, {1, 1}, {2, 0}},
	}

	for _, line := range lines {
		myCount := 0
		oppCount := 0
		emptyCount := 0
		
		for _, pos := range line {
			top := game.Board[pos[0]][pos[1]].Top()
			if top == nil {
				emptyCount++
			} else if top.Player == p.MyPlayer {
				myCount++
			} else {
				oppCount++
			}
		}
		
		if myCount == 2 && emptyCount == 1 {
			score += 10
		}
		if oppCount == 2 && emptyCount == 1 {
			score -= 15
		}
		if myCount == 1 && emptyCount == 2 {
			score += 1
		}
	}

	// Center bonus
	center := game.Board[1][1].Top()
	if center != nil {
		if center.Player == p.MyPlayer {
			score += 3
		} else {
			score -= 3
		}
	}

	return score
}

// RandomPlayer chooses random moves
type RandomPlayer struct{}

func (p *RandomPlayer) ChooseMove(game *Game) Move {
	moves := game.GetLegalMoves()
	if len(moves) == 0 {
		return Move{}
	}
	return moves[randInt(len(moves))]
}
