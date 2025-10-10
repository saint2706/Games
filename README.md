# Card Games

A collection of card games implemented in Python. The project currently
includes a casino-inspired Texas hold'em experience (playable from the terminal
or a Tkinter-powered GUI) and a lighthearted bluff-calling challenge with
adjustable AI difficulty.

## Repository layout

```
card_games/
├── common/           # Shared card representations
├── poker/            # Texas hold'em simulator and utilities
├── bluff/            # Interactive bluff game
└── uno/              # Classic Uno with bots and a CLI interface
```

## Poker

Sit at a four-player Texas hold'em table and battle three computer-controlled
opponents across full betting rounds. Each difficulty level tunes the bots'
Monte Carlo-backed decision making—higher settings reduce mistakes, tighten the
hands they play, and increase their aggression when they sense strength.

```bash
python -m card_games.poker --difficulty Medium --rounds 5 --seed 123
```

Gameplay features:

* Rotating dealer button with blinds, betting rounds (pre-flop through river),
  and side-pot aware chip accounting.
* Skill profiles that estimate equity against unknown hands to guide calls,
  bluffs, and value raises.
* Detailed action narration in the CLI plus a live-updating graphical table for
  players who prefer a visual experience.

Launch the GUI to play the same match with card visuals, action buttons, and a
running log of the hand:

```bash
python -m card_games.poker --gui --difficulty Hard --rounds 3
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
| Noob       | 1    | 1     | Cautious, rarely bluffs |
| Easy       | 2    | 1     | Even tempered with light deception |
| Medium     | 2    | 2     | Balanced mix of bluffing and scrutiny |
| Hard       | 3    | 2     | Bolder bluffs and sharper challenges |
| Insane     | 4    | 3     | Aggressive liars who constantly police rivals |

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

* Bots manage full hands, weigh whether to lie based on the pot size, and keep
  memory of who was recently caught stretching the truth.
* Suspicion travels around the table. Other bots (and you) can challenge any
  claim, so expect lively AI-versus-AI skirmishes when a rival seems shady.
* The Tkinter interface offers card buttons, challenge controls, and a running
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

* Authentic card distribution with skips, reverses, draw-twos, and wild draw
  fours that support stacking and optional challenges when a rival might be
  bluffing.
* Adjustable bot aggression so you can face easy-going opponents or relentless
  action-card junkies that decide when to risk a Wild +4 challenge.
* Automatic UNO call enforcement: fail to declare in time and the table hands
  you a two-card penalty.
* Launch `python -m card_games.uno --gui` to enjoy a Tkinter interface with
  colour-coded cards, UNO toggles, penalty prompts, and a scrolling event log
  that mirrors each turn.
