# Bridge

Classic contract bridge with bidding, partnership play, and trick-taking. This implementation now models key elements of modern
duplicate-style bridge including vulnerability, doubles, and rubber-style scoring.

## How to Play

```bash
python -m card_games.bridge
```

## Game Rules

- Four players in two partnerships (North-South vs East-West)
- Each player is dealt 13 cards
- **Bidding Phase**:
  - Fully automated auction using High Card Points, distribution, and simple partnership logic
  - Supports takeout doubles and balanced no-trump contracts
  - Vulnerability for the board is announced before the auction
  - Declarer is assigned to the first partnership member to bid the contract suit
- **Playing Phase**:
  - Declarer's partnership tries to make the contract, defenders try to defeat it
  - Left-hand opponent of declarer leads the opening card, dummy is revealed after the lead
  - Players must follow suit if possible, otherwise they may trump or discard
  - AI play favours holding winners when partner is ahead and uses trumps to contest tricks
- **Scoring**:
  - Rubber-style scoring with bonuses for games, slams, and insult points on doubled contracts
  - Accurate penalties for undertricks including vulnerability adjustments
  - Overtricks, doubles, and redoubles follow standard contract bridge rules

## Simplified Features

This implementation includes:
- Automated bidding with opening, response, and overcall logic
- Partnership-aware AI for trick play
- Trump suit mechanics and realistic trick evaluation
- Vulnerability-aware scoring with doubles and redoubles
- CLI presentation of the full bidding history and scoring summary

## High Card Points (HCP)

- Ace = 4 points
- King = 3 points
- Queen = 2 points
- Jack = 1 point
