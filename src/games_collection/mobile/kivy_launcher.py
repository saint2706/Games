"""Kivy-based mobile launcher that reuses the desktop catalog and profile services."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import lru_cache, partial
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Tuple

from games_collection.catalog.registry import GameMetadata, get_all_games
from games_collection.core.profile_service import ProfileService, RecentlyPlayedEntry, get_profile_service
from games_collection.launcher import _launcher_from_entry_point

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class MobileGameEntry:
    """Descriptor for a game exposed through the mobile launcher."""

    slug: str
    title: str
    description: str
    genre: str
    entry_point: str
    launcher: Callable[[], None]

    @classmethod
    def from_metadata(cls, metadata: GameMetadata) -> "MobileGameEntry":
        """Create an entry from :class:`~games_collection.catalog.registry.GameMetadata`."""

        synopsis = metadata.synopsis or metadata.description
        factory = _launcher_from_entry_point(metadata.entry_point)
        return cls(
            slug=metadata.slug,
            title=metadata.name,
            description=synopsis,
            genre=metadata.genre,
            entry_point=metadata.entry_point,
            launcher=partial(factory, None),
        )


@dataclass(frozen=True)
class _KivyNamespace:
    """Container with the Kivy classes required by the launcher."""

    app_cls: type
    screen_manager_cls: type
    screen_cls: type
    box_layout_cls: type
    grid_layout_cls: type
    button_cls: type
    label_cls: type
    scroll_view_cls: type


@lru_cache(maxsize=1)
def _load_kivy_namespace() -> _KivyNamespace:
    """Import the Kivy widgets on demand to keep the dependency optional."""

    try:
        from kivy.app import App
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.label import Label
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.screenmanager import Screen, ScreenManager
    except Exception as exc:  # pragma: no cover - exercised in runtime environments with Kivy installed
        raise RuntimeError(
            "Kivy is required for the mobile launcher. Install the 'games-collection[mobile]' extras first."
        ) from exc

    return _KivyNamespace(
        app_cls=App,
        screen_manager_cls=ScreenManager,
        screen_cls=Screen,
        box_layout_cls=BoxLayout,
        grid_layout_cls=GridLayout,
        button_cls=Button,
        label_cls=Label,
        scroll_view_cls=ScrollView,
    )


def _collect_entries() -> Tuple[MobileGameEntry, ...]:
    """Return the games declared in the catalogue sorted by name."""

    entries: Iterable[MobileGameEntry] = (MobileGameEntry.from_metadata(metadata) for metadata in get_all_games())
    return tuple(sorted(entries, key=lambda entry: (entry.genre, entry.title.lower())))


def _prioritise_entries(profile_service: ProfileService, entries: Sequence[MobileGameEntry]) -> Tuple[MobileGameEntry, ...]:
    """Return the entries reordered to put favourites at the top."""

    favorites = set(profile_service.get_favorites())
    return tuple(sorted(entries, key=lambda entry: (entry.slug not in favorites, entry.title.lower())))


def _format_recent_entry(entry: RecentlyPlayedEntry, catalogue: Dict[str, MobileGameEntry]) -> str:
    """Return a label for a recently played entry."""

    metadata = catalogue.get(entry.game_id)
    if metadata is None:
        name = entry.game_id.replace("_", " ").title()
    else:
        name = metadata.title
    timestamp = entry.last_played or "Unknown time"
    return f"{name} — {timestamp}"


def _favorite_label(is_favorite: bool) -> str:
    """Return the label displayed on the favourite toggle button."""

    return "★ Favourite" if is_favorite else "☆ Add Favourite"


def build_mobile_launcher_app(profile_service: Optional[ProfileService] = None) -> Any:
    """Return a configured Kivy :class:`~kivy.app.App` instance for mobile devices."""

    modules = _load_kivy_namespace()
    service = profile_service or get_profile_service()
    ordered_entries = _prioritise_entries(service, _collect_entries())
    catalogue = {entry.slug: entry for entry in ordered_entries}

    class MobileLauncherApp(modules.app_cls):  # type: ignore[misc]
        """Concrete application subclass bound to the dynamically imported Kivy base class."""

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self.profile_service = service
            self._modules = modules
            self._entries: Tuple[MobileGameEntry, ...] = ordered_entries
            self._catalogue = catalogue
            self._recent_container: Optional[Any] = None
            self._status_label: Optional[Any] = None

        def build(self) -> Any:  # pragma: no cover - UI composition exercised manually
            """Create the screen manager hosting the primary menu."""

            manager = self._modules.screen_manager_cls()
            screen = self._modules.screen_cls(name="menu")
            screen.add_widget(self._build_menu())
            manager.add_widget(screen)
            return manager

        def _build_menu(self) -> Any:
            """Assemble the touch-friendly menu layout."""

            layout = self._modules.box_layout_cls(orientation="vertical", padding=24, spacing=16)
            header = self._modules.label_cls(
                text=f"[b]{self._profile_banner()}[/b]",
                size_hint_y=None,
                height=48,
                markup=True,
            )
            layout.add_widget(header)

            scroll = self._modules.scroll_view_cls()
            grid = self._modules.grid_layout_cls(cols=1, spacing=12, size_hint_y=None, padding=(0, 0, 0, 24))
            grid.bind(minimum_height=grid.setter("height"))

            recent_wrapper = self._modules.grid_layout_cls(cols=1, spacing=8, size_hint_y=None, padding=(0, 0, 0, 16))
            recent_wrapper.bind(minimum_height=recent_wrapper.setter("height"))
            self._recent_container = recent_wrapper
            self._populate_recent(recent_wrapper)
            grid.add_widget(recent_wrapper)

            grid.add_widget(
                self._modules.label_cls(text="[b]All Games[/b]", size_hint_y=None, height=32, markup=True)
            )
            for entry in self._entries:
                grid.add_widget(self._build_entry_card(entry))

            scroll.add_widget(grid)
            layout.add_widget(scroll)

            status = self._modules.label_cls(text="Tap a game to launch", size_hint_y=None, height=40)
            self._status_label = status
            layout.add_widget(status)
            return layout

        def _profile_banner(self) -> str:
            """Return the formatted profile summary banner."""

            profile = self.profile_service.active_profile
            return f"{profile.display_name} — Level {profile.level} • {profile.experience} XP"

        def _populate_recent(self, container: Any) -> None:
            """Fill the recent section with shortcuts for the last played games."""

            container.clear_widgets()
            container.add_widget(
                self._modules.label_cls(text="[b]Recently Played[/b]", size_hint_y=None, height=32, markup=True)
            )
            entries = self.profile_service.get_recently_played(limit=5)
            if not entries:
                container.add_widget(
                    self._modules.label_cls(text="Play a game to build recent history.", size_hint_y=None, height=32)
                )
                return
            for entry in entries:
                label = _format_recent_entry(entry, self._catalogue)
                button = self._modules.button_cls(text=label, size_hint_y=None, height=56)
                button.bind(on_release=lambda _btn, slug=entry.game_id: self._launch_from_recent(slug))
                container.add_widget(button)

        def _build_entry_card(self, entry: MobileGameEntry) -> Any:
            """Return the widget tree describing a single game entry."""

            card = self._modules.box_layout_cls(orientation="vertical", padding=16, spacing=8, size_hint_y=None)
            card.height = 180

            header = self._modules.box_layout_cls(orientation="horizontal", spacing=12, size_hint_y=None, height=64)
            play_button = self._modules.button_cls(text=f"▶ {entry.title}", size_hint=(0.7, None), height=64, font_size="20sp")
            play_button.bind(on_release=lambda _btn, slug=entry.slug: self.launch_game(slug))
            favorite_button = self._modules.button_cls(
                text=_favorite_label(self.profile_service.is_favorite(entry.slug)),
                size_hint=(0.3, None),
                height=64,
            )
            favorite_button.bind(on_release=lambda btn, slug=entry.slug: self._toggle_favorite(slug, btn))
            header.add_widget(play_button)
            header.add_widget(favorite_button)
            card.add_widget(header)

            description = self._modules.label_cls(
                text=f"{entry.genre.title()} • {entry.description}",
                halign="left",
                valign="top",
                size_hint_y=None,
            )
            description.bind(width=lambda instance, value: setattr(instance, "text_size", (value, None)))
            description.bind(texture_size=lambda instance, value: setattr(instance, "height", max(72, value[1] + 12)))
            card.add_widget(description)
            return card

        def _toggle_favorite(self, slug: str, button: Any) -> None:
            """Toggle the favourite state for ``slug`` and update the UI label."""

            new_state = self.profile_service.toggle_favorite(slug)
            button.text = _favorite_label(new_state)
            if self._status_label is not None:
                state = "added to" if new_state else "removed from"
                entry = self._catalogue.get(slug)
                title = entry.title if entry is not None else slug.replace("_", " ").title()
                self._status_label.text = f"{title} {state} favourites"

        def launch_game(self, slug: str) -> None:
            """Launch the selected game and refresh auxiliary sections."""

            entry = self._catalogue.get(slug)
            if entry is None:
                if self._status_label is not None:
                    self._status_label.text = f"Unknown game identifier: {slug}"
                return
            try:
                entry.launcher()
            except Exception as exc:  # pragma: no cover - game launch relies on interactive UI
                LOGGER.exception("Failed to launch game: %s", slug)
                if self._status_label is not None:
                    self._status_label.text = f"Launch failed: {exc}"[:120]
                return
            if self._status_label is not None:
                self._status_label.text = f"Launching {entry.title}..."
            if self._recent_container is not None:
                self._populate_recent(self._recent_container)

        def _launch_from_recent(self, slug: str) -> None:
            """Helper used by recent shortcuts to delegate to :meth:`launch_game`."""

            self.launch_game(slug)

    return MobileLauncherApp()


def launch_mobile_launcher(profile_service: Optional[ProfileService] = None) -> None:
    """Execute the Kivy application and block until the user exits."""

    app = build_mobile_launcher_app(profile_service=profile_service)
    app.run()


def main() -> Any:
    """Entry point used by build tools such as Briefcase."""

    return build_mobile_launcher_app()


__all__ = ["MobileGameEntry", "build_mobile_launcher_app", "launch_mobile_launcher", "main"]
