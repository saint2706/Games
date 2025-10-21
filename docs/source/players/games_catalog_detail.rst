This document provides a complete index of all available games in the
repository, organized by category.

🎴 Card Games
-------------

Card games using standard 52-card decks or specialized card sets.

Poker
~~~~~

**Location**: ``card_games/poker/`` **Description**: Texas Hold’em and
Omaha variants with tournament mode, Monte Carlo AI, and comprehensive
statistics **Players**: 2-9 (with 3 AI opponents) **Run**:
``python -m card_games.poker``

Features:

-  Multiple variants (Texas Hold’em, Omaha)
-  Tournament mode with blind escalation
-  Pot-limit, no-limit, and fixed-limit betting
-  Statistics tracking and hand history
-  GUI and CLI interfaces
-  Adjustable AI difficulty

**Documentation**: `poker/README.md <card_games/poker/README.md>`__

--------------

Blackjack
~~~~~~~~~

**Location**: ``card_games/blackjack/`` **Description**: Casino-style
blackjack with splits, doubles, insurance, and surrender **Players**: 1
player vs dealer **Run**: ``python -m card_games.blackjack``

Features:

-  Multi-hand splitting
-  Double down
-  Insurance and surrender options
-  Shoe management with automatic shuffling
-  Side bets
-  Card counting hints
-  Premium GUI with card graphics

**Documentation**:
`blackjack/README.md <card_games/blackjack/README.md>`__

--------------

Bluff (Cheat)
~~~~~~~~~~~~~

**Location**: ``card_games/bluff/`` **Description**: Strategic bluffing
game where players must claim card ranks and challenge suspicious plays
**Players**: 2-5 (1 human + AI bots) **Run**:
``python -m card_games.bluff``

Features:

-  Adjustable difficulty (Noob to Insane)
-  AI opponents with personality traits
-  Challenge mechanics
-  Multiple deck support
-  Tournament mode
-  Replay system

**Documentation**: `bluff/README.md <card_games/bluff/README.md>`__

--------------

Uno
~~~

**Location**: ``card_games/uno/`` **Description**: Classic Uno with wild
cards, action cards, and strategic AI **Players**: 2-10 (configurable
human/AI mix) **Run**: ``python -m card_games.uno``

Features:

-  Full 108-card deck
-  Wild +4 challenges
-  Automatic UNO call enforcement
-  House rules (stacking, 7-0 swap)
-  Team mode
-  Sound effects
-  Adjustable AI skill

**Documentation**: `uno/README.md <card_games/uno/README.md>`__

--------------

Hearts
~~~~~~

**Location**: ``card_games/hearts/`` **Description**: Classic
trick-taking game where the goal is to avoid hearts and the Queen of
Spades **Players**: 4 (1 human + 3 AI) **Run**:
``python -m card_games.hearts``

Features:

-  Card passing phase (left, right, across, none rotation)
-  Shooting the moon mechanic
-  Strategic AI that avoids penalty cards
-  First to 100 points loses
-  Hearts breaking detection

**Documentation**: `hearts/README.md <card_games/hearts/README.md>`__

--------------

Spades
~~~~~~

**Location**: ``card_games/spades/`` **Description**: Partnership
bidding game with nil bids and bags tracking **Players**: 4 (2
partnerships) **Run**: ``python -m card_games.spades``

Features:

-  Partnership play (teams of 2)
-  Nil bid support (+100/-100)
-  Bags tracking (10 bags = -100 points)
-  Spades as trump suit
-  First to 500 wins
-  Strategic AI bidding and play

**Documentation**: `spades/README.md <card_games/spades/README.md>`__

--------------

Gin Rummy
~~~~~~~~~

**Location**: ``card_games/gin_rummy/`` **Description**: Two-player
melding game with knock and gin mechanics **Players**: 2 (1 human vs AI)
**Run**: ``python -m card_games.gin_rummy``

Features:

-  Automatic meld detection (sets and runs)
-  Deadwood calculation
-  Knock when deadwood ≤ 10
-  Gin bonus for 0 deadwood
-  Undercut detection
-  Multi-round scoring to 100

**Documentation**:
`gin_rummy/README.md <card_games/gin_rummy/README.md>`__

--------------

Bridge
~~~~~~

**Location**: ``card_games/bridge/`` **Description**: Classic contract
bridge with simplified automated bidding **Players**: 4 (2 partnerships)
**Run**: ``python -m card_games.bridge``

Features:

-  Partnership play (North-South vs East-West)
-  HCP-based bidding system
-  Contract system (1♣ to 7NT)
-  Trump suit mechanics
-  Declarer and defender roles
-  Contract scoring

**Documentation**: `bridge/README.md <card_games/bridge/README.md>`__

--------------

Canasta
~~~~~~~

**Location**: ``card_games/canasta/`` **Description**: Partnership
melding game with frozen discards, minimum meld requirements, and
canasta bonuses **Players**: 4 (two partnerships) **Run**:
``python -m card_games.canasta.cli``

Features:

-  Two-deck shoe with jokers and discard freezing
-  Partnership meld tracking with automatic canasta bonuses
-  Enforcement of wild-card limits and opening meld thresholds
-  Simple AI turns for non-human seats
-  CLI plus Tkinter and PyQt interfaces built on the shared GUI
   framework

**Documentation**: `canasta/README.md <card_games/canasta/README.md>`__

--------------

Solitaire (Klondike)
~~~~~~~~~~~~~~~~~~~~

**Location**: ``card_games/solitaire/`` **Description**: Classic
patience game with tableau, foundation, stock, and waste piles
**Players**: 1 (single player) **Run**:
``python -m card_games.solitaire``

Features:

-  7 tableau piles with face-up/face-down tracking
-  4 foundation piles (Ace to King by suit)
-  Stock and waste pile mechanics
-  Move validation (color alternation, descending order)
-  Auto-move functionality
-  Win detection

**Documentation**:
`solitaire/README.md <card_games/solitaire/README.md>`__

--------------

📝 Paper & Pencil Games
-----------------------

Classic paper-and-pencil games reimagined for the terminal and GUI.

Tic-Tac-Toe
~~~~~~~~~~~

**Location**: ``paper_games/tic_tac_toe/`` **Description**: Classic
noughts and crosses with perfect minimax AI **Players**: 1 vs AI or 2
players **Run**: ``python -m paper_games.tic_tac_toe``

Features:

-  Perfect minimax AI
-  Larger board sizes (3x3 to 9x9)
-  Ultimate Tic-Tac-Toe variant
-  Network multiplayer
-  Statistics tracking
-  Multiple themes
-  Coordinate input (A1-C3)

**Documentation**:
`tic_tac_toe/README.md <paper_games/tic_tac_toe/README.md>`__

--------------

Battleship
~~~~~~~~~~

**Location**: ``paper_games/battleship/`` **Description**: Naval combat
game with strategic ship placement and hunting AI **Players**: 1 vs AI
or 2 players **Run**: ``python -m paper_games.battleship``

Features:

-  Configurable grid sizes (6x6 to 10x10)
-  Multiple ship types
-  AI difficulty levels (random to smart hunting)
-  GUI with click-to-fire
-  Salvo mode
-  2-player hot-seat mode

**Documentation**:
`battleship/README.md <paper_games/battleship/README.md>`__

--------------

Hangman
~~~~~~~

**Location**: ``paper_games/hangman/`` **Description**: Word guessing
game with ASCII art gallows **Players**: 1 (vs computer) **Run**:
``python -m paper_games.hangman``

Features:

-  Curated word list
-  Configurable mistake limits
-  Progressive ASCII art
-  Themed word categories
-  Difficulty levels
-  Multiplayer mode
-  Hint system

**Documentation**: `hangman/README.md <paper_games/hangman/README.md>`__

--------------

Dots and Boxes
~~~~~~~~~~~~~~

**Location**: ``paper_games/dots_and_boxes/`` **Description**: Connect
edges to capture boxes **Players**: 1 vs AI or 2 players **Run**:
``python -m paper_games.dots_and_boxes``

Features:

-  Variable board sizes (2x2 to 5x5)
-  Chain highlighting
-  Strategic AI
-  Network multiplayer
-  Coordinate guides
-  Hint system

**Documentation**:
`dots_and_boxes/README.md <paper_games/dots_and_boxes/README.md>`__

--------------

Nim
~~~

**Location**: ``paper_games/nim/`` **Description**: Mathematical
strategy game with optimal AI **Players**: 2-4 (vs optimal AI) **Run**:
``python -m paper_games.nim``

Features:

-  Classic Nim
-  Variants: Northcott’s Game, Wythoff’s Game
-  Graphical heap visualization
-  Educational mode with strategy explanations
-  Multiplayer support (3+ players)
-  Custom rule variations
-  Optimal AI opponent

**Documentation**: `nim/README.md <paper_games/nim/README.md>`__

--------------

Unscramble
~~~~~~~~~~

**Location**: ``paper_games/unscramble/`` **Description**: Word
unscrambling game with curated vocabulary **Players**: 1 or multiplayer
**Run**: ``python -m paper_games.unscramble``

Features:

-  Curated word list
-  Timed mode
-  Difficulty levels
-  Multiplayer competition
-  Themed word packs
-  Achievement system
-  Score tracking

**Documentation**:
`unscramble/README.md <paper_games/unscramble/README.md>`__

--------------

Connect Four
~~~~~~~~~~~~

**Location**: ``paper_games/connect_four/`` **Description**: Vertical
grid game with gravity mechanics **Players**: 1 vs AI or 2 players
**Run**: ``python -m paper_games.connect_four``

Features:

-  7x6 grid with gravity
-  Win detection (4-in-a-row: horizontal, vertical, diagonal)
-  Minimax AI with alpha-beta pruning
-  Multiple difficulty levels
-  Undo/redo moves

**Documentation**:
`connect_four/README.md <paper_games/connect_four/README.md>`__

--------------

Checkers
~~~~~~~~

**Location**: ``paper_games/checkers/`` **Description**: Classic
checkers with jump mechanics and king promotion **Players**: 1 vs AI or
2 players **Run**: ``python -m paper_games.checkers``

Features:

-  Standard 8x8 board
-  Jump mechanics (single and multi-jump)
-  King promotion
-  Minimax AI
-  Move validation
-  Game state visualization

**Documentation**:
`checkers/README.md <paper_games/checkers/README.md>`__

--------------

Mancala
~~~~~~~

**Location**: ``paper_games/mancala/`` **Description**: Ancient stone
distribution game **Players**: 2 (1 vs AI) **Run**:
``python -m paper_games.mancala``

Features:

-  Traditional Kalah rules
-  Stone distribution mechanics
-  Capture rules
-  Strategic AI
-  Multiple pit configurations
-  Free turn mechanics

**Documentation**: `mancala/README.md <paper_games/mancala/README.md>`__

--------------

Othello (Reversi)
~~~~~~~~~~~~~~~~~

**Location**: ``paper_games/othello/`` **Description**: Disc flipping
game with positional strategy **Players**: 1 vs AI or 2 players **Run**:
``python -m paper_games.othello``

Features:

-  Standard 8x8 board
-  Disc flipping mechanics
-  Valid move highlighting
-  Positional strategy AI
-  Corner and edge priority
-  Move hints

**Documentation**: `othello/README.md <paper_games/othello/README.md>`__

--------------

Sudoku
~~~~~~

**Location**: ``paper_games/sudoku/`` **Description**: Number placement
puzzle **Players**: 1 (single player puzzle) **Run**:
``python -m paper_games.sudoku``

Features:

-  Puzzle generator
-  Multiple difficulty levels (easy to expert)
-  Hint system
-  Move validation
-  Conflict highlighting
-  Timer and scoring

**Documentation**: `sudoku/README.md <paper_games/sudoku/README.md>`__

--------------

Snakes and Ladders
~~~~~~~~~~~~~~~~~~

**Location**: ``paper_games/snakes_and_ladders/`` **Description**:
Classic board game with dice rolling, ladders, and snakes **Players**:
2-4 **Run**: ``python -m paper_games.snakes_and_ladders``

Features:

-  Standard 100-square board
-  Configurable snakes and ladders
-  Dice rolling mechanics
-  Turn-based gameplay
-  Multiple player support

**Documentation**:
`snakes_and_ladders/README.md <paper_games/snakes_and_ladders/README.md>`__

--------------

Yahtzee
~~~~~~~

**Location**: ``paper_games/yahtzee/`` **Description**: Dice scoring
game with category selection **Players**: 1-4 **Run**:
``python -m paper_games.yahtzee``

Features:

-  5 dice rolling (up to 3 rolls per turn)
-  13 scoring categories
-  Upper section bonus
-  Strategic dice keeping
-  Score tracking and display
-  Multiplayer support

**Documentation**: `yahtzee/README.md <paper_games/yahtzee/README.md>`__

--------------

Mastermind
~~~~~~~~~~

**Location**: ``paper_games/mastermind/`` **Description**: Code-breaking
game with colored pegs **Players**: 1 vs computer **Run**:
``python -m paper_games.mastermind``

Features:

-  6 colored pegs
-  Configurable code length (2-8)
-  Black and white peg feedback system
-  10 guess limit
-  Logical deduction gameplay
-  Guess history tracking

**Documentation**:
`mastermind/README.md <paper_games/mastermind/README.md>`__

--------------

20 Questions
~~~~~~~~~~~~

**Location**: ``paper_games/twenty_questions/`` **Description**: AI
guessing game with yes/no questions **Players**: 1 vs AI **Run**:
``python -m paper_games.twenty_questions``

Features:

-  Binary search strategy
-  Multiple object categories
-  20 question limit
-  Question history tracking
-  Interactive gameplay

**Documentation**:
`twenty_questions/README.md <paper_games/twenty_questions/README.md>`__

--------------

Boggle
~~~~~~

**Location**: ``paper_games/boggle/`` **Description**: Word search in
random letter grid **Players**: 1 **Run**:
``python -m paper_games.boggle``

Features:

-  Random 4x4 letter grid
-  Adjacent letter word formation
-  Dictionary validation
-  Word length scoring
-  Found word tracking

**Documentation**: `boggle/README.md <paper_games/boggle/README.md>`__

--------------

Four Square Writing
~~~~~~~~~~~~~~~~~~~

**Location**: ``paper_games/four_square_writing/`` **Description**:
Educational essay structure template **Players**: 1 **Run**:
``python -m paper_games.four_square_writing``

Features:

-  Four-quadrant writing method
-  Interactive template filling
-  Essay organization tool
-  Educational focus

**Documentation**:
`four_square_writing/README.md <paper_games/four_square_writing/README.md>`__

--------------

Pentago
~~~~~~~

**Location**: ``paper_games/pentago/`` **Description**: Board game with
rotating quadrants **Players**: 2 **Run**:
``python -m paper_games.pentago``

Features:

-  6x6 board with four 3x3 quadrants
-  Basic placement mechanics
-  5-in-a-row win condition
-  *Note: Quadrant rotation to be enhanced*

**Documentation**: `pentago/README.md <paper_games/pentago/README.md>`__

--------------

Backgammon
~~~~~~~~~~

**Location**: ``paper_games/backgammon/`` **Description**: Dice-based
race game **Players**: 2 **Run**: ``python -m paper_games.backgammon``

Features:

-  Traditional board layout
-  Dice rolling mechanics
-  Basic movement rules
-  *Note: Full rules and bearing off to be enhanced*

**Documentation**:
`backgammon/README.md <paper_games/backgammon/README.md>`__

--------------

Sprouts
~~~~~~~

**Location**: ``paper_games/sprouts/`` **Description**: Topological
graph game **Players**: 2 **Run**: ``python -m paper_games.sprouts``

Features:

-  Dot and line mechanics
-  Graph-based gameplay
-  Turn-based strategy
-  *Note: Full topological rules to be enhanced*

**Documentation**: `sprouts/README.md <paper_games/sprouts/README.md>`__

--------------

Chess
~~~~~

**Location**: ``paper_games/chess/`` **Description**: Classic chess game
**Players**: 2 **Run**: ``python -m paper_games.chess``

Features:

-  8x8 chess board
-  Basic piece movement
-  *Note: Full chess rules (castling, en passant, check/checkmate) and
   engine to be enhanced*

**Documentation**: `chess/README.md <paper_games/chess/README.md>`__

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
**Run**: ``python -m dice_games.craps``

Farkle
~~~~~~

Risk-based scoring game with push-your-luck mechanics. Roll six dice and
bank scoring combinations, but risk “farkling” (rolling no scoring dice)
and losing turn points.

**Features**: Hot dice bonus, multiple scoring patterns, strategic
banking **Run**: ``python -m dice_games.farkle``

Liar’s Dice
~~~~~~~~~~~

Bluffing game with dice bidding mechanics. Players secretly roll dice
and make bids on total dice values across all players. Challenge bids or
raise them higher.

**Features**: Hidden information, bluffing, challenge mechanics **Run**:
``python -m dice_games.liars_dice``

Bunco
~~~~~

Party dice game with rounds and team scoring. Roll three dice trying to
match the round number. Score 21 points for “Bunco” (all three dice
match the round).

**Features**: Simple rules, fast-paced, round-based scoring **Run**:
``python -m dice_games.bunco``

**Documentation**: `dice_games/README.md <dice_games/README.md>`__

--------------

📚 Word & Trivia Games
----------------------

Word-based games, trivia quizzes, and linguistic challenges.

Trivia Quiz
~~~~~~~~~~~

Multiple choice trivia questions from various categories. Test your
knowledge across different subjects with progressive difficulty.

**Features**: Multiple choice format, score tracking, diverse questions
**Run**: ``python -m word_games.trivia``

Crossword
~~~~~~~~~

Create and solve crossword puzzles with clue system. Fill in words based
on across and down clues to complete the puzzle grid.

**Features**: Grid-based puzzles, clue system, progressive solving
**Run**: ``python -m word_games.crossword``

Anagrams
~~~~~~~~

Word rearrangement game with scoring system. Unscramble letters to form
valid words as quickly as possible.

**Features**: Timed rounds, difficulty levels, score tracking **Run**:
``python -m word_games.anagrams``

WordBuilder
~~~~~~~~~~~

Tile-based word building game (Scrabble-like). Create words from letter
tiles with varying point values to maximize your score.

**Features**: Letter tiles, point values, strategic word building
**Run**: ``python -m word_games.wordbuilder``

**Documentation**: `word_games/README.md <word_games/README.md>`__

--------------

🧩 Logic & Puzzle Games
-----------------------

Logic puzzles, brain teasers, and problem-solving games.

Minesweeper
~~~~~~~~~~~

Classic mine detection puzzle game. Reveal cells on a grid using number
clues to identify mine locations. Don’t click on mines!

**Features**: Three difficulty levels, flag system, cascade reveal
**Run**: ``python -m logic_games.minesweeper``

Sokoban
~~~~~~~

Warehouse puzzle with box-pushing mechanics. Push boxes onto goal
positions without getting stuck. Plan moves carefully!

**Features**: Grid-based puzzles, undo support, level progression
**Run**: ``python -m logic_games.sokoban``

Sliding Puzzle (15-puzzle)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Number tile sliding game. Arrange numbered tiles in order by sliding
them into the empty space. Solvable configurations only.

**Features**: Multiple grid sizes, move counter, optimal solution hints
**Run**: ``python -m logic_games.sliding_puzzle``

Lights Out
~~~~~~~~~~

Toggle-based puzzle game. Click cells to toggle them and their
neighbors. Turn all lights off to win using pattern recognition.

**Features**: Grid-based toggling, pattern solving, move optimization
**Run**: ``python -m logic_games.lights_out``

Picross/Nonograms
~~~~~~~~~~~~~~~~~

Picture logic puzzles with row/column hints. Fill cells based on number
clues to reveal a hidden picture.

**Features**: Grid-based logic, number hints, picture reveal **Run**:
``python -m logic_games.picross``

**Documentation**: `logic_games/README.md <logic_games/README.md>`__

--------------

🎮 Quick Start
--------------

Running a Game
~~~~~~~~~~~~~~

All games can be run using Python’s module syntax:

.. code:: bash

   # Card games
   python -m card_games.poker
   python -m card_games.blackjack
   python -m card_games.uno

   # Paper games
   python -m paper_games.tic_tac_toe
   python -m paper_games.battleship
   python -m paper_games.hangman

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
   python -m card_games.poker --tournament --difficulty Hard

   # Play blackjack in GUI mode
   python -m card_games.blackjack --gui

   # Play Uno with custom rules
   python -m card_games.uno --players 4 --house-rules

   # Play tic-tac-toe on larger board
   python -m paper_games.tic_tac_toe --board-size 5

   # Play battleship with larger grid
   python -m paper_games.battleship --grid-size 10

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

All games follow consistent patterns using base classes from ``common/``
module.

📄 License
----------

See repository license for details.

--------------

**Last Updated**: 2025-10-16 **Games Count**: 49 playable games
**Status**: Active development
