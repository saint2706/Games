Achievement Catalogue
=====================

This document lists the achievements that are registered by the shared
achievement registry. Achievements are unlocked automatically when the
conditions below are met; progress is persisted via player profiles so
milestones carry forward between sessions.

Cross-game achievements
-----------------------

+-----------------------+-----------------------+-----------------------+
| ID                    | Name                  | Requirement           |
+=======================+=======================+=======================+
| ``first_win``         | First Victory         | Win any game for the  |
|                       |                       | first time.           |
+-----------------------+-----------------------+-----------------------+
| ``winning_streak_3``  | On a Roll             | Achieve a three game  |
|                       |                       | win streak in any     |
|                       |                       | title.                |
+-----------------------+-----------------------+-----------------------+
| ``winning_streak_5``  | Unstoppable           | Reach a five game win |
|                       |                       | streak in any title.  |
+-----------------------+-----------------------+-----------------------+
| ``games_played_10``   | Getting Started       | Play ten total games. |
+-----------------------+-----------------------+-----------------------+
| ``games_played_50``   | Dedicated Player      | Play fifty total      |
|                       |                       | games.                |
+-----------------------+-----------------------+-----------------------+
| ``games_played_100``  | Veteran               | Play one hundred      |
|                       |                       | total games.          |
+-----------------------+-----------------------+-----------------------+
| ``perfect_game``      | Perfection            | Register a perfect    |
|                       |                       | game using            |
|                       |                       | game-provided         |
|                       |                       | metadata.             |
+-----------------------+-----------------------+-----------------------+

Game specific achievements
--------------------------

+-----------------+-----------------+-----------------+-----------------+
| Game            | ID              | Name            | Requirement     |
+=================+=================+=================+=================+
| Tic-Tac-Toe     | ``tic_tac_      | Grid Graduate   | Win your first  |
|                 | toe_first_win`` |                 | Tic-Tac-Toe     |
|                 |                 |                 | game.           |
+-----------------+-----------------+-----------------+-----------------+
| Tic-Tac-Toe     | ``tic_tac       | Grid Dominator  | Reach a three   |
|                 | _toe_streak_3`` |                 | game            |
|                 |                 |                 | Tic-Tac-Toe win |
|                 |                 |                 | streak.         |
+-----------------+-----------------+-----------------+-----------------+
| Tic-Tac-Toe     | ``tic_ta        | Perfectionist   | Win a           |
|                 | c_toe_perfect`` |                 | Tic-Tac-Toe     |
|                 |                 |                 | game marked as  |
|                 |                 |                 | perfect.        |
+-----------------+-----------------+-----------------+-----------------+
| Hangman         | ``hang          | Word Wrangler   | Win your first  |
|                 | man_first_win`` |                 | Hangman game.   |
+-----------------+-----------------+-----------------+-----------------+
| Hangman         | ``han           | Noose Dodger    | Achieve a five  |
|                 | gman_streak_5`` |                 | game Hangman    |
|                 |                 |                 | win streak.     |
+-----------------+-----------------+-----------------+-----------------+
| Nim             | ``              | Pile Pioneer    | Win your first  |
|                 | nim_first_win`` |                 | Nim game.       |
+-----------------+-----------------+-----------------+-----------------+
| Nim             | ``nim_perfect`` | Mathematical    | Win a Nim game  |
|                 |                 | Maestro         | marked as       |
|                 |                 |                 | perfect.        |
+-----------------+-----------------+-----------------+-----------------+

Additional games can register new achievements by extending the registry
or using the same pattern when reporting stats through
``PlayerProfile.record_game``.
