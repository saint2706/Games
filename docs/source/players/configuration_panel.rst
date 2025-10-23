Managing Game Configuration
===========================

The Games Collection launcher now exposes a unified configuration panel for
popular titles. You can reach it from both the command-line interface and the
desktop launcher, and every change is persisted via the shared
``SettingsManager`` so that the next game session automatically reflects your
preferences.

How it works
------------

Each game that opts into the configuration system publishes a profile under the
``games_collection.core.configuration`` module. Profiles list the editable
fields, their default values, and any constraints (such as choice lists or data
types). When you open the configuration panel the launcher loads defaults and
any previously saved overrides, merges them, and presents the result for
editing.

Command-line workflow
---------------------

1. Launch ``games_collection.launcher`` and choose the **G. Manage game
   settings** option from the main menu.
2. Select the game you want to configure by number or slug.
3. Use the numbered options to edit fields, ``S`` to save the current values,
   or ``R`` to reset the profile to its defaults. ``B`` returns to the game
   list.

The CLI panel validates your input, ensuring integers, booleans, and choice
fields remain consistent with the profile schema.

GUI workflow
------------

When browsing the PyQt launcher, the detail pane for any supported game now
includes a **Configure settings** button. Clicking the button opens a dialog
with the same fields as the CLI panel. Widgets are tailored to the field type
— checkboxes for booleans, combo boxes for enumerated values, and spin boxes for
numeric fields. Use **Save** to persist changes or the **Reset to defaults**
button to discard all overrides.

Available profiles
------------------

The initial release provides configuration profiles for the following games:

``Blackjack``
    Adjust bankroll, minimum bet, deck count, preferred GUI framework, and
    whether the CLI should launch by default.

``Spades``
    Override the GUI backend, theme, sounds, and animations used by the desktop
    client.

``Crossword``
    Pick a crossword pack to load automatically and toggle the availability of
    the in-game hint helper.

Adding new games to the panel is straightforward: define a ``GameConfigurationProfile``
in ``games_collection.core.configuration`` with defaults and ``SettingField``
definitions. The launcher picks up the profile automatically and handles
loading, validation, and persistence without additional wiring.
