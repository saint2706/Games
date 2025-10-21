Status Tracking Documentation
=============================

This directory contains status tracking documents for ongoing
migrations, implementations, and projects in the Games repository.

Current Status Files
--------------------

- ``operations/status/gui_migration_status`` – Tracks progress for the tkinter → PyQt5 migration across all games.
  - Total games: 16, Completed: 16, Remaining: 0
  - Categories: Paper Games (2/2 completed), Card Games (14/14 completed)
  - Includes a full game-by-game breakdown in the referenced document.

Purpose
-------

Status tracking documents serve to:

-  Monitor progress of long-running migrations
-  Identify next priorities
-  Track completion percentages
-  Document migration decisions
-  Guide contributors

Adding Status Documents
-----------------------

When starting a new migration or major implementation:

1. Create a new status document in this directory
2. Include clear tracking metrics (completed, remaining, etc.)
3. Update regularly as work progresses
4. Link from the main docs/README.md
5. Archive or move to historical section when complete

Related Documentation
---------------------

-  `GUI Documentation <../gui/>`__ - GUI framework documentation
-  `Development Documentation <../development/>`__ - Development guides
-  `Architecture Documentation <../architecture/>`__ - Architecture
   patterns
-  `Planning Documentation <../planning/>`__ - Future roadmap
