CLI Utilities Documentation
===========================

The ``common.cli_utils`` module provides enhanced command-line interface
utilities for terminal-based games, including colorful ASCII art, rich
text formatting, progress indicators, interactive menus, command
history, and theme support.

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Features <#features>`__
-  `Quick Start <#quick-start>`__
-  `API Reference <#api-reference>`__

   -  `Colors and Themes <#colors-and-themes>`__
   -  `ASCII Art <#ascii-art>`__
   -  `Rich Text Formatting <#rich-text-formatting>`__
   -  `Progress Indicators <#progress-indicators>`__
   -  `Interactive Menus <#interactive-menus>`__
   -  `Command History <#command-history>`__
   -  `Utility Functions <#utility-functions>`__

-  `Examples <#examples>`__
-  `Best Practices <#best-practices>`__

Installation
------------

The CLI utilities are part of the common module and have no additional
dependencies beyond what’s already required for the project.

.. code:: python

   from games_collection.core.cli_utils import (
       ASCIIArt,
       Color,
       CommandHistory,
       InteractiveMenu,
       ProgressBar,
       RichText,
       Spinner,
       THEMES,
       Theme,
       clear_screen,
       get_terminal_size,
   )

Features
--------

✅ Colorful ASCII Art for Game States
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Victory, defeat, and draw ASCII art
-  Customizable banners and boxes
-  Multiple color options

✅ Rich Text Formatting with Visual Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Headers at multiple levels
-  Success, error, warning, and info messages
-  Text highlighting and colorization
-  Style attributes (bright, dim)

✅ Progress Bars and Spinners for Loading States
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Customizable progress bars
-  Animated spinners
-  Theme support

✅ Interactive Command-Line Menus with Arrow Key Navigation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Arrow key navigation (platform-specific)
-  Numbered fallback menu
-  Customizable themes

✅ Command History and Autocomplete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Command history with navigation
-  Search functionality
-  Autocomplete support

✅ Terminal Themes and Custom Color Schemes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Predefined themes (default, dark, light, ocean, forest)
-  Custom theme creation
-  Consistent color schemes across components

Quick Start
-----------

.. code:: python

   from games_collection.core.cli_utils import ASCIIArt, RichText, ProgressBar, InteractiveMenu, Color

   # Display a banner
   print(ASCIIArt.banner("My Game", Color.CYAN))

   # Show formatted messages
   print(RichText.success("Game started successfully!"))
   print(RichText.error("Connection failed!"))

   # Create a progress bar
   bar = ProgressBar(total=100)
   for i in range(101):
       bar.update(i)
       # ... do work ...

   # Display an interactive menu
   menu = InteractiveMenu("Main Menu", ["Play", "Options", "Quit"])
   choice = menu.display()
   print(f"Selected: {menu.options[choice]}")

API Reference
-------------

Colors and Themes
~~~~~~~~~~~~~~~~~

Color Enum
^^^^^^^^^^

Available colors:

-  ``Color.BLACK``
-  ``Color.RED``
-  ``Color.GREEN``
-  ``Color.YELLOW``
-  ``Color.BLUE``
-  ``Color.MAGENTA``
-  ``Color.CYAN``
-  ``Color.WHITE``
-  ``Color.RESET``

TextStyle Enum
^^^^^^^^^^^^^^

Available styles:

-  ``TextStyle.RESET``
-  ``TextStyle.BRIGHT``
-  ``TextStyle.DIM``
-  ``TextStyle.NORMAL``

Theme Class
^^^^^^^^^^^

.. code:: python

   @dataclass
   class Theme:
       primary: Color = Color.CYAN
       secondary: Color = Color.YELLOW
       success: Color = Color.GREEN
       error: Color = Color.RED
       warning: Color = Color.YELLOW
       info: Color = Color.BLUE
       text: Color = Color.WHITE
       accent: Color = Color.MAGENTA

Predefined Themes
^^^^^^^^^^^^^^^^^

.. code:: python

   THEMES = {
       "default": Theme(...),
       "dark": Theme(...),
       "light": Theme(...),
       "ocean": Theme(...),
       "forest": Theme(...),
   }

ASCII Art
~~~~~~~~~

ASCIIArt Class
^^^^^^^^^^^^^^

Static methods for creating ASCII art:

banner(text, color, width)
''''''''''''''''''''''''''

.. code:: python

   ASCIIArt.banner(
       text: str,
       color: Color = Color.CYAN,
       width: int = 60
   ) -> str

Creates a banner with the given text.

**Example:**

.. code:: python

   print(ASCIIArt.banner("Welcome!", Color.GREEN, width=40))

box(text, color, padding)
'''''''''''''''''''''''''

.. code:: python

   ASCIIArt.box(
       text: str,
       color: Color = Color.WHITE,
       padding: int = 1
   ) -> str

Creates a box around text.

**Example:**

.. code:: python

   print(ASCIIArt.box("Important\nMessage", Color.YELLOW))

victory(color)
''''''''''''''

.. code:: python

   ASCIIArt.victory(color: Color = Color.YELLOW) -> str

Returns victory ASCII art.

defeat(color)
'''''''''''''

.. code:: python

   ASCIIArt.defeat(color: Color = Color.RED) -> str

Returns defeat ASCII art.

draw(color)
'''''''''''

.. code:: python

   ASCIIArt.draw(color: Color = Color.CYAN) -> str

Returns draw/tie ASCII art.

Rich Text Formatting
~~~~~~~~~~~~~~~~~~~~

RichText Class
^^^^^^^^^^^^^^

Static methods for text formatting:

colorize(text, color, style)
''''''''''''''''''''''''''''

.. code:: python

   RichText.colorize(
       text: str,
       color: Color,
       style: Optional[TextStyle] = None
   ) -> str

Colorize text with optional style.

**Example:**

.. code:: python

   print(RichText.colorize("Important", Color.RED, TextStyle.BRIGHT))

header(text, level, theme)
''''''''''''''''''''''''''

.. code:: python

   RichText.header(
       text: str,
       level: int = 1,
       theme: Theme = THEMES["default"]
   ) -> str

Format text as a header (levels 1-3).

**Example:**

.. code:: python

   print(RichText.header("Main Title", level=1))
   print(RichText.header("Subtitle", level=2))

highlight(text, theme)
''''''''''''''''''''''

.. code:: python

   RichText.highlight(
       text: str,
       theme: Theme = THEMES["default"]
   ) -> str

Highlight important text.

success(text, theme)
''''''''''''''''''''

.. code:: python

   RichText.success(
       text: str,
       theme: Theme = THEMES["default"]
   ) -> str

Format success message with checkmark.

error(text, theme)
''''''''''''''''''

.. code:: python

   RichText.error(
       text: str,
       theme: Theme = THEMES["default"]
   ) -> str

Format error message with X mark.

warning(text, theme)
''''''''''''''''''''

.. code:: python

   RichText.warning(
       text: str,
       theme: Theme = THEMES["default"]
   ) -> str

Format warning message with warning symbol.

info(text, theme)
'''''''''''''''''

.. code:: python

   RichText.info(
       text: str,
       theme: Theme = THEMES["default"]
   ) -> str

Format info message with info symbol.

Progress Indicators
~~~~~~~~~~~~~~~~~~~

ProgressBar Class
^^^^^^^^^^^^^^^^^

.. code:: python

   class ProgressBar:
       def __init__(
           self,
           total: int,
           width: int = 40,
           theme: Theme = THEMES["default"]
       ):
           """Initialize progress bar."""

       def update(self, current: Optional[int] = None) -> None:
           """Update progress (increment or set to specific value)."""

       def complete(self) -> None:
           """Mark progress as complete."""

**Example:**

.. code:: python

   bar = ProgressBar(total=100, width=50)
   for i in range(101):
       bar.update(i)
       time.sleep(0.01)

Spinner Class
^^^^^^^^^^^^^

.. code:: python

   class Spinner:
       def __init__(
           self,
           message: str = "Loading",
           theme: Theme = THEMES["default"]
       ):
           """Initialize spinner."""

       def start(self) -> None:
           """Start the spinner."""

       def tick(self) -> None:
           """Advance to next frame."""

       def stop(self) -> None:
           """Stop the spinner."""

**Example:**

.. code:: python

   spinner = Spinner(message="Loading assets")
   spinner.start()
   for _ in range(10):
       time.sleep(0.1)
       spinner.tick()
   spinner.stop()

Interactive Menus
~~~~~~~~~~~~~~~~~

InteractiveMenu Class
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   class InteractiveMenu:
       def __init__(
           self,
           title: str,
           options: list[str],
           theme: Theme = THEMES["default"]
       ):
           """Initialize interactive menu."""

       def display(self, allow_arrow_keys: bool = True) -> int:
           """Display menu and get user selection."""

**Example:**

.. code:: python

   menu = InteractiveMenu(
       "Game Menu",
       ["New Game", "Continue", "Options", "Quit"]
   )
   choice = menu.display()
   print(f"You selected: {menu.options[choice]}")

**Notes:**

-  Arrow key navigation works on most terminals
-  Automatically falls back to numbered menu if arrow keys are
   unavailable
-  Returns the index of the selected option

Command History
~~~~~~~~~~~~~~~

CommandHistory Class
^^^^^^^^^^^^^^^^^^^^

.. code:: python

   class CommandHistory:
       def __init__(self, max_size: int = 100):
           """Initialize command history."""

       def add(self, command: str) -> None:
           """Add command to history."""

       def previous(self) -> Optional[str]:
           """Get previous command."""

       def next(self) -> Optional[str]:
           """Get next command."""

       def search(self, prefix: str) -> list[str]:
           """Search for commands matching prefix."""

       def autocomplete(
           self,
           partial: str,
           candidates: Iterable[str]
       ) -> Optional[str]:
           """Autocomplete partial command."""

**Example:**

.. code:: python

   history = CommandHistory()

   # Add commands
   history.add("play game")
   history.add("save state")

   # Navigate
   prev = history.previous()
   next_cmd = history.next()

   # Search
   results = history.search("play")

   # Autocomplete
   commands = ["play", "pause", "stop", "save", "load"]
   completed = history.autocomplete("pla", commands)

Utility Functions
~~~~~~~~~~~~~~~~~

clear_screen()
^^^^^^^^^^^^^^

.. code:: python

   def clear_screen() -> None:
       """Clear the terminal screen."""

**Example:**

.. code:: python

   clear_screen()

get_terminal_size()
^^^^^^^^^^^^^^^^^^^

.. code:: python

   def get_terminal_size() -> tuple[int, int]:
       """Get terminal size as (width, height)."""

**Example:**

.. code:: python

   width, height = get_terminal_size()
   print(f"Terminal: {width}x{height}")

Examples
--------

Complete Game Menu Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from games_collection.core.cli_utils import (
       ASCIIArt,
       Color,
       InteractiveMenu,
       ProgressBar,
       RichText,
       THEMES,
       clear_screen,
   )
   import time

   def main():
       # Show welcome banner
       print(ASCIIArt.banner("My Awesome Game", Color.CYAN, width=60))
       print()

       # Display menu
       menu = InteractiveMenu(
           "Main Menu",
           ["New Game", "Load Game", "Settings", "Quit"],
           theme=THEMES["ocean"]
       )
       choice = menu.display()

       if choice == 0:  # New Game
           print(RichText.info("Starting new game..."))

           # Show loading progress
           bar = ProgressBar(total=100, width=50, theme=THEMES["ocean"])
           for i in range(101):
               bar.update(i)
               time.sleep(0.02)

           print(RichText.success("Game loaded successfully!"))

       elif choice == 3:  # Quit
           print(RichText.warning("Thanks for playing!"))

   if __name__ == "__main__":
       main()

Status Message Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from games_collection.core.cli_utils import RichText

   # Game events
   print(RichText.success("Level completed!"))
   print(RichText.error("Game over!"))
   print(RichText.warning("Low health!"))
   print(RichText.info("Checkpoint saved."))

   # With custom theme
   from games_collection.core.cli_utils import THEMES
   theme = THEMES["forest"]
   print(RichText.success("Achievement unlocked!", theme))

Custom Theme Example
~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from games_collection.core.cli_utils import Theme, Color, RichText

   # Create custom theme
   custom_theme = Theme(
       primary=Color.MAGENTA,
       secondary=Color.CYAN,
       success=Color.GREEN,
       error=Color.RED,
       warning=Color.YELLOW,
       info=Color.BLUE,
       text=Color.WHITE,
       accent=Color.MAGENTA,
   )

   # Use custom theme
   print(RichText.header("My Game", level=1, theme=custom_theme))
   print(RichText.success("Custom themed message", theme=custom_theme))

Best Practices
--------------

1. Use Consistent Themes
~~~~~~~~~~~~~~~~~~~~~~~~

Choose a theme for your game and use it consistently:

.. code:: python

   from games_collection.core.cli_utils import THEMES

   GAME_THEME = THEMES["ocean"]

   # Use throughout your game
   menu = InteractiveMenu("Menu", options, theme=GAME_THEME)
   print(RichText.success("Success!", theme=GAME_THEME))

2. Provide Fallbacks
~~~~~~~~~~~~~~~~~~~~

The menu system automatically provides fallbacks, but test your CLI on
different terminals:

.. code:: python

   # Interactive menu with fallback
   menu = InteractiveMenu("Menu", options)
   choice = menu.display(allow_arrow_keys=True)  # Falls back to numbered menu

3. Use Appropriate Status Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the right message type for different situations:

.. code:: python

   # Good practices
   print(RichText.success("Action completed"))  # For successful operations
   print(RichText.error("Invalid input"))       # For errors
   print(RichText.warning("Are you sure?"))     # For warnings
   print(RichText.info("Hint: Press H for help"))  # For information

4. Progress Feedback
~~~~~~~~~~~~~~~~~~~~

Show progress for long operations:

.. code:: python

   # For known-length operations
   bar = ProgressBar(total=total_items)
   for item in items:
       process(item)
       bar.update()

   # For unknown-length operations
   spinner = Spinner(message="Processing")
   spinner.start()
   while processing:
       spinner.tick()
       time.sleep(0.1)
   spinner.stop()

5. Command History in Interactive Games
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate command history for better user experience:

.. code:: python

   history = CommandHistory()
   commands = ["play", "pause", "stop", "help", "quit"]

   while True:
       user_input = input("> ")

       # Autocomplete
       if user_input and user_input != history.autocomplete(user_input, commands):
           completed = history.autocomplete(user_input, commands)
           if completed:
               print(f"Did you mean: {completed}?")

       history.add(user_input)

       # Process command...

Platform Compatibility
----------------------

-  **Colors**: Work on all ANSI-compatible terminals (Linux, macOS,
   Windows 10+)
-  **Arrow Key Navigation**: Works on Windows (via msvcrt) and Unix (via
   termios)
-  **Automatic Fallback**: Numbered menu when arrow keys unavailable
-  **Unicode Characters**: Used in ASCII art and status messages (✓, ✗,
   ⚠, ℹ)

Testing
-------

Run the test suite:

.. code:: bash

   pytest tests/test_cli_utils.py -v

Run the demo:

.. code:: bash

   python examples/cli_utils_demo.py

Troubleshooting
---------------

Colors Not Displaying
~~~~~~~~~~~~~~~~~~~~~

If colors don’t display correctly:

1. Ensure your terminal supports ANSI escape codes
2. On Windows, use Windows 10+ or install colorama:
   ``pip install colorama``
3. Set ``TERM`` environment variable on Unix:
   ``export TERM=xterm-256color``

Arrow Keys Not Working
~~~~~~~~~~~~~~~~~~~~~~

If arrow key navigation doesn’t work:

1. The menu will automatically fall back to numbered selection
2. On Unix, ensure terminal has proper termios support
3. On Windows, ensure you’re using a console that supports msvcrt

Unicode Characters Not Displaying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If unicode characters (✓, ✗, ⚠, ℹ) don’t display:

1. Ensure your terminal uses UTF-8 encoding
2. On Windows, use Windows Terminal or set console to UTF-8
3. The functionality works without these characters, they’re just visual
   enhancements

Contributing
------------

When adding new CLI utilities:

1. Add comprehensive tests to ``tests/test_cli_utils.py``
2. Update this documentation
3. Add examples to ``examples/cli_utils_demo.py``
4. Ensure code passes linting (black, ruff, mypy)
5. Follow existing patterns and style

License
-------

Part of the Games repository - see main repository license.
