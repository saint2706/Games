"""Desktop launcher built on PyQt5 for browsing the Games catalogue."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from games_collection.catalog.registry import GameMetadata, get_all_games
from games_collection.core.daily_challenges import DailyChallengeScheduler
from games_collection.core.gui_frameworks import Framework, launch_preferred_gui
from games_collection.core.profile_service import ProfileService
from games_collection.core.leaderboard_service import CrossGameLeaderboardEntry
from games_collection.core.recommendation_service import RecommendationResult
from games_collection.launcher import GENRE_ORDER, build_launcher_snapshot

from games_collection.core.gui_base_pyqt import BaseGUI, GUIConfig, PYQT5_AVAILABLE

if PYQT5_AVAILABLE:  # pragma: no cover - exercised via smoke tests
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QListWidgetItem,
        QMainWindow,
        QPushButton,
        QScrollArea,
        QTableWidget,
        QTableWidgetItem,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
    )
else:  # pragma: no cover - exercised when GUI extras missing
    QApplication = None  # type: ignore[assignment]
    QFormLayout = None  # type: ignore[assignment]
    QGroupBox = None  # type: ignore[assignment]
    QHBoxLayout = None  # type: ignore[assignment]
    QLabel = None  # type: ignore[assignment]
    QListWidget = None  # type: ignore[assignment]
    QListWidgetItem = None  # type: ignore[assignment]
    QMainWindow = None  # type: ignore[assignment]
    QPushButton = None  # type: ignore[assignment]
    QScrollArea = None  # type: ignore[assignment]
    QTableWidget = None  # type: ignore[assignment]
    QTableWidgetItem = None  # type: ignore[assignment]
    QTreeWidget = None  # type: ignore[assignment]
    QTreeWidgetItem = None  # type: ignore[assignment]
    QVBoxLayout = None  # type: ignore[assignment]
    QWidget = None  # type: ignore[assignment]


_CATEGORY_LABELS: Dict[str, str] = {
    "card": "Card Games",
    "paper": "Paper Games",
    "dice": "Dice Games",
    "logic": "Logic Games",
    "word": "Word Games",
}


@dataclass(frozen=True)
class CatalogueGroup:
    """Convenience container describing grouped catalogue entries."""

    title: str
    entries: Tuple[GameMetadata, ...]


def _sorted_catalogue() -> Tuple[GameMetadata, ...]:
    """Return catalogue metadata sorted to mirror the CLI layout."""

    return tuple(
        sorted(
            get_all_games(),
            key=lambda metadata: (GENRE_ORDER.get(metadata.genre, 100), metadata.name.lower()),
        )
    )


def _group_catalogue(metadata: Sequence[GameMetadata]) -> Tuple[CatalogueGroup, ...]:
    """Bucket metadata by category label while preserving ordering."""

    grouped: Dict[str, List[GameMetadata]] = {}
    for entry in metadata:
        label = _CATEGORY_LABELS.get(entry.genre, entry.genre.title())
        grouped.setdefault(label, []).append(entry)

    ordered: List[Tuple[int, str, Tuple[GameMetadata, ...]]] = []
    for label, games in grouped.items():
        games.sort(key=lambda item: item.name.lower())
        rank = GENRE_ORDER.get(games[0].genre, 100) if games else 100
        ordered.append((rank, label, tuple(games)))

    ordered.sort(key=lambda item: (item[0], item[1]))
    return tuple(CatalogueGroup(title=label, entries=entries) for _, label, entries in ordered)


if PYQT5_AVAILABLE:  # pragma: no cover - logic validated through smoke interfaces

    class LauncherWindow(QMainWindow, BaseGUI):
        """PyQt5 window presenting launcher insights and catalogue browsing."""

        def __init__(self, profile_service: ProfileService, scheduler: DailyChallengeScheduler) -> None:
            self._profile_service = profile_service
            self._scheduler = scheduler
            self._catalogue = _sorted_catalogue()
            self._catalogue_index = {metadata.slug: metadata for metadata in self._catalogue}

            QMainWindow.__init__(self)
            config = GUIConfig(
                window_title="Games Collection Launcher",
                window_width=1100,
                window_height=780,
                enable_sounds=False,
                enable_animations=False,
                log_height=0,
                log_width=0,
                theme_name="midnight",
            )
            BaseGUI.__init__(self, root=self, config=config)

            self._build_layout()
            self.refresh_contents()

        def _build_layout(self) -> None:
            """Construct the window widgets."""

            container = QWidget()
            container_layout = QVBoxLayout()
            container_layout.setContentsMargins(18, 18, 18, 18)
            container_layout.setSpacing(14)
            container.setLayout(container_layout)
            self.setCentralWidget(container)

            header_layout = QHBoxLayout()
            title_label = QLabel("Games Collection Launcher")
            title_label.setObjectName("launcherTitle")
            title_label.setStyleSheet("font-size: 22px; font-weight: 600;")
            header_layout.addWidget(title_label)
            header_layout.addStretch(1)

            self._refresh_button = QPushButton("Refresh data")
            self._refresh_button.clicked.connect(self.refresh_contents)  # type: ignore[arg-type]
            header_layout.addWidget(self._refresh_button)
            container_layout.addLayout(header_layout)

            self._profile_group = self._build_profile_group()
            container_layout.addWidget(self._profile_group)

            self._daily_group = self._build_daily_group()
            container_layout.addWidget(self._daily_group)

            self._leaderboard_group = self._build_leaderboard_group()
            container_layout.addWidget(self._leaderboard_group)

            self._recommendations_group = self._build_recommendations_group()
            container_layout.addWidget(self._recommendations_group)

            self._catalogue_group = self._build_catalogue_group()
            container_layout.addWidget(self._catalogue_group, stretch=1)

        def _build_profile_group(self) -> QGroupBox:
            """Create the profile summary group."""

            group = QGroupBox("Profile overview")
            layout = QFormLayout()
            group.setLayout(layout)

            self._profile_identifier_label = QLabel()
            layout.addRow("Active profile:", self._profile_identifier_label)

            self._profile_level_label = QLabel()
            layout.addRow("Level:", self._profile_level_label)

            self._profile_xp_label = QLabel()
            layout.addRow("Experience:", self._profile_xp_label)

            self._profile_achievements_label = QLabel()
            layout.addRow("Achievements:", self._profile_achievements_label)

            return group

        def _build_daily_group(self) -> QGroupBox:
            """Create the daily challenge summary widgets."""

            group = QGroupBox("Daily challenge")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._daily_summary_label = QLabel()
            self._daily_summary_label.setWordWrap(True)
            layout.addWidget(self._daily_summary_label)

            self._daily_status_label = QLabel()
            self._daily_status_label.setWordWrap(True)
            layout.addWidget(self._daily_status_label)

            self._daily_streak_label = QLabel()
            layout.addWidget(self._daily_streak_label)

            return group

        def _build_leaderboard_group(self) -> QGroupBox:
            """Create the leaderboard table widgets."""

            group = QGroupBox("Top players")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._leaderboard_table = QTableWidget(0, 5)
            self._leaderboard_table.setHorizontalHeaderLabels(["Rank", "Player", "Wins", "XP", "Achievement pts"])
            self._leaderboard_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self._leaderboard_table.setSelectionMode(QAbstractItemView.NoSelection)
            self._leaderboard_table.setAlternatingRowColors(True)
            layout.addWidget(self._leaderboard_table)

            return group

        def _build_recommendations_group(self) -> QGroupBox:
            """Create the recommendations list."""

            group = QGroupBox("Recommendations")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._recommendations_list = QListWidget()
            self._recommendations_list.setAlternatingRowColors(True)
            layout.addWidget(self._recommendations_list)

            return group

        def _build_catalogue_group(self) -> QGroupBox:
            """Create the catalogue tree widget."""

            group = QGroupBox("Games catalogue")
            layout = QHBoxLayout()
            group.setLayout(layout)

            self._catalogue_tree = QTreeWidget()
            self._catalogue_tree.setColumnCount(2)
            self._catalogue_tree.setHeaderLabels(["Game", "Genre"])
            self._catalogue_tree.setAlternatingRowColors(True)
            self._catalogue_tree.setRootIsDecorated(True)
            self._catalogue_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._catalogue_tree.setUniformRowHeights(True)
            self._catalogue_tree.currentItemChanged.connect(self._on_catalogue_selection_changed)
            layout.addWidget(self._catalogue_tree, stretch=1)

            detail_container = QScrollArea()
            detail_container.setWidgetResizable(True)
            layout.addWidget(detail_container, stretch=1)

            detail_widget = QWidget()
            detail_container.setWidget(detail_widget)
            detail_layout = QVBoxLayout()
            detail_layout.setContentsMargins(12, 12, 12, 12)
            detail_layout.setSpacing(8)
            detail_widget.setLayout(detail_layout)

            self._detail_title_label = QLabel("Select a game to view details")
            self._detail_title_label.setObjectName("catalogueDetailTitle")
            self._detail_title_label.setStyleSheet("font-size: 16px; font-weight: 600;")
            detail_layout.addWidget(self._detail_title_label)

            self._detail_image_label = QLabel()
            self._detail_image_label.setAlignment(Qt.AlignCenter)
            self._detail_image_label.setMinimumHeight(180)
            self._detail_image_label.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 4px;")
            detail_layout.addWidget(self._detail_image_label)

            self._detail_description_label = QLabel()
            self._detail_description_label.setWordWrap(True)
            detail_layout.addWidget(self._detail_description_label)

            self._detail_synopsis_label = QLabel()
            self._detail_synopsis_label.setWordWrap(True)
            detail_layout.addWidget(self._detail_synopsis_label)

            self._detail_tags_label = QLabel()
            self._detail_tags_label.setWordWrap(True)
            self._detail_tags_label.setStyleSheet("color: #cccccc;")
            detail_layout.addWidget(self._detail_tags_label)

            self._detail_mechanics_label = QLabel()
            self._detail_mechanics_label.setWordWrap(True)
            self._detail_mechanics_label.setStyleSheet("color: #cccccc;")
            detail_layout.addWidget(self._detail_mechanics_label)

            detail_layout.addStretch(1)
            self._set_detail_placeholder()

            return group

        def refresh_contents(self) -> None:
            """Refresh all sections with the latest profile insights."""

            self._catalogue = _sorted_catalogue()
            self._catalogue_index = {metadata.slug: metadata for metadata in self._catalogue}
            snapshot = build_launcher_snapshot(self._profile_service, self._scheduler)
            self._profile_identifier_label.setText(
                f"{snapshot.profile_name} ({snapshot.profile_identifier})"
            )
            self._profile_level_label.setText(str(snapshot.profile_level))
            self._profile_xp_label.setText(
                f"{snapshot.experience} XP (next level in {snapshot.experience_to_next} XP)"
            )
            self._profile_achievements_label.setText(
                f"{snapshot.achievements_unlocked}/{snapshot.achievements_total} ({snapshot.achievement_points} pts)"
            )

            status_colour = "#2e7d32" if snapshot.daily_completed else "#f9a825"
            status_text = "Completed" if snapshot.daily_completed else "Available"
            self._daily_summary_label.setText(snapshot.daily_selection.summary())
            self._daily_status_label.setText(
                f"Status: <span style='color:{status_colour}; font-weight:600'>{status_text}</span>"
            )
            self._daily_streak_label.setText(
                f"Streak: {snapshot.daily_streak} (Best {snapshot.best_daily_streak}) · Total completed: {snapshot.total_daily_completed}"
            )

            self._populate_leaderboard(snapshot.leaderboard)
            self._populate_recommendations(snapshot.recommendations)
            self._populate_catalogue()

        def _set_detail_placeholder(self) -> None:
            """Display guidance when no game is selected."""

            self._detail_title_label.setText("Select a game to view details")
            self._detail_description_label.setText("Browse the catalogue to preview descriptions, tags, and mechanics.")
            self._detail_synopsis_label.clear()
            self._detail_tags_label.clear()
            self._detail_mechanics_label.clear()
            self._detail_image_label.setPixmap(QPixmap())
            self._detail_image_label.setText("Screenshot preview unavailable")

        def _load_catalogue_pixmap(self, path: str | None) -> QPixmap | None:
            """Return a pixmap for ``path`` if the asset can be loaded."""

            if not path:
                return None
            try:
                resource = resources.files("games_collection").joinpath(path)
                data = resource.read_bytes()
            except (FileNotFoundError, OSError):
                return None

            pixmap = QPixmap()
            if pixmap.loadFromData(data):
                return pixmap
            return None

        def _on_catalogue_selection_changed(
            self, current: Optional[QTreeWidgetItem], _: Optional[QTreeWidgetItem]
        ) -> None:
            """Update the detail pane when the selection changes."""

            if current is None:
                self._set_detail_placeholder()
                return

            slug = current.data(0, Qt.UserRole)
            metadata = self._catalogue_index.get(slug) if isinstance(slug, str) else None
            if metadata is None:
                self._set_detail_placeholder()
                return

            self._update_detail_panel(metadata)

        def _update_detail_panel(self, metadata: GameMetadata) -> None:
            """Populate the detail pane with metadata information."""

            self._detail_title_label.setText(metadata.name)
            self._detail_description_label.setText(metadata.description)
            synopsis = metadata.synopsis or metadata.description
            self._detail_synopsis_label.setText(synopsis)

            if metadata.tags:
                self._detail_tags_label.setText(f"Tags: {', '.join(metadata.tags)}")
            else:
                self._detail_tags_label.setText("Tags: none specified")

            if metadata.mechanics:
                self._detail_mechanics_label.setText(f"Mechanics: {', '.join(metadata.mechanics)}")
            else:
                self._detail_mechanics_label.setText("Mechanics: flexible play")

            pixmap = self._load_catalogue_pixmap(metadata.screenshot_path)
            if pixmap is None or pixmap.isNull():
                self._detail_image_label.setPixmap(QPixmap())
                self._detail_image_label.setText("Screenshot preview unavailable")
            else:
                scaled = pixmap.scaled(420, 236, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self._detail_image_label.setText("")
                self._detail_image_label.setPixmap(scaled)

        def _populate_leaderboard(self, entries: Sequence[CrossGameLeaderboardEntry]) -> None:
            """Populate the leaderboard table."""

            self._leaderboard_table.setRowCount(len(entries) if entries else 1)
            if not entries:
                placeholder = QTableWidgetItem("Play a game to generate leaderboard data")
                placeholder.setFlags(placeholder.flags() & ~Qt.ItemIsEditable)
                self._leaderboard_table.setItem(0, 0, placeholder)
                for column in range(1, self._leaderboard_table.columnCount()):
                    empty = QTableWidgetItem("")
                    empty.setFlags(empty.flags() & ~Qt.ItemIsEditable)
                    self._leaderboard_table.setItem(0, column, empty)
                self._leaderboard_table.resizeColumnsToContents()
                return

            for row, entry in enumerate(entries):
                values = [
                    str(row + 1),
                    entry.display_name,
                    str(entry.total_wins),
                    str(entry.experience),
                    str(entry.achievement_points),
                ]
                for column, value in enumerate(values):
                    item = QTableWidgetItem(value)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self._leaderboard_table.setItem(row, column, item)

            self._leaderboard_table.resizeColumnsToContents()

        def _populate_recommendations(self, recommendations: Sequence[RecommendationResult]) -> None:
            """Populate the recommendations list."""

            self._recommendations_list.clear()
            if not recommendations:
                self._recommendations_list.addItem(
                    "Play a few more games to unlock personalised recommendations."
                )
                return

            for recommendation in recommendations:
                text = recommendation.game_name
                if recommendation.explanation:
                    text += f" — {recommendation.explanation}"
                if recommendation.reasons:
                    text += f" ({', '.join(recommendation.reasons)})"
                self._recommendations_list.addItem(QListWidgetItem(text))

        def _populate_catalogue(self) -> None:
            """Populate the catalogue tree with grouped entries."""

            self._catalogue_tree.clear()
            groups = _group_catalogue(self._catalogue)
            first_detail_item: Optional[QTreeWidgetItem] = None
            for group in groups:
                parent = QTreeWidgetItem([group.title, ""])
                parent.setFlags(parent.flags() & ~Qt.ItemIsEditable)
                self._catalogue_tree.addTopLevelItem(parent)
                for metadata in group.entries:
                    child = QTreeWidgetItem([metadata.name, metadata.genre.title()])
                    child.setData(0, Qt.UserRole, metadata.slug)
                    child.setFlags(child.flags() & ~Qt.ItemIsEditable)
                    parent.addChild(child)
                    if first_detail_item is None:
                        first_detail_item = child

            self._catalogue_tree.expandAll()
            if first_detail_item is not None:
                self._catalogue_tree.setCurrentItem(first_detail_item)
            else:
                self._set_detail_placeholder()


else:

    class LauncherWindow:  # type: ignore[too-few-public-methods]
        """Placeholder used when PyQt5 is unavailable."""

        def __init__(self, *_: object, **__: object) -> None:
            raise RuntimeError("PyQt5 is required to instantiate the launcher GUI")


def _build_pyqt_launcher(
    service: ProfileService, scheduler: DailyChallengeScheduler
) -> Optional[Callable[[], None]]:
    """Return a callable that boots the PyQt launcher when available."""

    if not PYQT5_AVAILABLE:
        return None

    def _launch() -> None:
        app = QApplication.instance() or QApplication([])
        window = LauncherWindow(service, scheduler)
        window.show()
        app.exec()

    return _launch


def run_launcher_gui(
    service: ProfileService,
    scheduler: DailyChallengeScheduler,
    *,
    preferred_framework: Optional[Framework] = None,
) -> bool:
    """Launch the desktop launcher if a supported GUI framework is installed."""

    pyqt_launcher = _build_pyqt_launcher(service, scheduler)
    launched, _ = launch_preferred_gui(
        preferred=preferred_framework,
        tkinter_launcher=None,
        pyqt_launcher=pyqt_launcher,
    )
    return launched


__all__ = ["LauncherWindow", "run_launcher_gui"]
