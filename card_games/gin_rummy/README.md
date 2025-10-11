# Gin Rummy

Two-player card game where players form melds (sets and runs) and try to minimize deadwood (unmatched cards).

## How to Play

```bash
python -m card_games.gin_rummy
```

## Game Rules

- Two players compete
- Each player is dealt 10 cards
- **Melds**:
  - **Set**: Three or four cards of the same rank
  - **Run**: Three or more consecutive cards of the same suit
- **Deadwood**: Unmatched cards count against you (face cards = 10, aces = 1)
- Draw from stock or discard pile
- Discard one card each turn
- **Knock**: Declare when deadwood ≤ 10 points
- **Gin**: Knock with 0 deadwood for bonus points
- **Undercut**: If opponent has less deadwood when you knock, they get bonus
- First to 100 points wins

## Scoring

- **Gin**: Opponent's deadwood + 25 bonus
- **Knock**: Deadwood difference
- **Undercut**: Deadwood difference + 25 bonus

## Features

- Automatic meld detection (sets and runs)
- Deadwood calculation
- Knock and gin logic
- Multi-round scoring
- AI opponent
