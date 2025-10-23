# Launcher Asset Workflow

The desktop launcher now surfaces rich previews for every bundled game. Contributors can attach screenshots and thumbnails that
the GUI detail pane and CLI metadata preview reference. Follow the steps below whenever you add a new title or refresh artwork.

## 1. Prepare the assets

* Store images inside `src/games_collection/assets/launcher/`.
* Use `PNG` files sized to 16:9 where possible (the default preview scales a 320×180 screenshot and a 160×90 thumbnail).
* Keep filenames descriptive—`<slug>_screenshot.png` and `<slug>_thumbnail.png` help identify assets later.
* Optimise images before committing; target files smaller than 250 KB to keep wheel sizes modest.

## 2. Reference assets from the registry

Update the entry in `src/games_collection/catalog/registry.json`:

```json
{
  "slug": "new_game",
  "name": "New Game",
  "description": "Short summary for menus.",
  "screenshot_path": "assets/launcher/new_game_screenshot.png",
  "thumbnail_path": "assets/launcher/new_game_thumbnail.png",
  "synopsis": "Longer marketing-style description shown in the detail pane."
}
```

The `screenshot_path` and `thumbnail_path` values are resolved relative to the `games_collection` package root. The loader keeps
fields optional, but providing both ensures the GUI and CLI previews render helpful information.

## 3. Refresh synopsis copy (optional)

Synopses can be edited by hand. A concise first sentence keeps catalogue cards readable, while subsequent sentences can expand on
mechanics, player count, or theme so the CLI preview reads naturally. If you prefer to script the update, a short Python snippet
like the one below can generate boilerplate for you:

```bash
python - <<'PY'
import json
from pathlib import Path

path = Path("src/games_collection/catalog/registry.json")
data = json.loads(path.read_text())
for entry in data["games"]:
    if entry["slug"] == "new_game":
        entry["synopsis"] = (
            f"{entry['description'].rstrip('.')}. {entry['name']} is a polished {entry['genre']} experience "
            "that highlights cooperative play and features card-drafting mechanics."
        )
path.write_text(json.dumps(data, indent=2) + "\n")
PY
```

## 4. Validate locally

1. Run `pytest tests/test_catalog_registry.py` to confirm metadata loading continues to succeed.
2. Launch the GUI with `python -m games_collection.launcher --ui gui` and select the new game to verify the detail pane.
3. From the CLI launcher, run `INFO <slug>` to ensure the textual preview lists the screenshot paths and tags you expect.

Keeping this workflow in mind helps the catalogue stay visually rich and reduces merge conflicts in the registry file.
