# GUI Migration Status: Tkinter → PyQt5

This document tracks the progress of migrating game GUIs from Tkinter to PyQt5.

## Overview

- **Total Games**: 14
- **Completed**: 2 (14%)
- **Remaining**: 12 (86%)

## Status by Category

### Paper Games (1/2 completed)

| Game           | Status      | GUI File                                 | Notes                                           |
| -------------- | ----------- | ---------------------------------------- | ----------------------------------------------- |
| Dots and Boxes | ✅ Complete | `paper_games/dots_and_boxes/gui_pyqt.py` | Proof of concept migration                      |
| Battleship     | ⏳ Pending  | -                                        | Complex board with drag-and-drop ship placement |

### Card Games (1/12 completed)

| Game         | Status     | GUI File | Notes                             |
| ------------ | ---------- | -------- | --------------------------------- |
| Blackjack    | ⏳ Pending | -        | 688 lines, table-based layout     |
| Bluff        | ⏳ Pending | -        | 451 lines, multi-player           |
| Bridge       | ⏳ Pending | -        | 488 lines, complex bidding system |
| Crazy Eights | ⏳ Pending | -        | 465 lines                         |
| Gin Rummy    | ⏳ Pending | -        | 709 lines, melding system         |
| Go Fish      | ✅ Complete | `card_games/go_fish/gui_pyqt.py` | 425 lines, simplest card game GUI |
| Hearts       | ⏳ Pending | -        | 610 lines, trick-taking           |
| Poker        | ⏳ Pending | -        | 437 lines, betting interface      |
| Solitaire    | ⏳ Pending | -        | 729 lines, most complex GUI       |
| Spades       | ⏳ Pending | -        | 582 lines, bidding and tricks     |
| Uno          | ⏳ Pending | -        | 524 lines, special cards          |
| War          | ⏳ Pending | -        | 622 lines, simple mechanics       |

## Migration Guidelines

For detailed migration instructions, see:

- [GUI Migration Guide](docs/GUI_MIGRATION_GUIDE.md)
- [PyQt5 Implementation Summary](docs/PYQT5_IMPLEMENTATION.md)
- [GUI Frameworks Documentation](docs/GUI_FRAMEWORKS.md)

### Quick Steps

1. Create `gui_pyqt.py` alongside existing `gui.py`
2. Import PyQt5 widgets and base class from `common.gui_base_pyqt`
3. Convert widget mappings (see migration guide)
4. Update event handlers from Tkinter to PyQt5 signals/slots
5. Convert layouts from pack/grid to QVBoxLayout/QHBoxLayout
6. Add tests in `tests/test_gui_pyqt.py`
7. Update this status file
8. Update documentation files

### Suggested Migration Order

Based on complexity (lines of code and features):

1. **Go Fish** (425 lines) - Simplest card game
2. **Poker** (437 lines) - Moderate complexity
3. **Bluff** (451 lines) - Multi-player interaction
4. **Crazy Eights** (465 lines) - Special rules
5. **Bridge** (488 lines) - Complex bidding
6. **Uno** (524 lines) - Special cards and colors
7. **Spades** (582 lines) - Trick-taking with bidding
8. **Hearts** (610 lines) - Trick-taking, point avoidance
9. **Battleship** (617 lines) - Complex board interaction
10. **War** (622 lines) - Despite simple rules, has animations
11. **Blackjack** (688 lines) - Betting and dealer logic
12. **Gin Rummy** (709 lines) - Complex melding system
13. **Solitaire** (729 lines) - Most complex, multiple layouts

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
2. Update the completion counts at the top
3. Update documentation files:
   - `docs/PYQT5_IMPLEMENTATION.md`
   - `docs/GUI_FRAMEWORKS.md`
   - `docs/GUI_MIGRATION_GUIDE.md`
4. Add the module to `tests/test_gui_pyqt.py`

## Related Resources

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt5 Documentation](https://doc.qt.io/qt-5/)
- [Base GUI Class](common/gui_base_pyqt.py)
- [Example Implementation](paper_games/dots_and_boxes/gui_pyqt.py)
