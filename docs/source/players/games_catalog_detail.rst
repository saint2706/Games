This document provides a complete index of all available games in the
repository, organized by category.

🎴 Card Games
-------------

Card games using standard 52-card decks or specialized card sets.

Poker
~~~~~

**Location**: ``src/games_collection/games/card/poker/`` **Description**: Texas Hold’em and
Omaha variants with tournament mode, Monte Carlo AI, and comprehensive
statistics **Players**: 2-9 (with 3 AI opponents) **Run**:
``python -m games_collection.games.card.poker``

Features:

-  Multiple variants (Texas Hold’em, Omaha)
-  Tournament mode with blind escalation
-  Pot-limit, no-limit, and fixed-limit betting
-  Statistics tracking and hand history
-  GUI and CLI interfaces
-  Adjustable AI difficulty

**Documentation**: `poker/README.md <src/games_collection/games/card/poker/README.md>`__

--------------

Blackjack
~~~~~~~~~

**Location**: ``src/games_collection/games/card/blackjack/`` **Description**: Casino-style
blackjack with splits, doubles, insurance, and surrender **Players**: 1
player vs dealer **Run**: ``python -m games_collection.games.card.blackjack``

Features:

-  Multi-hand splitting
-  Double down
-  Insurance and surrender options
-  Shoe management with automatic shuffling
-  Side bets
-  Card counting hints
-  Premium GUI with card graphics

**Documentation**:
`blackjack/README.md <src/games_collection/games/card/blackjack/README.md>`__

--------------

Bluff (Cheat)
~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/card/bluff/`` **Description**: Strategic bluffing
game where players must claim card ranks and challenge suspicious plays
**Players**: 2-5 (1 human + AI bots) **Run**:
``python -m games_collection.games.card.bluff``

Features:

-  Adjustable difficulty (Noob to Insane)
-  AI opponents with personality traits
-  Challenge mechanics
-  Multiple deck support
-  Tournament mode
-  Replay system

**Documentation**: `bluff/README.md <src/games_collection/games/card/bluff/README.md>`__

--------------

Uno
~~~

**Location**: ``src/games_collection/games/card/uno/`` **Description**: Classic Uno with wild
cards, action cards, and strategic AI **Players**: 2-10 (configurable
human/AI mix) **Run**: ``python -m games_collection.games.card.uno``

Features:

-  Full 108-card deck
-  Wild +4 challenges
-  Automatic UNO call enforcement
-  House rules (stacking, 7-0 swap)
-  Team mode
-  Sound effects
-  Adjustable AI skill

**Documentation**: `uno/README.md <src/games_collection/games/card/uno/README.md>`__

--------------

Hearts
~~~~~~

**Location**: ``src/games_collection/games/card/hearts/`` **Description**: Classic
trick-taking game where the goal is to avoid hearts and the Queen of
Spades **Players**: 4 (1 human + 3 AI) **Run**:
``python -m games_collection.games.card.hearts``

Features:

-  Card passing phase (left, right, across, none rotation)
-  Shooting the moon mechanic
-  Strategic AI that avoids penalty cards
-  First to 100 points loses
-  Hearts breaking detection

**Documentation**: `hearts/README.md <src/games_collection/games/card/hearts/README.md>`__

--------------

Spades
~~~~~~

**Location**: ``src/games_collection/games/card/spades/`` **Description**: Partnership
bidding game with nil bids and bags tracking **Players**: 4 (2
partnerships) **Run**: ``python -m games_collection.games.card.spades``

Features:

-  Partnership play (teams of 2)
-  Nil bid support (+100/-100)
-  Bags tracking (10 bags = -100 points)
-  Spades as trump suit
-  First to 500 wins
-  Strategic AI bidding and play

**Documentation**: `spades/README.md <src/games_collection/games/card/spades/README.md>`__

--------------

Gin Rummy
~~~~~~~~~

**Location**: ``src/games_collection/games/card/gin_rummy/`` **Description**: Two-player
melding game with knock and gin mechanics **Players**: 2 (1 human vs AI)
**Run**: ``python -m games_collection.games.card.gin_rummy``

Features:

-  Automatic meld detection (sets and runs)
-  Deadwood calculation
-  Knock when deadwood ≤ 10
-  Gin bonus for 0 deadwood
-  Undercut detection
-  Multi-round scoring to 100

**Documentation**:
`gin_rummy/README.md <src/games_collection/games/card/gin_rummy/README.md>`__

--------------

Bridge
~~~~~~

**Location**: ``src/games_collection/games/card/bridge/`` **Description**: Classic contract
bridge with simplified automated bidding **Players**: 4 (2 partnerships)
**Run**: ``python -m games_collection.games.card.bridge``

Features:

-  Partnership play (North-South vs East-West)
-  HCP-based bidding system
-  Contract system (1♣ to 7NT)
-  Trump suit mechanics
-  Declarer and defender roles
-  Contract scoring

**Documentation**: `bridge/README.md <src/games_collection/games/card/bridge/README.md>`__

--------------

Canasta
~~~~~~~

**Location**: ``src/games_collection/games/card/canasta/`` **Description**: Partnership
melding game with frozen discards, minimum meld requirements, and
canasta bonuses **Players**: 4 (two partnerships) **Run**:
``python -m games_collection.games.card.canasta.cli``

Features:

-  Two-deck shoe with jokers and discard freezing
-  Partnership meld tracking with automatic canasta bonuses
-  Enforcement of wild-card limits and opening meld thresholds
-  Simple AI turns for non-human seats
-  CLI plus Tkinter and PyQt interfaces built on the shared GUI
   framework

**Documentation**: `canasta/README.md <src/games_collection/games/card/canasta/README.md>`__

--------------

Solitaire (Klondike)
~~~~~~~~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/card/solitaire/`` **Description**: Classic
patience game with tableau, foundation, stock, and waste piles
**Players**: 1 (single player) **Run**:
``python -m games_collection.games.card.solitaire``

Features:

-  7 tableau piles with face-up/face-down tracking
-  4 foundation piles (Ace to King by suit)
-  Stock and waste pile mechanics
-  Move validation (color alternation, descending order)
-  Auto-move functionality
-  Win detection

**Documentation**:
`solitaire/README.md <src/games_collection/games/card/solitaire/README.md>`__

--------------

📝 Paper & Pencil Games
-----------------------

Classic paper-and-pencil games reimagined for the terminal and GUI.

Tic-Tac-Toe
~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/tic_tac_toe/`` **Description**: Classic
noughts and crosses with perfect minimax AI **Players**: 1 vs AI or 2
players **Run**: ``python -m games_collection.games.paper.tic_tac_toe``

Features:

-  Perfect minimax AI
-  Larger board sizes (3x3 to 9x9)
-  Ultimate Tic-Tac-Toe variant
-  Network multiplayer
-  Statistics tracking
-  Multiple themes
-  Coordinate input (A1-C3)

**Documentation**:
`tic_tac_toe/README.md <src/games_collection/games/paper/tic_tac_toe/README.md>`__

--------------

Battleship
~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/battleship/`` **Description**: Naval combat
game with strategic ship placement and hunting AI **Players**: 1 vs AI
or 2 players **Run**: ``python -m games_collection.games.paper.battleship``

Features:

-  Configurable grid sizes (6x6 to 10x10)
-  Multiple ship types
-  AI difficulty levels (random to smart hunting)
-  GUI with click-to-fire
-  Salvo mode
-  2-player hot-seat mode

**Documentation**:
`battleship/README.md <src/games_collection/games/paper/battleship/README.md>`__

--------------

Hangman
~~~~~~~

**Location**: ``src/games_collection/games/paper/hangman/`` **Description**: Word guessing
game with ASCII art gallows **Players**: 1 (vs computer) **Run**:
``python -m games_collection.games.paper.hangman``

Features:

-  Curated word list
-  Configurable mistake limits
-  Progressive ASCII art
-  Themed word categories
-  Difficulty levels
-  Multiplayer mode
-  Hint system

**Documentation**: `hangman/README.md <src/games_collection/games/paper/hangman/README.md>`__

--------------

Dots and Boxes
~~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/dots_and_boxes/`` **Description**: Connect
edges to capture boxes **Players**: 1 vs AI or 2 players **Run**:
``python -m games_collection.games.paper.dots_and_boxes``

Features:

-  Variable board sizes (2x2 to 5x5)
-  Chain highlighting
-  Strategic AI
-  Network multiplayer
-  Coordinate guides
-  Hint system

**Documentation**:
`dots_and_boxes/README.md <src/games_collection/games/paper/dots_and_boxes/README.md>`__

--------------

Nim
~~~

**Location**: ``src/games_collection/games/paper/nim/`` **Description**: Mathematical
strategy game with optimal AI **Players**: 2-4 (vs optimal AI) **Run**:
``python -m games_collection.games.paper.nim``

Features:

-  Classic Nim
-  Variants: Northcott’s Game, Wythoff’s Game
-  Graphical heap visualization
-  Educational mode with strategy explanations
-  Multiplayer support (3+ players)
-  Custom rule variations
-  Optimal AI opponent

**Documentation**: `nim/README.md <src/games_collection/games/paper/nim/README.md>`__

--------------

Unscramble
~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/unscramble/`` **Description**: Word
unscrambling game with curated vocabulary **Players**: 1 or multiplayer
**Run**: ``python -m games_collection.games.paper.unscramble``

Features:

-  Curated word list
-  Timed mode
-  Difficulty levels
-  Multiplayer competition
-  Themed word packs
-  Achievement system
-  Score tracking

**Documentation**:
`unscramble/README.md <src/games_collection/games/paper/unscramble/README.md>`__

--------------

Connect Four
~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/connect_four/`` **Description**: Vertical
grid game with gravity mechanics **Players**: 1 vs AI or 2 players
**Run**: ``python -m games_collection.games.paper.connect_four``

Features:

-  7x6 grid with gravity
-  Win detection (4-in-a-row: horizontal, vertical, diagonal)
-  Minimax AI with alpha-beta pruning
-  Multiple difficulty levels
-  Undo/redo moves

**Documentation**:
`connect_four/README.md <src/games_collection/games/paper/connect_four/README.md>`__

--------------

Checkers
~~~~~~~~

**Location**: ``src/games_collection/games/paper/checkers/`` **Description**: Classic
checkers with jump mechanics and king promotion **Players**: 1 vs AI or
2 players **Run**: ``python -m games_collection.games.paper.checkers``

Features:

-  Standard 8x8 board
-  Jump mechanics (single and multi-jump)
-  King promotion
-  Minimax AI
-  Move validation
-  Game state visualization

**Documentation**:
`checkers/README.md <src/games_collection/games/paper/checkers/README.md>`__

--------------

Mancala
~~~~~~~

**Location**: ``src/games_collection/games/paper/mancala/`` **Description**: Ancient stone
distribution game **Players**: 2 (1 vs AI) **Run**:
``python -m games_collection.games.paper.mancala``

Features:

-  Traditional Kalah rules
-  Stone distribution mechanics
-  Capture rules
-  Strategic AI
-  Multiple pit configurations
-  Free turn mechanics

**Documentation**: `mancala/README.md <src/games_collection/games/paper/mancala/README.md>`__

--------------

Othello (Reversi)
~~~~~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/othello/`` **Description**: Disc flipping
game with positional strategy **Players**: 1 vs AI or 2 players **Run**:
``python -m games_collection.games.paper.othello``

Features:

-  Standard 8x8 board
-  Disc flipping mechanics
-  Valid move highlighting
-  Positional strategy AI
-  Corner and edge priority
-  Move hints

**Documentation**: `othello/README.md <src/games_collection/games/paper/othello/README.md>`__

--------------

Sudoku
~~~~~~

**Location**: ``src/games_collection/games/paper/sudoku/`` **Description**: Number placement
puzzle **Players**: 1 (single player puzzle) **Run**:
``python -m games_collection.games.paper.sudoku``

Features:

-  Puzzle generator
-  Multiple difficulty levels (easy to expert)
-  Hint system
-  Move validation
-  Conflict highlighting
-  Timer and scoring

**Documentation**: `sudoku/README.md <src/games_collection/games/paper/sudoku/README.md>`__

--------------

Snakes and Ladders
~~~~~~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/snakes_and_ladders/`` **Description**:
Classic board game with dice rolling, ladders, and snakes **Players**:
2-4 **Run**: ``python -m games_collection.games.paper.snakes_and_ladders``

Features:

-  Standard 100-square board
-  Configurable snakes and ladders
-  Dice rolling mechanics
-  Turn-based gameplay
-  Multiple player support

**Documentation**:
`snakes_and_ladders/README.md <src/games_collection/games/paper/snakes_and_ladders/README.md>`__

--------------

Yahtzee
~~~~~~~

**Location**: ``src/games_collection/games/paper/yahtzee/`` **Description**: Dice scoring
game with category selection **Players**: 1-4 **Run**:
``python -m games_collection.games.paper.yahtzee``

Features:

-  5 dice rolling (up to 3 rolls per turn)
-  13 scoring categories
-  Upper section bonus
-  Strategic dice keeping
-  Score tracking and display
-  Multiplayer support

**Documentation**: `yahtzee/README.md <src/games_collection/games/paper/yahtzee/README.md>`__

--------------

Mastermind
~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/mastermind/`` **Description**: Code-breaking
game with colored pegs **Players**: 1 vs computer **Run**:
``python -m games_collection.games.paper.mastermind``

Features:

-  6 colored pegs
-  Configurable code length (2-8)
-  Black and white peg feedback system
-  10 guess limit
-  Logical deduction gameplay
-  Guess history tracking

**Documentation**:
`mastermind/README.md <src/games_collection/games/paper/mastermind/README.md>`__

--------------

20 Questions
~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/twenty_questions/`` **Description**: AI
guessing game with yes/no questions **Players**: 1 vs AI **Run**:
``python -m games_collection.games.paper.twenty_questions``

Features:

-  Binary search strategy
-  Multiple object categories
-  20 question limit
-  Question history tracking
-  Interactive gameplay

**Documentation**:
`twenty_questions/README.md <src/games_collection/games/paper/twenty_questions/README.md>`__

--------------

Boggle
~~~~~~

**Location**: ``src/games_collection/games/paper/boggle/`` **Description**: Word search in
random letter grid **Players**: 1 **Run**:
``python -m games_collection.games.paper.boggle``

Features:

-  Random 4x4 letter grid
-  Adjacent letter word formation
-  Dictionary validation
-  Word length scoring
-  Found word tracking

**Documentation**: `boggle/README.md <src/games_collection/games/paper/boggle/README.md>`__

--------------

Four Square Writing
~~~~~~~~~~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/four_square_writing/`` **Description**:
Educational essay structure template **Players**: 1 **Run**:
``python -m games_collection.games.paper.four_square_writing``

Features:

-  Four-quadrant writing method
-  Interactive template filling
-  Essay organization tool
-  Educational focus

**Documentation**:
`four_square_writing/README.md <src/games_collection/games/paper/four_square_writing/README.md>`__

--------------

Pentago
~~~~~~~

**Location**: ``src/games_collection/games/paper/pentago/`` **Description**: Board game with
rotating quadrants **Players**: 2 **Run**:
``python -m games_collection.games.paper.pentago``

Features:

-  6x6 board with four 3x3 quadrants
-  Basic placement mechanics
-  5-in-a-row win condition
-  *Note: Quadrant rotation to be enhanced*

**Documentation**: `pentago/README.md <src/games_collection/games/paper/pentago/README.md>`__

--------------

Backgammon
~~~~~~~~~~

**Location**: ``src/games_collection/games/paper/backgammon/`` **Description**: Dice-based
race game **Players**: 2 **Run**: ``python -m games_collection.games.paper.backgammon``

Features:

-  Traditional board layout
-  Dice rolling mechanics
-  Basic movement rules
-  *Note: Full rules and bearing off to be enhanced*

**Documentation**:
`backgammon/README.md <src/games_collection/games/paper/backgammon/README.md>`__

--------------

Sprouts
~~~~~~~

**Location**: ``src/games_collection/games/paper/sprouts/`` **Description**: Topological
graph game **Players**: 2 **Run**: ``python -m games_collection.games.paper.sprouts``

Features:

-  Dot and line mechanics
-  Graph-based gameplay
-  Turn-based strategy
-  *Note: Full topological rules to be enhanced*

**Documentation**: `sprouts/README.md <src/games_collection/games/paper/sprouts/README.md>`__

--------------

Chess
~~~~~

**Location**: ``src/games_collection/games/paper/chess/`` **Description**: Classic chess game
**Players**: 2 **Run**: ``python -m games_collection.games.paper.chess``

Features:

-  8x8 chess board
-  Basic piece movement
-  *Note: Full chess rules (castling, en passant, check/checkmate) and
   engine to be enhanced*

**Documentation**: `chess/README.md <src/games_collection/games/paper/chess/README.md>`__

--------------

🎲 Dice Games
-------------

Dice-based games with random elements and strategic decisions.

Craps
~~~~~

Casino dice game with pass/don’t pass betting. Roll two dice and bet on
the outcome. Come-out roll wins on 7/11, loses on 2/3/12, otherwise
establishes a point.

**Features**: Pass line betting, don’t pass option, point system
**Run**: ``python -m games_collection.games.dice.craps``

Farkle
~~~~~~

Risk-based scoring game with push-your-luck mechanics. Roll six dice and
bank scoring combinations, but risk “farkling” (rolling no scoring dice)
and losing turn points.

**Features**: Hot dice bonus, multiple scoring patterns, strategic
banking **Run**: ``python -m games_collection.games.dice.farkle``

Liar’s Dice
~~~~~~~~~~~

Bluffing game with dice bidding mechanics. Players secretly roll dice
and make bids on total dice values across all players. Challenge bids or
raise them higher.

**Features**: Hidden information, bluffing, challenge mechanics **Run**:
``python -m games_collection.games.dice.liars_dice``

Bunco
~~~~~

Party dice game with rounds and team scoring. Roll three dice trying to
match the round number. Score 21 points for “Bunco” (all three dice
match the round).

**Features**: Simple rules, fast-paced, round-based scoring **Run**:
``python -m games_collection.games.dice.bunco``

**Documentation**: `src/games_collection/games/dice/README.md <src/games_collection/games/dice/README.md>`__

--------------

📚 Word & Trivia Games
----------------------

Word-based games, trivia quizzes, and linguistic challenges.

Trivia Quiz
~~~~~~~~~~~

Multiple choice trivia questions from various categories. Test your
knowledge across different subjects with progressive difficulty.

**Features**: Multiple choice format, score tracking, diverse questions
**Run**: ``python -m games_collection.games.word.trivia``

Crossword
~~~~~~~~~

Create and solve crossword puzzles with clue system. Fill in words based
on across and down clues to complete the puzzle grid.

**Features**: Grid-based puzzles, clue system, progressive solving
**Run**: ``python -m games_collection.games.word.crossword``

Anagrams
~~~~~~~~

Word rearrangement game with scoring system. Unscramble letters to form
valid words as quickly as possible.

**Features**: Timed rounds, difficulty levels, score tracking **Run**:
``python -m games_collection.games.word.anagrams``

WordBuilder
~~~~~~~~~~~

Tile-based word building game (Scrabble-like). Create words from letter
tiles with varying point values to maximize your score.

**Features**: Letter tiles, point values, strategic word building
**Run**: ``python -m games_collection.games.word.wordbuilder``

**Documentation**: `src/games_collection/games/word/README.md <src/games_collection/games/word/README.md>`__

--------------

🧩 Logic & Puzzle Games
-----------------------

Logic puzzles, brain teasers, and problem-solving games.

Minesweeper
~~~~~~~~~~~

Classic mine detection puzzle game. Reveal cells on a grid using number
clues to identify mine locations. Don’t click on mines!

**Features**: Three difficulty levels, flag system, cascade reveal
**Run**: ``python -m games_collection.games.logic.minesweeper``

Sokoban
~~~~~~~

Warehouse puzzle with box-pushing mechanics. Push boxes onto goal
positions without getting stuck. Plan moves carefully!

**Features**: Grid-based puzzles, undo support, level progression
**Run**: ``python -m games_collection.games.logic.sokoban``

Sliding Puzzle (15-puzzle)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Number tile sliding game. Arrange numbered tiles in order by sliding
them into the empty space. Solvable configurations only.

**Features**: Multiple grid sizes, move counter, optimal solution hints
**Run**: ``python -m games_collection.games.logic.sliding_puzzle``

Lights Out
~~~~~~~~~~

Toggle-based puzzle game. Click cells to toggle them and their
neighbors. Turn all lights off to win using pattern recognition.

**Features**: Grid-based toggling, pattern solving, move optimization
**Run**: ``python -m games_collection.games.logic.lights_out``

Picross/Nonograms
~~~~~~~~~~~~~~~~~

Picture logic puzzles with row/column hints. Fill cells based on number
clues to reveal a hidden picture.

**Features**: Grid-based logic, number hints, picture reveal **Run**:
``python -m games_collection.games.logic.picross``

**Documentation**: `src/games_collection/games/logic/README.md <src/games_collection/games/logic/README.md>`__

--------------

🎮 Quick Start
--------------

Running a Game
~~~~~~~~~~~~~~

All games can be run using Python’s module syntax:

.. code:: bash

   # Card games
   python -m games_collection.games.card.poker
   python -m games_collection.games.card.blackjack
   python -m games_collection.games.card.uno

   # Paper games
   python -m games_collection.games.paper.tic_tac_toe
   python -m games_collection.games.paper.battleship
   python -m games_collection.games.paper.hangman

Common Options
~~~~~~~~~~~~~~

Most games support these command-line options:

.. code:: bash

   --gui              # Launch GUI interface (if available)
   --difficulty LEVEL # Set AI difficulty (Easy, Medium, Hard)
   --players N        # Number of players
   --seed N           # Set random seed for reproducibility
   --help             # Show game-specific options

Example Commands
~~~~~~~~~~~~~~~~

.. code:: bash

   # Play poker tournament with hard AI
   python -m games_collection.games.card.poker --tournament --difficulty Hard

   # Play blackjack in GUI mode
   python -m games_collection.games.card.blackjack --gui

   # Play Uno with custom rules
   python -m games_collection.games.card.uno --players 4 --house-rules

   # Play tic-tac-toe on larger board
   python -m games_collection.games.paper.tic_tac_toe --board-size 5

   # Play battleship with larger grid
   python -m games_collection.games.paper.battleship --grid-size 10

📚 Documentation
----------------

-  **Main README**: `README.md <README.md>`__ - Project overview
-  **Contributing**: contributors/contributing (contributors/contributing) - How to
   contribute
-  **Architecture**:
   `docs/architecture/README.md <docs/architecture/README.md>`__ -
   Design patterns
-  **Code Quality**:
   developers/guides/code_quality (developers/guides/code_quality)
   - Standards and guidelines
-  **Testing**:
   developers/guides/testing (developers/guides/testing) -
   Testing guide
-  **Development**:
   developers/guides/implementation_notes (developers/guides/implementation_notes)
   - Implementation details
-  **Roadmap**: `docs/planning/README.md <docs/planning/README.md>`__ -
   Future plans

🎯 Game Statistics
------------------

-  **Total Games**: 49 playable games (15 card games + 21 paper games +
   4 dice games + 4 word games + 5 logic games)
-  **Game Categories**: 5 (Card, Paper, Dice, Word, Logic)
-  **Total Lines of Code**: ~229,000+ (Python)
-  **Test Coverage**: 40%+ overall (goal: 90%+), with 682 tests
-  **Supported Platforms**: Linux, macOS, Windows

🤖 AI Opponents
---------------

All games feature AI opponents with varying strategies:

-  **Minimax**: Tic-Tac-Toe, Connect Four, Checkers
-  **Monte Carlo**: Poker
-  **Heuristic-based**: Blackjack, Bluff, Uno, Hearts, Spades
-  **Optimal Strategy**: Nim
-  **Positional Strategy**: Othello, Mancala

🎨 Interfaces
-------------

Most games support multiple interfaces:

-  **CLI**: Text-based terminal interface (all games)
-  **GUI**: Graphical Tkinter interface (Poker, Blackjack, Bluff, Uno,
   Battleship, and more)
-  **Network**: Multiplayer support (select games)

🔧 Development
--------------

Want to add a new game? See:

-  contributors/contributing (contributors/contributing) - Contribution guidelines
-  `docs/architecture/README.md <docs/architecture/README.md>`__ -
   Architecture patterns
-  `examples/ <examples/>`__ - Example implementations

All games follow consistent patterns using base classes from ``src/games_collection/core/``
module.

📄 License
----------

See repository license for details.

--------------

**Last Updated**: 2025-10-16 **Games Count**: 49 playable games
**Status**: Active development
