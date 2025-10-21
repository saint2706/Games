GUI Framework Support
=====================

The Games repository supports multiple GUI frameworks to ensure
compatibility across different environments and platforms.

Available Frameworks
--------------------

PyQt5 (Recommended)
~~~~~~~~~~~~~~~~~~~

**Status**: Primary framework for new GUIs

PyQt5 is the recommended GUI framework for the Games repository because:

-  ✅ Works in headless CI/CD environments
-  ✅ Better cross-platform support (Linux, Windows, macOS)
-  ✅ More robust and feature-rich
-  ✅ Professional appearance with modern widgets
-  ✅ Extensive documentation and community support

**Installation:**

.. code:: bash

   pip install games-collection[gui]
   # or
   pip install pyqt5

**Available Games:** All 16 games with GUI support have been migrated to
PyQt5.

**Paper Games:**

-  Battleship (``src/games_collection/games/paper/battleship/gui_pyqt.py``)
-  Dots and Boxes (``src/games_collection/games/paper/dots_and_boxes/gui_pyqt.py``)

**Card Games:**

-  Blackjack (``src/games_collection/games/card/blackjack/gui_pyqt.py``)
-  Bluff (``src/games_collection/games/card/bluff/gui_pyqt.py``)
-  Bridge (``src/games_collection/games/card/bridge/gui_pyqt.py``)
-  Canasta (``src/games_collection/games/card/canasta/gui_pyqt.py``)
-  Crazy Eights (``src/games_collection/games/card/crazy_eights/gui_pyqt.py``)
-  Gin Rummy (``src/games_collection/games/card/gin_rummy/gui_pyqt.py``)
-  Go Fish (``src/games_collection/games/card/go_fish/gui_pyqt.py``)
-  Hearts (``src/games_collection/games/card/hearts/gui_pyqt.py``)
-  Pinochle (``src/games_collection/games/card/pinochle/gui_pyqt.py``)
-  Poker (``src/games_collection/games/card/poker/gui_pyqt.py``)
-  Solitaire (``src/games_collection/games/card/solitaire/gui_pyqt.py``)
-  Spades (``src/games_collection/games/card/spades/gui_pyqt.py``)
-  Uno (``src/games_collection/games/card/uno/gui_pyqt.py``)
-  War (``src/games_collection/games/card/war/gui_pyqt.py``)

Tkinter (Legacy)
~~~~~~~~~~~~~~~~

**Status**: Legacy framework, still supported as fallback

Tkinter is the original GUI framework used in this repository. It
remains available as a fallback option since it’s included in Python’s
standard library. However, it has some limitations:

-  ❌ Not available in all Python installations
-  ❌ Requires X11 display server (problematic in CI/CD)
-  ❌ Less consistent cross-platform behavior
-  ❌ Limited widget set

Most games maintain both Tkinter (``gui.py``) and PyQt5
(``gui_pyqt.py``) implementations for backward compatibility.

Migration Status
----------------

🎉 **Migration Complete!** All games with GUI support have been
successfully migrated to PyQt5.

**For detailed migration information, see**
operations/status/gui_migration_status (operations/status/gui_migration_status)\ **.**

For migration guidelines and best practices, see ``developers/gui/migration_guide``.

Summary
~~~~~~~

============ ===== ==========
Status       Count Percentage
============ ===== ==========
✅ Completed 16/16 100%
============ ===== ==========

All 16 games (2 paper games, 14 card games) now have PyQt5
implementations with feature parity to their Tkinter versions.

Using GUIs
----------

Running a Game with GUI
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   # Using module syntax (recommended)
   python -m games_collection.games.paper.dots_and_boxes --gui

   # Using entry point (if installed via pip)
   games-dots-and-boxes --gui

Checking Framework Availability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the provided utility script:

.. code:: bash

   # Check what frameworks are available
   python scripts/test_gui.py --check-framework all

   # List all games and their GUI support
   python scripts/test_gui.py --list

   # Check specific game
   python scripts/test_gui.py --check-game src/games_collection/games/paper/dots_and_boxes --framework pyqt5

For Developers
--------------

Creating a New GUI
~~~~~~~~~~~~~~~~~~

When creating a new game GUI, use PyQt5:

.. code:: python

   from PyQt5.QtWidgets import QApplication, QWidget
   import sys

   class MyGameGUI(QWidget):
       def __init__(self):
           super().__init__()
           self.setWindowTitle("My Game")
           # Build your GUI here

   def run_gui():
       app = QApplication.instance() or QApplication(sys.argv)
       window = MyGameGUI()
       window.show()
       app.exec()

   if __name__ == "__main__":
       run_gui()

Using BaseGUI
~~~~~~~~~~~~~

For consistency, use the BaseGUI class:

.. code:: python

   from games_collection.core.gui_base_pyqt import BaseGUI, GUIConfig

   class MyGameGUI(BaseGUI):
       def __init__(self):
           config = GUIConfig(
               window_title="My Game",
               window_width=800,
               window_height=600,
           )
           super().__init__(config=config)
           self.build_layout()

       def build_layout(self):
           # Implement your layout
           pass

       def update_display(self):
           # Update UI based on game state
           pass

Testing GUIs
~~~~~~~~~~~~

.. code:: python

   import pytest

   @pytest.mark.gui
   class TestMyGamePyQt:
       def test_import(self):
           from my_game.gui_pyqt import MyGameGUI
           assert MyGameGUI is not None

       @pytest.mark.skipif(not has_display(), reason="Requires display")
       def test_initialization(self, qtbot):
           from my_game.gui_pyqt import MyGameGUI

           window = MyGameGUI()
           qtbot.addWidget(window)
           assert window is not None

FAQ
---

Q: Why not use Pygame?
~~~~~~~~~~~~~~~~~~~~~~

Pygame is better suited for games with real-time graphics and
animations. Most games in this repository are turn-based and benefit
more from traditional widget-based GUIs that PyQt5 provides. However,
Pygame is still available as an optional dependency for games that need
it (like Uno’s sound effects).

Q: Can I still use tkinter?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, tkinter GUIs are still available for games that haven’t been
migrated yet. However, they may not work in all environments (especially
CI/CD systems and headless servers).

Q: How do I migrate my game from tkinter to PyQt5?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See ``developers/gui/migration_guide`` for a comprehensive guide with examples.

Q: What about web-based GUIs?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Web-based GUIs are out of scope for this project, which focuses on
desktop applications. However, the game engines are designed to be
UI-agnostic, so you could create web frontends using Flask or similar
frameworks.

Resources
---------

-  `PyQt5
   Documentation <https://www.riverbankcomputing.com/static/Docs/PyQt5/>`__
-  `Qt Documentation <https://doc.qt.io/qt-5/>`__
-  Migration Guide (developers/gui/migration_guide)
-  `Test Utility <../../scripts/test_gui.py>`__
