package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"time"
)

func randInt(n int) int {
	return rand.Intn(n)
}

// MoveRecord for JSON output
type MoveRecord struct {
	PlayerNum int     `json:"player"`
	Size      string  `json:"size"`
	From      *[2]int `json:"from"`
	To        [2]int  `json:"to"`
}

// StateRecord for JSON output
type StateRecord struct {
	Board         [3][3][]string            `json:"board"`
	Hands         map[string]map[string]int `json:"hands"`
	CurrentPlayer int                       `json:"current_player"`
	Turn          int                       `json:"turn"`
}

// GameRecord for JSON output
type GameRecord struct {
	Player1    string        `json:"player1"`
	Player2    string        `json:"player2"`
	Moves      []MoveRecord  `json:"moves"`
	States     []StateRecord `json:"states"`
	Result     string        `json:"result"`
	Winner     *int          `json:"winner"`
	TotalTurns int           `json:"total_turns"`
}

func sizeToString(s PieceSize) string {
	switch s {
	case Small:
		return "SMALL"
	case Medium:
		return "MEDIUM"
	case Large:
		return "LARGE"
	}
	return ""
}

func gameToState(g *Game) StateRecord {
	state := StateRecord{
		CurrentPlayer: int(g.CurrentPlayer),
		Turn:          g.TurnCount,
		Hands: map[string]map[string]int{
			"player1": {"SMALL": g.Hands[Player1][Small], "MEDIUM": g.Hands[Player1][Medium], "LARGE": g.Hands[Player1][Large]},
			"player2": {"SMALL": g.Hands[Player2][Small], "MEDIUM": g.Hands[Player2][Medium], "LARGE": g.Hands[Player2][Large]},
		},
	}
	for r := 0; r < 3; r++ {
		for c := 0; c < 3; c++ {
			var stack []string
			for _, p := range g.Board[r][c].Stack {
				stack = append(stack, p.String())
			}
			state.Board[r][c] = stack
		}
	}
	return state
}

// AIPlayer interface
type AIPlayer interface {
	ChooseMove(game *Game) Move
}

func playGame(p1 AIPlayer, p2 AIPlayer, p1Name, p2Name string) GameRecord {
	game := NewGame()
	record := GameRecord{
		Player1: p1Name,
		Player2: p2Name,
		States:  []StateRecord{gameToState(game)},
	}

	for !game.IsGameOver() {
		var move Move
		if game.CurrentPlayer == Player1 {
			move = p1.ChooseMove(game)
		} else {
			move = p2.ChooseMove(game)
		}

		// Record move
		var from *[2]int
		if !move.IsFromHand() {
			from = &[2]int{move.FromRow, move.FromCol}
		}
		moveRec := MoveRecord{
			PlayerNum: int(game.CurrentPlayer),
			Size:      sizeToString(move.PieceSize),
			From:      from,
			To:        [2]int{move.ToRow, move.ToCol},
		}
		record.Moves = append(record.Moves, moveRec)

		game.MakeMove(move)
		record.States = append(record.States, gameToState(game))
	}

	// Result
	switch game.Result {
	case Player1Win:
		record.Result = "PLAYER1_WIN"
		w := 1
		record.Winner = &w
	case Player2Win:
		record.Result = "PLAYER2_WIN"
		w := 2
		record.Winner = &w
	case Draw:
		record.Result = "DRAW"
	}
	record.TotalTurns = game.TurnCount

	return record
}

func main() {
	rand.Seed(time.Now().UnixNano())

	fmt.Println("🎮 Gobblet Gobblers - Go Engine (Fast!)")
	fmt.Println("========================================")

	// Settings
	nGames := 500

	minimax4 := NewMinimaxPlayer(4)
	minimax3 := NewMinimaxPlayer(3)
	random := &RandomPlayer{}

	var allRecords []GameRecord

	// Minimax(4) vs Minimax(3)
	fmt.Printf("\n📊 Collecting: Minimax(4) vs Minimax(3) (%d games)...\n", nGames)
	start := time.Now()
	for i := 0; i < nGames; i++ {
		record := playGame(minimax4, minimax3, "MinimaxPlayer(d=4)", "MinimaxPlayer(d=3)")
		allRecords = append(allRecords, record)
		if (i+1)%100 == 0 {
			fmt.Printf("  %d/%d... (%.1fs elapsed)\n", i+1, nGames, time.Since(start).Seconds())
		}
	}
	fmt.Printf("  ✅ Done in %.1fs\n", time.Since(start).Seconds())

	// Minimax(3) vs Minimax(4)
	fmt.Printf("\n📊 Collecting: Minimax(3) vs Minimax(4) (%d games)...\n", nGames)
	start = time.Now()
	for i := 0; i < nGames; i++ {
		record := playGame(minimax3, minimax4, "MinimaxPlayer(d=3)", "MinimaxPlayer(d=4)")
		allRecords = append(allRecords, record)
		if (i+1)%100 == 0 {
			fmt.Printf("  %d/%d... (%.1fs elapsed)\n", i+1, nGames, time.Since(start).Seconds())
		}
	}
	fmt.Printf("  ✅ Done in %.1fs\n", time.Since(start).Seconds())

	// Minimax vs Random
	fmt.Printf("\n📊 Collecting: Minimax(4) vs Random (%d games)...\n", nGames)
	start = time.Now()
	for i := 0; i < nGames; i++ {
		record := playGame(minimax4, random, "MinimaxPlayer(d=4)", "RandomPlayer")
		allRecords = append(allRecords, record)
		if (i+1)%100 == 0 {
			fmt.Printf("  %d/%d... (%.1fs elapsed)\n", i+1, nGames, time.Since(start).Seconds())
		}
	}
	fmt.Printf("  ✅ Done in %.1fs\n", time.Since(start).Seconds())

	// Save to JSON
	filename := fmt.Sprintf("training_data_%s.json", time.Now().Format("20060102_150405"))
	data, _ := json.Marshal(allRecords)
	os.WriteFile(filename, data, 0644)

	fmt.Printf("\n💾 Saved %d games to: %s\n", len(allRecords), filename)
	fmt.Printf("📦 File size: %.2f MB\n", float64(len(data))/(1024*1024))
}
