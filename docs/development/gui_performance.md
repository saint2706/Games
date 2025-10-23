# PyQt GUI Performance Guidelines

This document captures the findings from auditing the PyQt update flows and
describes the new throttling utilities available to widget authors.

## Audit summary

| Module | Hot path | Previous behaviour | Updated behaviour |
| --- | --- | --- | --- |
| `core/gui_base_pyqt.py` | `BaseGUI.update_display` was invoked directly from game controllers. | Every call executed immediately and refreshed the whole layout. | Introduced `request_update_display()` to coalesce work via a single-shot `QTimer`. Regions can be marked dirty so only the required widgets repaint. |
| `games/card/hearts/gui_pyqt.py` | Passing and trick resolution spammed `update_display()` while toggling hint labels. | The scoreboard, trick arena, and status banner repainted on every call. | Calls now mark `status`/`trick`/`scoreboard` regions explicitly and `update_display()` honours `should_update_region()`. |
| `games/card/gin_rummy/gui_pyqt.py` | Draw/discard loops triggered multiple refreshes as the hand changed. | Entire table redrew after each draw, causing deadwood analysis to re-run repeatedly. | Dirty-region signals differentiate between `hand`, `scoreboard`, `status`, `discard`, `stock`, and `badges`, minimising redundant calculations. |

The remaining PyQt game UIs already benefit from throttling through
`request_update_display()`. They default to full repaints until they are
incrementally annotated.

## Using the throttling helpers

* Prefer `self.request_update_display({"status", "hand"})` over calling
  `self.update_display()` directly.
* When a change must be visible immediately (e.g., right after layout
  construction), pass `immediate=True`.
* Inside `update_display()` call `self.should_update_region("name")` before
  performing expensive work. The helper returns `True` whenever a full repaint
  was requested.
* Metadata can be attached via `self.mark_dirty("log", highlight=True)` and
  then consumed from `self.current_dirty_metadata`.

## Testing expectations

`tests/gui/test_pyqt_update_throttling.py` introduces Qt bot driven tests that
simulate bursty update requests. The assertions verify that multiple logical
regions are coalesced into a single repaint and that the timer prevents more
than a handful of frames when 10 updates are requested back-to-back. These
tests serve as a baseline for future GUIs that adopt the throttling helpers.

## Best practices

1. Group updates logically. Repaint only the sections whose state actually
   changed—hands, scoreboards, status banners, etc.
2. Defer heavy analysis (e.g., scoring calculations) until the corresponding
   region is dirty. This keeps AI-driven games responsive when opponents play
   quickly.
3. Keep accessibility hooks intact by updating focusable widgets inside
   `update_display()`. When skipping a region, ensure any assistive text that
   depends on it is still updated elsewhere.
4. Document new regions in the module docstring so other contributors know how
   to signal updates.
