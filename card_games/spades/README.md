# Spades

Partnership trick-taking game where spades are always trump. Players bid on tricks and partnerships work together to make their combined bid.

## How to Play

```bash
python -m card_games.spades
```

## Game Rules

- Four players in two partnerships (North-South vs East-West)
- Each player is dealt 13 cards
- **Bidding Phase**: Each player bids 0-13 tricks (0 is "nil" for bonus points)
- Spades are always trump
- Must follow suit if possible
- Partnerships combine their bids and tricks
- Making bid: Score 10 points per trick bid
- Overtricks (bags): 1 point each, but 10 bags = -100 points
- Nil bid: +100 if successful, -100 if failed
- First partnership to 500 points wins

## Features

- Partnership mechanics (0&2 vs 1&3)
- Nil bid handling with bonuses/penalties
- Bags tracking
- AI bidding strategy
- Strategic AI card play
- Full trick-taking implementation
