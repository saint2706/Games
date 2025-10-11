# Card Games

A collection of card games implemented in Python. The project currently
includes a casino-inspired Texas hold'em experience (playable from the terminal
or a Tkinter-powered GUI), a lighthearted bluff-calling challenge with
adjustable AI difficulty, a richly themed blackjack table with a full graphical
interface, and a colourful take on Uno complete with bots.

## Repository layout

```text
card_games/
├── common/           # Shared card representations
├── poker/            # Texas hold'em simulator and utilities
├── bluff/            # Interactive bluff game
├── blackjack/        # Casino-style blackjack with splits, doubles, and a GUI table
└── uno/              # Classic Uno with bots and a CLI interface
paper_games/
├── battleship/      # Hunt hidden ships on a compact grid
├── dots_and_boxes/  # Claim edges to capture boxes against a computer foe
├── hangman/         # Guess the word before the gallows fills up (ASCII art + curated list)
├── nim/             # Take on an optimal opponent in the game of Nim
├── tic_tac_toe/     # Minimax-powered noughts and crosses with coordinate input
└── unscramble/      # Race to rebuild scrambled vocabulary words
```

## Documentation roadmap

Every game module now opens with an extensive module-level docstring that
introduces the contained classes and explains how they collaborate. Class and
function docstrings are deliberately verbose so that you can treat the source as
an executable design document. To dive in:

- Start with `card_games/bluff/bluff.py` for a guided tour of the Cheat/Bluff
  engine, including commentary on turn structure and challenge resolution.
- Explore `card_games/poker/poker.py` and `card_games/poker/gui.py` to see
  how the Texas hold'em mechanics feed into both a CLI and Tkinter front-end.
- Browse `card_games/bluff/gui.py` to learn how the GUI keeps its widgets in
  sync with the engine state using richly annotated helper methods.

Each module's docstrings provide inline references to supporting utilities so
you can jump between files without losing context.

## Paper and pencil classics

Looking for lighter fare? The `paper_games` package recreates a handful of
classroom staples:

- `python -m paper_games.hangman` drops you into a word-guessing showdown with
  configurable mistake limits, gallows art that fills in piece by piece, and a
  curated vocabulary sourced from the
  [The Hangman Wordlist](https://github.com/TheBiemGamer/The-Hangman-Wordlist)
  project. Go letter by letter or gamble on a full-word reveal.
- `python -m paper_games.tic_tac_toe` pits you against a perfect minimax AI that
  respects coin tosses for the opening move, supports X-or-O selection, and uses
  coordinate input (A1 through C3) so the board feels like the pencil-and-paper
  classic.
- `python -m paper_games.dots_and_boxes` lets you outline squares on a
  2×2 board, while the computer now reads chains, takes bonus turns, and prints
  coordinate guides so you can follow along with precision.
- `python -m paper_games.battleship` challenges you to sink a trio of hidden
  ships spread across a 6×6 ocean.
- `python -m paper_games.unscramble` serves up scrambled words over multiple
  rounds and keeps score of your successes, drawing from the same curated word
  list as hangman for consistency.
- `python -m paper_games.nim` offers a comprehensive exploration of
  combinatorial game theory with classic Nim plus variants (Northcott's Game
  and Wythoff's Game). Features include graphical heap visualization,
  educational mode with strategy explanations, multiplayer support (3+ players),
  and custom rule variations. The optimal AI opponent teaches winning strategies
  while you play.

## Blackjack

Take a seat at a richly detailed blackjack table that recreates the flow of a
casino shoe. The Tkinter interface renders premium card art, highlights the
active hand, animates the dealer's draw, and keeps your bankroll front and
centre while you decide when to hit, stand, double, or split.

```bash
python -m card_games.blackjack
```

Prefer the original text-mode experience? Launch it with:

```bash
python -m card_games.blackjack --cli --bankroll 300 --min-bet 15 --decks 4
```

Highlights:

- Shoe management with automatic shuffling as the cards run low.
- Animated dealer reveals, natural blackjack detection, and soft-17 behaviour.
- Support for doubling down, splitting pairs, and per-hand outcome summaries
  that update your bankroll instantly in both the GUI and CLI.

## Poker

Sit at a four-player poker table and battle three computer-controlled
opponents across full betting rounds. Each difficulty level tunes the bots'
Monte Carlo-backed decision making—higher settings reduce mistakes, tighten the
hands they play, and increase their aggression when they sense strength.

The poker module now supports multiple game variants, betting structures, and
tournament play with comprehensive statistics tracking.

```bash
# Classic Texas Hold'em
python -m card_games.poker --difficulty Medium --rounds 5 --seed 123

# Omaha Hold'em with 4 hole cards
python -m card_games.poker --variant omaha --rounds 5

# Tournament mode with increasing blinds
python -m card_games.poker --tournament --rounds 10

# Pot-limit betting
python -m card_games.poker --limit pot-limit --rounds 5
```

Gameplay features:

- **Game Variants**: Texas Hold'em (2 hole cards) and Omaha (4 hole cards with
  exact 2+3 hand evaluation)
- **Betting Limits**: No-limit, pot-limit, and fixed-limit structures
- **Tournament Mode**: Blinds increase automatically based on configurable schedule
- **Statistics Tracking**: Hands won, fold frequency, showdown performance, and
  net profit tracked for all players
- **Hand History**: Complete game logs saved to JSON files for post-session review
- **Showdown Animations**: Visual card reveals and hand ranking explanations in GUI
- Rotating dealer button with blinds, betting rounds (pre-flop through river),
  and side-pot aware chip accounting
- Skill profiles that estimate equity against unknown hands to guide calls,
  bluffs, and value raises
- Detailed action narration in the CLI plus a live-updating graphical table for
  players who prefer a visual experience

Launch the GUI to play the same match with card visuals, action buttons, and a
running log of the hand:

```bash
python -m card_games.poker --gui --difficulty Hard --rounds 3
python -m card_games.poker --gui --variant omaha --tournament
```

Evaluate an arbitrary set of cards via the helper utility:

```bash
python -m card_games.poker.poker_hand_evaluator As Kd Qh Jc Tc
```

## Bluff

Play a full game of Cheat/Bluff where every participant—bots included—handles a
hand of cards. Each turn a player discards a card face down and claims its
rank. If the claim is challenged, the entire pile swings to the truthful player;
otherwise it keeps growing until someone is caught. First to shed every card, or
whoever holds the fewest cards after the configured number of table rotations,
wins the match.

Difficulty levels tune the number of opponents, deck count, and AI
personalities:

| Difficulty | Bots | Decks | Personality |
| ---------- | ---- | ----- | ----------- |
| Noob | 1 | 1 | Cautious, rarely bluffs |
| Easy | 2 | 1 | Even tempered with light deception |
| Medium | 2 | 2 | Balanced mix of bluffing and scrutiny |
| Hard | 3 | 2 | Bolder bluffs and sharper challenges |
| Insane | 4 | 3 | Aggressive liars who constantly police rivals |

Fire up a five-rotation match on the default "Noob" setting from the terminal:

```bash
python -m card_games.bluff
```

Add variety with seeds, longer tables, or the graphical interface:

```bash
python -m card_games.bluff --difficulty Hard --rounds 7 --seed 42
python -m card_games.bluff --gui --difficulty Medium
```

### Gameplay highlights

- Bots manage full hands, weigh whether to lie based on the pot size, and keep
  memory of who was recently caught stretching the truth.
- Suspicion travels around the table. Other bots (and you) can challenge any
  claim, so expect lively AI-versus-AI skirmishes when a rival seems shady.
- The Tkinter interface offers card buttons, challenge controls, and a running
  event log alongside live card counts for every player.

## Uno

Enjoy a fast-paced game of Uno that recreates the classic 108-card deck,
supports stacking draw cards, and lets you battle an assortment of AI
personalities. The rebuilt engine adds authentic Wild +4 challenges, automatic
penalties when someone forgets to shout UNO, and smarter bots that weigh risks
before bluffing with a draw card. The terminal interface highlights the active
colour, tracks draw penalties, and prompts for wild-card colour selections
while bots automatically choose colours based on the makeup of their hands.

```bash
python -m card_games.uno --players 4 --bots 3 --bot-skill balanced --seed 2024
```

Highlights:

- Authentic card distribution with skips, reverses, draw-twos, and wild draw
  fours that support stacking and optional challenges when a rival might be
  bluffing.
- Adjustable bot aggression so you can face easy-going opponents or relentless
  action-card junkies that decide when to risk a Wild +4 challenge.
- Automatic UNO call enforcement: fail to declare in time and the table hands
  you a two-card penalty.
- Launch `python -m card_games.uno --gui` to enjoy a Tkinter interface with
  colour-coded cards, UNO toggles, penalty prompts, and a scrolling event log
  that mirrors each turn.
