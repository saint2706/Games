# Bridge

Classic contract bridge with bidding, partnership play, and trick-taking. This is a simplified implementation of the complex game.

## How to Play

```bash
python -m card_games.bridge
```

## Game Rules

- Four players in two partnerships (North-South vs East-West)
- Each player is dealt 13 cards
- **Bidding Phase**: Players bid contracts (1♣ to 7NT)
  - Bids indicate level (6+level tricks needed) and trump suit
  - Higher bids can overcall lower bids
- **Playing Phase**: 
  - Declarer's partnership tries to make the contract
  - Defenders try to prevent it
  - Must follow suit if possible
  - Trump cards (if any) win tricks
- **Scoring**: Points awarded for making or defeating contracts

## Simplified Features

This implementation includes:
- Automated bidding based on High Card Points (HCP)
- Partnership play
- Trump suit mechanics
- Basic scoring system
- AI card play

Note: This is a simplified version. Full contract bridge includes complex bidding conventions, declarer play strategies, and detailed scoring.

## High Card Points (HCP)

- Ace = 4 points
- King = 3 points
- Queen = 2 points
- Jack = 1 point
