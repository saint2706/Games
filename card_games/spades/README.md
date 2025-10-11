# Spades

Partnership trick-taking game where spades are always trump. Players bid on tricks and partnerships work together to make their combined bid.

## How to Play

```bash
python -m card_games.spades
```

## Game Rules

- Four players in two partnerships (North-South vs East-West)
- Each player is dealt 13 cards
- **Opening lead**: The player holding the 2♣ leads the first trick of the rubber
- **Bidding phase**: Each player bids 0-13 tricks (0 is "nil", blind nil is supported for higher stakes)
- Spades are always trump and cannot be led until broken (unless a player has nothing but spades)
- Must follow suit if possible
- Partnerships combine the bids of their non-nil players and total tricks won
- Making the combined bid scores 10 points per trick bid
- Overtricks (bags) give 1 point each but 10 bags incur a 100-point penalty
- Nil bid: +100 if successful, -100 if failed (blind nil doubles these values)
- First partnership to 500 points wins, with ties broken by the higher score

## Features

- Partnership mechanics (0&2 vs 1&3) with persistent team scores and bag tracking
- Nil and blind-nil bid handling with automatic logging of bidding history
- Trick history preserved for post-hand analysis and next-round leader selection
- Enforced opening 2♣ lead and authentic spade-breaking restrictions
- AI bidding and play heuristics that respect the new rule set
- CLI walkthrough showing bids, trick transcripts, and cumulative scores after every round
