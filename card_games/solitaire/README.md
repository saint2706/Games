# Solitaire (Klondike)

Classic single-player patience game where the goal is to build four foundation piles from Ace to King, one for each suit.

## How to Play

```bash
python -m card_games.solitaire
```

## Game Rules

- **Tableau**: Seven piles where cards can be moved in descending order with alternating colors
- **Foundation**: Four piles (one per suit) built from Ace to King
- **Stock**: Draw pile from which you can draw cards
- **Waste**: Discard pile where drawn cards are placed

### Commands

- `d` or `draw` - Draw a card from stock to waste
- `r` or `reset` - Reset stock from waste pile
- `a` or `auto` - Auto-move cards to foundations
- `w <dest>` - Move waste card (e.g., 'w 0' moves to tableau 0)
- `<src> f` - Move tableau card to foundation (e.g., '0 f')
- `<src> <dest> [n]` - Move n cards from tableau src to dest (e.g., '0 1 3')
- `h` or `help` - Show help
- `q` or `quit` - Quit game

## Features

- Standard Klondike rules
- Auto-move functionality
- Win detection
- Face-up/face-down card tracking
