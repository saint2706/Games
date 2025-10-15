Player Guide
============

This chapter explains how to install the Games Collection, explore the catalogue,
and launch matches. No Python knowledge is required for the basics—only a recent
Python interpreter or a packaged release.

Installation options
--------------------

1. **Install from PyPI** (recommended for most players)::

       pip install games-collection

   This installs console entry points such as ``games-blackjack`` and
   ``games-tic-tac-toe`` that start games immediately.

2. **Run from a source checkout** (handy when tracking the latest commits)::

       git clone https://github.com/saint2706/Games.git
       cd Games
       pip install -e .

   The editable installation exposes the same entry points while allowing you to
   modify the code locally.

3. **Optional GUI extras** – install PyQt5 and pygame for richer graphical
   interfaces::

       pip install games-collection[gui]

Launching a game
----------------

*From the command line*
    Every packaged game registers a console script. Example commands:

    * ``games-blackjack`` – launch the Blackjack card table
    * ``games-tic-tac-toe`` – start a quick board duel
    * ``games-farkle`` – roll the dice from your terminal

*Using Python modules*
    Prefer explicit module execution or want to inspect command-line options?
    Run games with ``python -m``::

       python -m card_games.blackjack --help
       python -m paper_games.connect_four --mode ai
       python -m dice_games.craps

GUI support
-----------

Most titles ship with a Tkinter-based GUI that can be triggered with a flag::

    python -m card_games.blackjack --gui

PyQt5 implementations are gradually rolling out. When available they can be
selected explicitly::

    python -m paper_games.dots_and_boxes --gui-framework pyqt5

Not every game features a GUI yet; consult the :doc:`games_catalog` for the
latest status.

Saving progress
---------------

Games that support persistence expose a ``--save`` flag (or prompt from within
the interface). Save files are stored in the ``~/.games_collection`` directory
by default. Load them later with ``--load`` or through the in-game menus. The
shared persistence helpers live in :mod:`common.persistence` for developers who
want to add support to new titles.

Multiplayer and AI
------------------

* **Local multiplayer** – Pass-and-play modes are available in titles such as
  Connect Four, Checkers, and Uno.
* **AI opponents** – Many games ship with multiple difficulty settings. Use the
  ``--difficulty`` option (when supported) to adjust the challenge curve. The
  AI engines typically rely on heuristics or minimax search depending on game
  complexity.

Next steps
----------

Browse the :doc:`games_catalog` for the full list of experiences or continue to
:doc:`developer_guide` if you plan to tinker with the codebase.
