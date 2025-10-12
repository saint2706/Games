# Games Catalog

This document provides a complete index of all available games in the repository, organized by category.

## 🎴 Card Games

Card games using standard 52-card decks or specialized card sets.

### Poker

**Location**: `card_games/poker/`  
**Description**: Texas Hold'em and Omaha variants with tournament mode, Monte Carlo AI, and comprehensive statistics  
**Players**: 2-9 (with 3 AI opponents)  
**Run**: `python -m card_games.poker`

Features:
- Multiple variants (Texas Hold'em, Omaha)
- Tournament mode with blind escalation
- Pot-limit, no-limit, and fixed-limit betting
- Statistics tracking and hand history
- GUI and CLI interfaces
- Adjustable AI difficulty

**Documentation**: [poker/README.md](card_games/poker/README.md)

---

### Blackjack

**Location**: `card_games/blackjack/`  
**Description**: Casino-style blackjack with splits, doubles, insurance, and surrender  
**Players**: 1 player vs dealer  
**Run**: `python -m card_games.blackjack`

Features:
- Multi-hand splitting
- Double down
- Insurance and surrender options
- Shoe management with automatic shuffling
- Side bets
- Card counting hints
- Premium GUI with card graphics

**Documentation**: [blackjack/README.md](card_games/blackjack/README.md)

---

### Bluff (Cheat)

**Location**: `card_games/bluff/`  
**Description**: Strategic bluffing game where players must claim card ranks and challenge suspicious plays  
**Players**: 2-5 (1 human + AI bots)  
**Run**: `python -m card_games.bluff`

Features:
- Adjustable difficulty (Noob to Insane)
- AI opponents with personality traits
- Challenge mechanics
- Multiple deck support
- Tournament mode
- Replay system

**Documentation**: [bluff/README.md](card_games/bluff/README.md)

---

### Uno

**Location**: `card_games/uno/`  
**Description**: Classic Uno with wild cards, action cards, and strategic AI  
**Players**: 2-10 (configurable human/AI mix)  
**Run**: `python -m card_games.uno`

Features:
- Full 108-card deck
- Wild +4 challenges
- Automatic UNO call enforcement
- House rules (stacking, 7-0 swap)
- Team mode
- Sound effects
- Adjustable AI skill

**Documentation**: [uno/README.md](card_games/uno/README.md)

---

### Hearts

**Location**: `card_games/hearts/`  
**Description**: Classic trick-taking game where the goal is to avoid hearts and the Queen of Spades  
**Players**: 4 (1 human + 3 AI)  
**Run**: `python -m card_games.hearts`

Features:
- Card passing phase (left, right, across, none rotation)
- Shooting the moon mechanic
- Strategic AI that avoids penalty cards
- First to 100 points loses
- Hearts breaking detection

**Documentation**: [hearts/README.md](card_games/hearts/README.md)

---

### Spades

**Location**: `card_games/spades/`  
**Description**: Partnership bidding game with nil bids and bags tracking  
**Players**: 4 (2 partnerships)  
**Run**: `python -m card_games.spades`

Features:
- Partnership play (teams of 2)
- Nil bid support (+100/-100)
- Bags tracking (10 bags = -100 points)
- Spades as trump suit
- First to 500 wins
- Strategic AI bidding and play

**Documentation**: [spades/README.md](card_games/spades/README.md)

---

### Gin Rummy

**Location**: `card_games/gin_rummy/`  
**Description**: Two-player melding game with knock and gin mechanics  
**Players**: 2 (1 human vs AI)  
**Run**: `python -m card_games.gin_rummy`

Features:
- Automatic meld detection (sets and runs)
- Deadwood calculation
- Knock when deadwood ≤ 10
- Gin bonus for 0 deadwood
- Undercut detection
- Multi-round scoring to 100

**Documentation**: [gin_rummy/README.md](card_games/gin_rummy/README.md)

---

### Bridge

**Location**: `card_games/bridge/`  
**Description**: Classic contract bridge with simplified automated bidding  
**Players**: 4 (2 partnerships)  
**Run**: `python -m card_games.bridge`

Features:
- Partnership play (North-South vs East-West)
- HCP-based bidding system
- Contract system (1♣ to 7NT)
- Trump suit mechanics
- Declarer and defender roles
- Contract scoring

**Documentation**: [bridge/README.md](card_games/bridge/README.md)

---

### Solitaire (Klondike)

**Location**: `card_games/solitaire/`  
**Description**: Classic patience game with tableau, foundation, stock, and waste piles  
**Players**: 1 (single player)  
**Run**: `python -m card_games.solitaire`

Features:
- 7 tableau piles with face-up/face-down tracking
- 4 foundation piles (Ace to King by suit)
- Stock and waste pile mechanics
- Move validation (color alternation, descending order)
- Auto-move functionality
- Win detection

**Documentation**: [solitaire/README.md](card_games/solitaire/README.md)

---

## 📝 Paper & Pencil Games

Classic paper-and-pencil games reimagined for the terminal and GUI.

### Tic-Tac-Toe

**Location**: `paper_games/tic_tac_toe/`  
**Description**: Classic noughts and crosses with perfect minimax AI  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.tic_tac_toe`

Features:
- Perfect minimax AI
- Larger board sizes (3x3 to 9x9)
- Ultimate Tic-Tac-Toe variant
- Network multiplayer
- Statistics tracking
- Multiple themes
- Coordinate input (A1-C3)

**Documentation**: [tic_tac_toe/README.md](paper_games/tic_tac_toe/README.md)

---

### Battleship

**Location**: `paper_games/battleship/`  
**Description**: Naval combat game with strategic ship placement and hunting AI  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.battleship`

Features:
- Configurable grid sizes (6x6 to 10x10)
- Multiple ship types
- AI difficulty levels (random to smart hunting)
- GUI with click-to-fire
- Salvo mode
- 2-player hot-seat mode

**Documentation**: [battleship/README.md](paper_games/battleship/README.md)

---

### Hangman

**Location**: `paper_games/hangman/`  
**Description**: Word guessing game with ASCII art gallows  
**Players**: 1 (vs computer)  
**Run**: `python -m paper_games.hangman`

Features:
- Curated word list
- Configurable mistake limits
- Progressive ASCII art
- Themed word categories
- Difficulty levels
- Multiplayer mode
- Hint system

**Documentation**: [hangman/README.md](paper_games/hangman/README.md)

---

### Dots and Boxes

**Location**: `paper_games/dots_and_boxes/`  
**Description**: Connect edges to capture boxes  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.dots_and_boxes`

Features:
- Variable board sizes (2x2 to 5x5)
- Chain highlighting
- Strategic AI
- Network multiplayer
- Coordinate guides
- Hint system

**Documentation**: [dots_and_boxes/README.md](paper_games/dots_and_boxes/README.md)

---

### Nim

**Location**: `paper_games/nim/`  
**Description**: Mathematical strategy game with optimal AI  
**Players**: 2-4 (vs optimal AI)  
**Run**: `python -m paper_games.nim`

Features:
- Classic Nim
- Variants: Northcott's Game, Wythoff's Game
- Graphical heap visualization
- Educational mode with strategy explanations
- Multiplayer support (3+ players)
- Custom rule variations
- Optimal AI opponent

**Documentation**: [nim/README.md](paper_games/nim/README.md)

---

### Unscramble

**Location**: `paper_games/unscramble/`  
**Description**: Word unscrambling game with curated vocabulary  
**Players**: 1 or multiplayer  
**Run**: `python -m paper_games.unscramble`

Features:
- Curated word list
- Timed mode
- Difficulty levels
- Multiplayer competition
- Themed word packs
- Achievement system
- Score tracking

**Documentation**: [unscramble/README.md](paper_games/unscramble/README.md)

---

### Connect Four

**Location**: `paper_games/connect_four/`  
**Description**: Vertical grid game with gravity mechanics  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.connect_four`

Features:
- 7x6 grid with gravity
- Win detection (4-in-a-row: horizontal, vertical, diagonal)
- Minimax AI with alpha-beta pruning
- Multiple difficulty levels
- Undo/redo moves

**Documentation**: [connect_four/README.md](paper_games/connect_four/README.md)

---

### Checkers

**Location**: `paper_games/checkers/`  
**Description**: Classic checkers with jump mechanics and king promotion  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.checkers`

Features:
- Standard 8x8 board
- Jump mechanics (single and multi-jump)
- King promotion
- Minimax AI
- Move validation
- Game state visualization

**Documentation**: [checkers/README.md](paper_games/checkers/README.md)

---

### Mancala

**Location**: `paper_games/mancala/`  
**Description**: Ancient stone distribution game  
**Players**: 2 (1 vs AI)  
**Run**: `python -m paper_games.mancala`

Features:
- Traditional Kalah rules
- Stone distribution mechanics
- Capture rules
- Strategic AI
- Multiple pit configurations
- Free turn mechanics

**Documentation**: [mancala/README.md](paper_games/mancala/README.md)

---

### Othello (Reversi)

**Location**: `paper_games/othello/`  
**Description**: Disc flipping game with positional strategy  
**Players**: 1 vs AI or 2 players  
**Run**: `python -m paper_games.othello`

Features:
- Standard 8x8 board
- Disc flipping mechanics
- Valid move highlighting
- Positional strategy AI
- Corner and edge priority
- Move hints

**Documentation**: [othello/README.md](paper_games/othello/README.md)

---

### Sudoku

**Location**: `paper_games/sudoku/`  
**Description**: Number placement puzzle  
**Players**: 1 (single player puzzle)  
**Run**: `python -m paper_games.sudoku`

Features:
- Puzzle generator
- Multiple difficulty levels (easy to expert)
- Hint system
- Move validation
- Conflict highlighting
- Timer and scoring

**Documentation**: [sudoku/README.md](paper_games/sudoku/README.md)

---

## 🎲 Dice Games

Dice-based games with random elements and strategic decisions. This is a new category with games planned for future implementation.

**Planned Games:**
- Craps - Casino dice game with pass/don't pass betting
- Farkle - Risk-based scoring with push-your-luck mechanics
- Liar's Dice - Bluffing game similar to Bluff but with dice
- Bunco - Party dice game with rounds and team scoring

**Documentation**: [dice_games/README.md](dice_games/README.md)

---

## 📚 Word & Trivia Games

Word-based games, trivia quizzes, and linguistic challenges. This is a new category with games planned for future implementation.

**Planned Games:**
- Trivia Quiz - Multiple choice questions from various categories with API integration
- Crossword Generator - Create and solve crossword puzzles with clue system
- Anagrams - Word rearrangement game with scoring system
- Scrabble-like - Tile-based word building game (avoiding trademark issues)

**Documentation**: [word_games/README.md](word_games/README.md)

---

## 🧩 Logic & Puzzle Games

Logic puzzles, brain teasers, and problem-solving games. This is a new category with games planned for future implementation.

**Planned Games:**
- Minesweeper - Classic mine detection game with difficulty levels
- Sokoban - Warehouse puzzle with box-pushing mechanics
- Sliding Puzzle (15-puzzle) - Number tile sliding game with solvability check
- Lights Out - Toggle-based puzzle with graph theory solution
- Picross/Nonograms - Picture logic puzzles with row/column hints

**Documentation**: [logic_games/README.md](logic_games/README.md)

---

## 🎮 Quick Start

### Running a Game

All games can be run using Python's module syntax:

```bash
# Card games
python -m card_games.poker
python -m card_games.blackjack
python -m card_games.uno

# Paper games
python -m paper_games.tic_tac_toe
python -m paper_games.battleship
python -m paper_games.hangman
```

### Common Options

Most games support these command-line options:

```bash
--gui              # Launch GUI interface (if available)
--difficulty LEVEL # Set AI difficulty (Easy, Medium, Hard)
--players N        # Number of players
--seed N           # Set random seed for reproducibility
--help             # Show game-specific options
```

### Example Commands

```bash
# Play poker tournament with hard AI
python -m card_games.poker --tournament --difficulty Hard

# Play blackjack in GUI mode
python -m card_games.blackjack --gui

# Play Uno with custom rules
python -m card_games.uno --players 4 --house-rules

# Play tic-tac-toe on larger board
python -m paper_games.tic_tac_toe --board-size 5

# Play battleship with larger grid
python -m paper_games.battleship --grid-size 10
```

## 📚 Documentation

- **Main README**: [README.md](README.md) - Project overview
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- **Architecture**: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) - Design patterns
- **Code Quality**: [docs/development/CODE_QUALITY.md](docs/development/CODE_QUALITY.md) - Standards and guidelines
- **Testing**: [docs/development/TESTING.md](docs/development/TESTING.md) - Testing guide
- **Development**: [docs/development/IMPLEMENTATION_NOTES.md](docs/development/IMPLEMENTATION_NOTES.md) - Implementation details
- **Roadmap**: [docs/planning/TODO.md](docs/planning/TODO.md) - Future plans

## 🎯 Game Statistics

- **Total Games**: 21 playable games (10 card games + 11 paper games)
- **Game Categories**: 5 (Card, Paper, Dice, Word, Logic - last 3 are new and awaiting implementations)
- **Total Lines of Code**: ~15,000+
- **Test Coverage**: 90%+ for most games
- **Supported Platforms**: Linux, macOS, Windows

## 🤖 AI Opponents

All games feature AI opponents with varying strategies:

- **Minimax**: Tic-Tac-Toe, Connect Four, Checkers
- **Monte Carlo**: Poker
- **Heuristic-based**: Blackjack, Bluff, Uno, Hearts, Spades
- **Optimal Strategy**: Nim
- **Positional Strategy**: Othello, Mancala

## 🎨 Interfaces

Most games support multiple interfaces:

- **CLI**: Text-based terminal interface (all games)
- **GUI**: Graphical Tkinter interface (Poker, Blackjack, Bluff, Uno, Battleship, and more)
- **Network**: Multiplayer support (select games)

## 🔧 Development

Want to add a new game? See:

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) - Architecture patterns
- [examples/](examples/) - Example implementations

All games follow consistent patterns using base classes from `common/` module.

## 📄 License

See repository license for details.

---

**Last Updated**: October 2025  
**Games Count**: 21 playable games  
**Status**: Active development
