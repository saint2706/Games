# Gin Rummy

The Gin Rummy module now simulates full-length matches with authentic rules:

* Alternating dealers with an opening upcard offer that each player may accept or pass.
* Exhaustive meld search to minimise deadwood and surface the exact sets/runs a player can table.
* Realistic scoring that distinguishes normal knocks, gin, big gin, and undercuts while processing opponent layoffs.
* Automatic stock reshuffles, discard restrictions (no throwing back the taken upcard), and a persistent round log.
* A smarter AI capable of evaluating draw sources, timing safe knocks, and discarding cards that hinder meld formation.

## Running the CLI

Launch the interactive experience with:

```bash
python -m card_games.gin_rummy
```

During play you will see your hand analysis, available melds, and live scoring updates after every hand. The AI follows the same rules and will attempt to capitalise on gin or undercuts when the odds favour those plays.

## Core Rules Implemented

* Two players receive 10 cards; the dealer alternates each round.
* The non-dealer may take the turned-up discard. If both players pass, that card cannot be taken until after the first stock draw.
* Melds include three- or four-of-a-kind sets and same-suit runs of length ≥ 3. The engine automatically finds the configuration that minimises deadwood.
* Players may knock with 10 or fewer deadwood points. Zero deadwood after drawing is scored as gin, or big gin when holding 11 cards.
* When a player knocks without gin, the opponent may lay off cards that extend the revealed melds before their deadwood is counted.
* Games continue until a player reaches 100 points.

### Scoring Details

| Event        | Points Awarded |
|--------------|----------------|
| Knock        | Deadwood difference (opponent minus knocker) |
| Gin          | Opponent deadwood + 25 bonus points |
| Big Gin      | Opponent deadwood + 31 bonus points |
| Undercut     | Deadwood difference + 25 points to the undercutter |

## Testing

Run the focused test suite with:

```bash
pytest tests/test_new_card_games.py::TestGinRummy -q
```

These tests cover meld discovery, deadwood optimisation, scoring outcomes (including layoffs and undercuts), and deck recycling behaviour.
