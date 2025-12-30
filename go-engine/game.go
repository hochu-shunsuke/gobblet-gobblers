package main

// PieceSize represents the size of a piece
type PieceSize int

const (
	Small  PieceSize = 1
	Medium PieceSize = 2
	Large  PieceSize = 3
)

// Player represents a player
type Player int

const (
	Player1 Player = 1
	Player2 Player = 2
)

func (p Player) Opponent() Player {
	if p == Player1 {
		return Player2
	}
	return Player1
}

// Piece represents a game piece
type Piece struct {
	Player Player
	Size   PieceSize
}

func (p Piece) String() string {
	var playerStr string
	if p.Player == Player1 {
		playerStr = "1"
	} else {
		playerStr = "2"
	}
	var sizeStr string
	switch p.Size {
	case Small:
		sizeStr = "S"
	case Medium:
		sizeStr = "M"
	case Large:
		sizeStr = "L"
	}
	return playerStr + sizeStr
}

// Cell represents a cell on the board (stack of pieces)
type Cell struct {
	Stack []Piece
}

func (c *Cell) Top() *Piece {
	if len(c.Stack) == 0 {
		return nil
	}
	return &c.Stack[len(c.Stack)-1]
}

func (c *Cell) CanPlace(piece Piece) bool {
	top := c.Top()
	if top == nil {
		return true
	}
	return piece.Size > top.Size
}

func (c *Cell) Place(piece Piece) {
	c.Stack = append(c.Stack, piece)
}

func (c *Cell) RemoveTop() *Piece {
	if len(c.Stack) == 0 {
		return nil
	}
	piece := c.Stack[len(c.Stack)-1]
	c.Stack = c.Stack[:len(c.Stack)-1]
	return &piece
}

// Move represents a game move
type Move struct {
	PieceSize PieceSize
	ToRow     int
	ToCol     int
	FromRow   int // -1 if from hand
	FromCol   int // -1 if from hand
}

func (m Move) IsFromHand() bool {
	return m.FromRow == -1
}

// GameResult represents the game result
type GameResult int

const (
	Ongoing    GameResult = 0
	Player1Win GameResult = 1
	Player2Win GameResult = 2
	Draw       GameResult = 3
)

// Game represents the game state
type Game struct {
	Board         [3][3]Cell
	Hands         map[Player]map[PieceSize]int
	CurrentPlayer Player
	TurnCount     int
	Result        GameResult
}

const MaxTurns = 50

// NewGame creates a new game
func NewGame() *Game {
	g := &Game{
		CurrentPlayer: Player1,
		TurnCount:     0,
		Result:        Ongoing,
		Hands: map[Player]map[PieceSize]int{
			Player1: {Small: 2, Medium: 2, Large: 2},
			Player2: {Small: 2, Medium: 2, Large: 2},
		},
	}
	return g
}

// Clone creates a deep copy of the game
func (g *Game) Clone() *Game {
	newGame := &Game{
		CurrentPlayer: g.CurrentPlayer,
		TurnCount:     g.TurnCount,
		Result:        g.Result,
		Hands: map[Player]map[PieceSize]int{
			Player1: {Small: g.Hands[Player1][Small], Medium: g.Hands[Player1][Medium], Large: g.Hands[Player1][Large]},
			Player2: {Small: g.Hands[Player2][Small], Medium: g.Hands[Player2][Medium], Large: g.Hands[Player2][Large]},
		},
	}
	for r := 0; r < 3; r++ {
		for c := 0; c < 3; c++ {
			newGame.Board[r][c].Stack = make([]Piece, len(g.Board[r][c].Stack))
			copy(newGame.Board[r][c].Stack, g.Board[r][c].Stack)
		}
	}
	return newGame
}

// GetLegalMoves returns all legal moves for the current player
func (g *Game) GetLegalMoves() []Move {
	var moves []Move
	player := g.CurrentPlayer

	// From hand
	for size, count := range g.Hands[player] {
		if count > 0 {
			for r := 0; r < 3; r++ {
				for c := 0; c < 3; c++ {
					if g.Board[r][c].CanPlace(Piece{player, size}) {
						moves = append(moves, Move{size, r, c, -1, -1})
					}
				}
			}
		}
	}

	// From board
	for fr := 0; fr < 3; fr++ {
		for fc := 0; fc < 3; fc++ {
			top := g.Board[fr][fc].Top()
			if top != nil && top.Player == player {
				for tr := 0; tr < 3; tr++ {
					for tc := 0; tc < 3; tc++ {
						if fr != tr || fc != tc {
							if g.Board[tr][tc].CanPlace(*top) {
								moves = append(moves, Move{top.Size, tr, tc, fr, fc})
							}
						}
					}
				}
			}
		}
	}

	return moves
}

// MakeMove executes a move
func (g *Game) MakeMove(move Move) bool {
	player := g.CurrentPlayer

	if move.IsFromHand() {
		if g.Hands[player][move.PieceSize] <= 0 {
			return false
		}
		piece := Piece{player, move.PieceSize}
		if !g.Board[move.ToRow][move.ToCol].CanPlace(piece) {
			return false
		}
		g.Hands[player][move.PieceSize]--
		g.Board[move.ToRow][move.ToCol].Place(piece)
	} else {
		fromCell := &g.Board[move.FromRow][move.FromCol]
		top := fromCell.Top()
		if top == nil || top.Player != player || top.Size != move.PieceSize {
			return false
		}
		if !g.Board[move.ToRow][move.ToCol].CanPlace(*top) {
			return false
		}
		piece := fromCell.RemoveTop()
		g.Board[move.ToRow][move.ToCol].Place(*piece)
	}

	g.checkWinner()

	if g.Result == Ongoing {
		g.CurrentPlayer = player.Opponent()
		g.TurnCount++
		if g.TurnCount >= MaxTurns {
			g.Result = Draw
		}
	}

	return true
}

func (g *Game) checkWinner() {
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
		var pieces [3]*Piece
		for i, pos := range line {
			pieces[i] = g.Board[pos[0]][pos[1]].Top()
		}
		if pieces[0] != nil && pieces[1] != nil && pieces[2] != nil {
			if pieces[0].Player == pieces[1].Player && pieces[1].Player == pieces[2].Player {
				if pieces[0].Player == Player1 {
					g.Result = Player1Win
				} else {
					g.Result = Player2Win
				}
				return
			}
		}
	}
}

// IsGameOver returns true if the game is over
func (g *Game) IsGameOver() bool {
	return g.Result != Ongoing
}

// GetWinner returns the winner (0 if no winner)
func (g *Game) GetWinner() Player {
	if g.Result == Player1Win {
		return Player1
	} else if g.Result == Player2Win {
		return Player2
	}
	return 0
}
