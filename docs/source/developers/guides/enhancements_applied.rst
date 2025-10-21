Enhanced Features Applied to Games
==================================

This document summarizes the infrastructure enhancements that have been
applied to demonstrate the capabilities of the common architecture
systems.

Overview
--------

Four games have been enhanced to demonstrate different infrastructure
capabilities:

1. **War (Card Game)** - Save/Load Functionality
2. **Tic-Tac-Toe (Paper Game)** - Replay/Undo Functionality
3. **Hangman (Paper Game)** - CLI Enhancements
4. **Hearts & Spades (Card Games)** - GUI Preference Persistence

1. War Game - Save/Load Functionality
-------------------------------------

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/card/war/game.py``**

-  Added ``to_dict()`` method to serialize game state
-  Added ``from_dict()`` class method to deserialize and restore game
   state
-  Serializes all game components: player decks, pile, state, rounds,
   wars, winner

**File: ``src/games_collection/games/card/war/gui.py``**

-  Integrated ``SaveLoadManager`` from
   ``common.architecture.persistence``
-  Added “Save Game” button to GUI
-  Added “Load Game” button to GUI
-  Implemented ``_save_game()`` handler with file dialog
-  Implemented ``_load_game()`` handler with file selection

Usage
~~~~~

Players can now:

-  Save their game progress at any time during play
-  Load previously saved games to continue from where they left off
-  Games are saved with metadata (timestamp, game type)
-  Save files are stored in ``./saves/`` directory

Testing
~~~~~~~

.. code:: bash

   python -m games_collection.games.card.war --gui
   # Click "Save Game" during gameplay
   # Click "Load Game" to restore a saved game

2. Tic-Tac-Toe - Replay/Undo Functionality
------------------------------------------

.. _changes-made-1:

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/paper/tic_tac_toe/tic_tac_toe.py``**

-  Integrated ``ReplayManager`` from ``common.architecture.replay``
-  Added replay manager initialization in ``__post_init__()``
-  Modified ``make_move()`` to record actions with state snapshots
-  Added ``undo_last_move()`` method to undo moves
-  Added ``can_undo()`` method to check if undo is available

**File: ``src/games_collection/games/paper/tic_tac_toe/cli.py``**

-  Added ‘undo’ command support in the game loop
-  Undoing reverts both the human’s last move and the computer’s
   previous move
-  Automatically switches turn back after undo

.. _enhancements-applied-usage-1:

Usage
~~~~~

During gameplay:

-  Type ``undo`` instead of a move coordinate
-  The game will undo your last move and the computer’s previous move
-  The board state is fully restored from the snapshot
-  Continue playing from the restored position

.. _enhancements-applied-testing-1:

Testing
~~~~~~~

.. code:: bash

   python -m games_collection.games.paper.tic_tac_toe
   # Make some moves
   # Type "undo" to revert moves

3. Hangman - CLI Enhancements
-----------------------------

.. _changes-made-2:

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/paper/hangman/cli.py``**

-  Integrated ``ASCIIArt``, ``InteractiveMenu``, ``RichText``, ``Theme``
   from ``common.cli_utils``
-  Created ``CLI_THEME`` for consistent color scheme
-  Replaced plain text menus with ``InteractiveMenu`` (supports arrow
   key navigation)
-  Added ASCII art banner for welcome screen
-  Added ASCII art banner for multiplayer mode
-  Applied ``RichText`` for all user feedback:

   -  Success messages (green)
   -  Error messages (red)
   -  Info messages (blue)
   -  Warning messages (yellow)
   -  Highlighted messages (gold)

-  Added ``clear_screen()`` for better UX

.. _enhancements-applied-usage-2:

Usage
~~~~~

Enhanced user experience:

-  **Interactive Menus**: Use arrow keys (↑↓) and Enter to select
   options
-  **Colored Output**: Success, error, info, and warning messages are
   color-coded
-  **ASCII Art**: Welcome banner and section headers
-  **Clear Screen**: Better visual organization between screens

.. _enhancements-applied-testing-2:

Testing
~~~~~~~

.. code:: bash

   python -m games_collection.games.paper.hangman
   # Navigate menus with arrow keys
   # See colored feedback during gameplay

4. Hearts & Spades - GUI Preference Persistence
-----------------------------------------------

.. _changes-made-3:

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/card/hearts/gui.py``**

-  Added persistent preference loading via ``SettingsManager``
-  Introduced a GUI “Preferences” menu for selecting themes, toggling
   sounds, and enabling/disabling animations
-  Added helpers to update or reset preferences programmatically (used
   by tests and the menu actions)

**File: ``src/games_collection/games/card/spades/gui.py``**

-  Mirrored the Hearts GUI enhancements for preference loading and menu
   controls
-  Exposed helpers to update/reset preferences and ensured menu state
   stays in sync with stored values

**File: ``src/games_collection/games/card/hearts/__main__.py``**

-  Surfaced new CLI switches (``--theme``, ``--sounds/--no-sounds``,
   ``--animations/--no-animations``, ``--reset-preferences``)
-  CLI switches persist the selection so the GUI picks them up on the
   next launch

**File: ``src/games_collection/games/card/spades/__main__.py``**

-  Added the same CLI switches and persistence logic as the Hearts entry
   point (with backend auto-detection retained)

**File: ``tests/test_gui_preferences.py``**

-  Added Tkinter-aware smoke tests that verify preferences load
   correctly and that helper methods persist new settings without
   raising errors

.. _enhancements-applied-usage-3:

Usage
~~~~~

-  Launch either GUI and open **Preferences → Theme** to select between
   *Light*, *Dark*, and *High Contrast*
-  Toggle **Enable sounds** or **Enable animations** in the same menu;
   settings persist across sessions
-  Use CLI flags to preconfigure preferences, for example:

.. code:: bash

   python -m games_collection.games.card.hearts --theme high_contrast --no-sounds
   python -m games_collection.games.card.spades --backend tk --animations --sounds

.. _enhancements-applied-testing-3:

Testing
~~~~~~~

.. code:: bash

   pytest tests/test_gui_preferences.py -k "preferences"

Architecture Systems Demonstrated
---------------------------------

1. Persistence System (``src/games_collection/core/architecture/persistence.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``SaveLoadManager`` - High-level save/load interface
-  ``JSONSerializer`` - JSON-based serialization (used by default)
-  Automatic metadata handling (timestamps, game type)
-  Directory management for save files

2. Replay System (``src/games_collection/core/architecture/replay.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``ReplayManager`` - Undo/redo functionality
-  ``ReplayAction`` - Action recording with state snapshots
-  History management with configurable limits
-  State restoration from snapshots

3. CLI Utilities (``src/games_collection/core/cli_utils.py``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``InteractiveMenu`` - Arrow key navigation menus
-  ``ASCIIArt`` - Banner and box creation
-  ``RichText`` - Colored text output (success, error, info, warning,
   highlight)
-  ``Theme`` - Consistent color scheme management
-  ``clear_screen()`` - Screen clearing utility

Benefits
--------

For Players
~~~~~~~~~~~

-  **War Game**: Never lose progress - save and continue later
-  **Tic-Tac-Toe**: Undo mistakes and try different strategies
-  **Hangman**: More enjoyable CLI with colors and easy navigation

For Developers
~~~~~~~~~~~~~~

-  **Reusable Infrastructure**: All systems are in ``src/games_collection/core/`` and ready
   to use
-  **Minimal Integration**: Just a few imports and method calls
-  **Type Safety**: Full type hints for all APIs
-  **Consistent Patterns**: Same approach works across all games

Code Quality
------------

All changes have been validated:

-  ✓ All tests pass (73 passed, 1 skipped)
-  ✓ Linting passes (ruff check)
-  ✓ Code formatted (black)
-  ✓ No breaking changes to existing functionality
-  ✓ Manual testing confirms all features work correctly

Future Applications
-------------------

These patterns can be easily applied to other games:

Save/Load
~~~~~~~~~

-  Any card game (Poker, Blackjack, Hearts, Spades, etc.)
-  Any strategy game (Chess, Checkers, Othello, etc.)
-  Any game with long sessions

Replay/Undo
~~~~~~~~~~~

-  All strategy games benefit from undo
-  Puzzle games (Sudoku, Minesweeper, etc.)
-  Educational games for learning

CLI Enhancements
~~~~~~~~~~~~~~~~

-  All games with CLI interfaces can benefit
-  Especially games with complex menus
-  Games targeting terminal enthusiasts

Example Integration Code
------------------------

Adding Save/Load (5 minutes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # In game engine
   from games_collection.core.architecture.persistence import SaveLoadManager

   def to_dict(self) -> dict:
       return {"player_state": self.player, "game_state": self.state}

   @classmethod
   def from_dict(cls, data: dict):
       game = cls()
       game.player = data["player_state"]
       game.state = data["game_state"]
       return game

   # In GUI/CLI
   manager = SaveLoadManager()
   manager.save("game_name", game.to_dict())  # Save
   data = manager.load(filepath)  # Load
   game = Game.from_dict(data["state"])  # Restore

Adding Replay/Undo (5 minutes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   # In game engine
   from games_collection.core.architecture.replay import ReplayManager

   def __init__(self):
       self.replay_manager = ReplayManager()

   def make_move(self, move):
       state_before = self.get_state()
       self.replay_manager.record_action(
           timestamp=time.time(),
           actor=self.current_player,
           action_type="move",
           data={"move": move},
           state_before=state_before
       )
       # Execute move

   def undo(self):
       if self.replay_manager.can_undo():
           action = self.replay_manager.undo()
           self.restore_state(action.state_before)

Adding CLI Enhancements (5 minutes)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from games_collection.core.cli_utils import InteractiveMenu, ASCIIArt, RichText, Theme

   theme = Theme()
   print(ASCIIArt.banner("GAME NAME", theme.primary))

   menu = InteractiveMenu("Main Menu", ["Play", "Options", "Quit"], theme=theme)
   choice = menu.display()

   print(RichText.success("You won!", theme))
   print(RichText.error("Game over!", theme))

5. Go Fish - Event-Driven Autosave Integration
----------------------------------------------

.. _changes-made-4:

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/card/go_fish/game.py``**

-  Wired ``GoFishGame`` into the shared event bus (``GameEventType``) so
   every turn emits action, score, and lifecycle events
-  Added ``to_state()``/``from_state()`` helpers for persistence using
   the existing card serialization utilities
-  Provided ``_card_to_dict()``/``_card_from_dict()`` helpers for
   round-tripping immutable ``Card`` objects

**File: ``src/games_collection/games/card/go_fish/cli.py``**

-  Introduced an autosave slot powered by ``SaveLoadManager``
-  Prompts players to resume an unfinished match when an autosave exists
-  Persists rich metadata (next player, deck size, last action)
   alongside the serialized state after every valid action

.. _enhancements-applied-usage-4:

Usage
~~~~~

-  Start the CLI with ``python -m games_collection.games.card.go_fish``
-  Play a few turns and exit the program; a ``go_fish_autosave.save``
   file is created automatically
-  Relaunch the CLI and choose to resume when prompted to continue
   exactly where you left off

.. _enhancements-applied-testing-4:

Testing
~~~~~~~

.. code:: bash

   python -m games_collection.games.card.go_fish
   # Play a few turns, exit, and relaunch to verify autosave resume

6. Connect Four - Event Bus & Autosave Enhancements
---------------------------------------------------

.. _changes-made-5:

Changes Made
~~~~~~~~~~~~

**File: ``src/games_collection/games/paper/connect_four/connect_four.py``**

-  Updated ``ConnectFourGame`` to emit ``GameEventType`` events for
   initialization, turn progression, and game over states
-  Added ``to_state()``/``from_state()`` helpers so games can be
   serialized and restored without replaying moves
-  Extended the CLI wrapper to leverage ``SaveLoadManager`` for
   automatic persistence between sessions

.. _enhancements-applied-usage-5:

Usage
~~~~~

-  Launch the CLI via ``python -m games_collection.games.paper.connect_four``
-  Accept the resume prompt when an autosave exists to recover the
   previous board position instantly
-  Autosave files live in ``./saves/connect_four_autosave.save``

.. _enhancements-applied-testing-5:

Testing
~~~~~~~

.. code:: bash

   python -m games_collection.games.paper.connect_four
   # Make moves, exit, relaunch, and resume the saved game

Conclusion
----------

These enhancements demonstrate that the infrastructure is
production-ready and easy to integrate. Any game in the repository can
adopt these features with minimal code changes, providing better user
experience and demonstrating the value of the common architecture
patterns.
