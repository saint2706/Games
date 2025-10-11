# Hearts

Trick-taking card game where the goal is to avoid taking hearts and the Queen of Spades, or to "shoot the moon" by taking all penalty cards.

## How to Play

```bash
python -m card_games.hearts
```

## Game Rules

- Four players compete individually
- Each player is dealt 13 cards
- Before each hand, players pass 3 cards in rotating directions (left, right, across, none)
- Players must follow suit if possible
- Hearts and the Queen of Spades are penalty cards
- Each heart is worth 1 point, Queen of Spades is worth 13 points
- **Shooting the Moon**: Taking all hearts AND the Queen of Spades gives 0 points to you and 26 to everyone else
- First player to reach 100 points loses

## Features

- Pass-the-cards mechanic with rotating directions
- Shooting the moon detection
- AI opponents that avoid hearts
- Strategic card play
- Full trick-taking rules implementation
