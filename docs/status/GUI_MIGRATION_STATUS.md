# GUI Migration Status: Tkinter → PyQt5

This document tracks the progress of migrating game GUIs from Tkinter to PyQt5.

## Overview

- **Total Games**: 14
- **Completed**: 3 (21%)
- **Remaining**: 11 (79%)

## Status by Category

### Paper Games (1/2 completed)

| Game | Status | GUI File | Notes |
| -------------- | ----------- | ---------------------------------------- | ----------------------------------------------- |
| Dots and Boxes | ✅ Complete | `paper_games/dots_and_boxes/gui_pyqt.py` | Proof of concept migration |
| Battleship | ⏳ Pending | - | Complex board with drag-and-drop ship placement |

### Card Games (2/12 completed)

| Game | Status | GUI File | Notes |
| ------------ | ---------- | ------------------------------------------- | --------------------------------- |
| Blackjack | ⏳ Pending | - | 688 lines, table-based layout |
| Bluff | ⏳ Pending | - | 451 lines, multi-player |
| Bridge | ⏳ Pending | - | 488 lines, complex bidding system |
| Crazy Eights | ⏳ Pending | - | 465 lines |
| Gin Rummy | ⏳ Pending | - | 709 lines, melding system |
| Go Fish | ✅ Complete | `card_games/go_fish/gui_pyqt.py` | 425 lines, simplest card game GUI |
| Hearts | ✅ Complete | `card_games/hearts/gui_pyqt.py` | 610 lines, trick-taking |
| Poker | ⏳ Pending | - | 437 lines, betting interface |
| Solitaire | ⏳ Pending | - | 729 lines, most complex GUI |
| Spades | ⏳ Pending | - | 582 lines, bidding and tricks |
| Uno | ⏳ Pending | - | 524 lines, special cards |
| War | ⏳ Pending | - | 622 lines, simple mechanics |

## Migration Guidelines

For detailed migration instructions, see:

- [GUI Migration Guide](../gui/MIGRATION_GUIDE.md)
- [PyQt5 Implementation Summary](../gui/PYQT5_IMPLEMENTATION.md)
- [GUI Frameworks Documentation](../gui/FRAMEWORKS.md)

### Quick Steps

1. Create `gui_pyqt.py` alongside existing `gui.py`
1. Import PyQt5 widgets and base class from `common.gui_base_pyqt`
1. Convert widget mappings (see migration guide)
1. Update event handlers from Tkinter to PyQt5 signals/slots
1. Convert layouts from pack/grid to QVBoxLayout/QHBoxLayout
1. Add tests in `tests/test_gui_pyqt.py`
1. Update this status file
1. Update documentation files

### Suggested Migration Order

Based on complexity (lines of code and features):

1. **Go Fish** (425 lines) - Simplest card game
1. **Poker** (437 lines) - Moderate complexity
1. **Bluff** (451 lines) - Multi-player interaction
1. **Crazy Eights** (465 lines) - Special rules
1. **Bridge** (488 lines) - Complex bidding
1. **Uno** (524 lines) - Special cards and colors
1. **Spades** (582 lines) - Trick-taking with bidding
1. **Hearts** (610 lines) - Trick-taking, point avoidance
1. **Battleship** (617 lines) - Complex board interaction
1. **War** (622 lines) - Despite simple rules, has animations
1. **Blackjack** (688 lines) - Betting and dealer logic
1. **Gin Rummy** (709 lines) - Complex melding system
1. **Solitaire** (729 lines) - Most complex, multiple layouts

## Testing

All PyQt5 GUIs must include:

- Import test in `tests/test_gui_pyqt.py`
- Initialization test (with display skip for CI)
- Widget creation verification
- Integration with existing game engine

## Dependencies

PyQt5 is installed as an optional dependency:

```bash
pip install -e ".[gui]"
```

Or directly:

```bash
pip install pyqt5>=5.15
```

## Progress Updates

When a game is migrated:

1. Update the status table above (✅ Complete, add GUI file path)
1. Update the completion counts at the top
1. Update documentation files:
   - `docs/gui/PYQT5_IMPLEMENTATION.md`
   - `docs/gui/FRAMEWORKS.md`
   - `docs/gui/MIGRATION_GUIDE.md`
1. Add the module to `tests/test_gui_pyqt.py`

## Related Resources

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt5 Documentation](https://doc.qt.io/qt-5/)
- [Base GUI Class](common/gui_base_pyqt.py)
- [Example Implementation](paper_games/dots_and_boxes/gui_pyqt.py)
