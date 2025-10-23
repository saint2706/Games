"""Desktop launcher built on PyQt5 for browsing the Games catalogue."""

from __future__ import annotations

from dataclasses import dataclass
import os
import threading
from importlib import resources
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from games_collection.catalog.registry import GameMetadata, get_all_games
from games_collection.core.configuration import (
    get_configuration_profile,
    get_settings_manager,
    load_settings,
    prepare_launcher_settings,
    reset_settings,
    update_settings_from_mapping,
)
from games_collection.core.daily_challenges import DailyChallengeScheduler
from games_collection.core.gui_frameworks import Framework, launch_preferred_gui
from games_collection.core.profile_service import ProfileService, ProfileServiceError, RecentlyPlayedEntry
from games_collection.core.leaderboard_service import CrossGameLeaderboardEntry
from games_collection.core.recommendation_service import RecommendationResult
from games_collection.core.update_service import (
    UpdateCheckResult,
    check_for_updates,
    detect_bundle,
    download_release_asset,
    get_auto_update_preference,
    set_auto_update_preference,
)
from games_collection.launcher import GENRE_ORDER, build_launcher_snapshot, format_recent_timestamp, get_game_entry

from games_collection.core.gui_base_pyqt import BaseGUI, GUIConfig, PYQT5_AVAILABLE

if PYQT5_AVAILABLE:  # pragma: no cover - exercised via smoke tests
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QHeaderView,
        QInputDialog,
        QCheckBox,
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QDoubleSpinBox,
        QFormLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QListWidgetItem,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QScrollArea,
        QTableWidget,
        QTableWidgetItem,
        QTreeWidget,
        QTreeWidgetItem,
        QVBoxLayout,
        QWidget,
        QSpinBox,
    )
else:  # pragma: no cover - exercised when GUI extras missing
    QApplication = None  # type: ignore[assignment]
    QHeaderView = None  # type: ignore[assignment]
    QInputDialog = None  # type: ignore[assignment]
    QCheckBox = None  # type: ignore[assignment]
    QComboBox = None  # type: ignore[assignment]
    QDialog = None  # type: ignore[assignment]
    QDialogButtonBox = None  # type: ignore[assignment]
    QDoubleSpinBox = None  # type: ignore[assignment]
    QFormLayout = None  # type: ignore[assignment]
    QGroupBox = None  # type: ignore[assignment]
    QHBoxLayout = None  # type: ignore[assignment]
    QLabel = None  # type: ignore[assignment]
    QListWidget = None  # type: ignore[assignment]
    QListWidgetItem = None  # type: ignore[assignment]
    QLineEdit = None  # type: ignore[assignment]
    QMainWindow = None  # type: ignore[assignment]
    QMessageBox = None  # type: ignore[assignment]
    QPushButton = None  # type: ignore[assignment]
    QScrollArea = None  # type: ignore[assignment]
    QTableWidget = None  # type: ignore[assignment]
    QTableWidgetItem = None  # type: ignore[assignment]
    QTreeWidget = None  # type: ignore[assignment]
    QTreeWidgetItem = None  # type: ignore[assignment]
    QVBoxLayout = None  # type: ignore[assignment]
    QWidget = None  # type: ignore[assignment]
    QSpinBox = None  # type: ignore[assignment]


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

    class ConfigurationDialog(QDialog):
        """Dialog that exposes editable settings for a single game."""

        def __init__(self, parent: QWidget, slug: str) -> None:
            profile = get_configuration_profile(slug)
            if profile is None:
                raise ValueError(f"No configuration profile is registered for {slug}.")
            super().__init__(parent)
            self._slug = slug
            self._profile = profile
            self._manager = get_settings_manager()
            self._settings = load_settings(slug, self._manager)
            self._widgets: dict[str, QWidget] = {}
            self.setWindowTitle(f"{profile.title} settings")
            self._build_layout()
            self._apply_settings()

        def _build_layout(self) -> None:
            layout = QVBoxLayout()
            self.setLayout(layout)

            description = QLabel(self._profile.description)
            description.setWordWrap(True)
            layout.addWidget(description)

            form = QFormLayout()
            merged = self._profile.current_settings(self._settings.to_dict())
            for field in self._profile.fields:
                widget = self._create_widget(field, merged.get(field.key))
                widget.setToolTip(field.description)
                self._widgets[field.key] = widget
                form.addRow(f"{field.label}:", widget)
            layout.addLayout(form)

            self._button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            reset_button = self._button_box.addButton("Reset to defaults", QDialogButtonBox.ResetRole)
            self._button_box.accepted.connect(self._on_accept)  # type: ignore[arg-type]
            self._button_box.rejected.connect(self.reject)  # type: ignore[arg-type]
            reset_button.clicked.connect(self._on_reset)  # type: ignore[arg-type]
            layout.addWidget(self._button_box)

        def _create_widget(self, field, value):  # noqa: ANN001 - Qt widget factory
            if field.field_type == "boolean":
                checkbox = QCheckBox()
                checkbox.setChecked(bool(value))
                return checkbox
            if field.field_type == "choice":
                combo = QComboBox()
                for choice in field.choices:
                    combo.addItem(str(choice), choice)
                if value is not None:
                    index = combo.findData(value)
                    if index < 0:
                        index = combo.findText(str(value))
                    if index >= 0:
                        combo.setCurrentIndex(index)
                return combo
            if field.field_type == "integer":
                spin = QSpinBox()
                spin.setRange(-1_000_000, 1_000_000)
                spin.setValue(int(value) if value is not None else 0)
                return spin
            if field.field_type == "float":
                spin = QDoubleSpinBox()
                spin.setDecimals(2)
                spin.setRange(-1_000_000.0, 1_000_000.0)
                spin.setValue(float(value) if value is not None else 0.0)
                return spin
            line_edit = QLineEdit(str(value) if value is not None else "")
            return line_edit

        def _apply_settings(self) -> None:
            merged = self._profile.current_settings(self._settings.to_dict())
            for field in self._profile.fields:
                value = merged.get(field.key)
                widget = self._widgets.get(field.key)
                if widget is None:
                    continue
                if isinstance(widget, QCheckBox):
                    widget.setChecked(bool(value))
                    continue
                if isinstance(widget, QComboBox):
                    if value is None:
                        widget.setCurrentIndex(0 if widget.count() else -1)
                    else:
                        index = widget.findData(value)
                        if index < 0:
                            index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    continue
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value) if value is not None else 0)
                    continue
                if isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value) if value is not None else 0.0)
                    continue
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value) if value is not None else "")

        def _collect_values(self) -> dict[str, object]:
            collected: dict[str, object] = {}
            for field in self._profile.fields:
                widget = self._widgets[field.key]
                if isinstance(widget, QCheckBox):
                    raw_value = widget.isChecked()
                elif isinstance(widget, QComboBox):
                    data = widget.currentData()
                    raw_value = data if data is not None else widget.currentText()
                elif isinstance(widget, QSpinBox):
                    raw_value = widget.value()
                elif isinstance(widget, QDoubleSpinBox):
                    raw_value = widget.value()
                elif isinstance(widget, QLineEdit):
                    raw_value = widget.text()
                else:  # pragma: no cover - defensive for unexpected widget
                    raw_value = None
                try:
                    collected[field.key] = field.normalise_value(raw_value)
                except ValueError as exc:
                    raise ValueError(f"{field.label}: {exc}") from exc
            return collected

        def _on_accept(self) -> None:
            try:
                payload = self._collect_values()
            except ValueError as exc:
                QMessageBox.warning(self, "Game settings", str(exc))
                return
            if not update_settings_from_mapping(self._slug, payload, manager=self._manager):
                QMessageBox.warning(
                    self,
                    "Game settings",
                    "Settings could not be saved. Check file permissions and try again.",
                )
                return
            QMessageBox.information(self, "Game settings", "Settings saved.")
            self.accept()

        def _on_reset(self) -> None:
            if not reset_settings(self._slug, self._manager):
                QMessageBox.warning(
                    self,
                    "Game settings",
                    "Settings could not be reset. Check file permissions and try again.",
                )
                return
            self._settings = load_settings(self._slug, self._manager)
            self._apply_settings()
            QMessageBox.information(self, "Game settings", "Settings restored to defaults.")


    class LauncherWindow(QMainWindow, BaseGUI):
        """PyQt5 window presenting launcher insights and catalogue browsing."""

        def __init__(self, profile_service: ProfileService, scheduler: DailyChallengeScheduler) -> None:
            self._profile_service = profile_service
            self._scheduler = scheduler
            self._catalogue = _sorted_catalogue()
            self._catalogue_index = {metadata.slug: metadata for metadata in self._catalogue}
            self._favorite_slugs: set[str] = set()
            self._quick_alias_map: Dict[str, str] = {}
            self._quick_alias_rows: List[str] = []
            self._settings_manager = get_settings_manager()
            self._selected_slug: Optional[str] = None
            self._update_check_result: Optional[UpdateCheckResult] = None
            self._bundle_hint = detect_bundle()
            self._auto_check_enabled = get_auto_update_preference(self._settings_manager)
            self._update_banner: Optional[QWidget] = None
            self._update_label: Optional[QLabel] = None
            self._update_download_button: Optional[QPushButton] = None
            self._auto_check_checkbox: Optional[QCheckBox] = None
            self._check_updates_button: Optional[QPushButton] = None

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
            if self._update_banner is not None:
                self._update_banner.hide()
            self.refresh_contents()
            if self._auto_check_enabled:
                self._queue_update_check()

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
            self._check_updates_button = QPushButton("Check for updates")
            self._check_updates_button.clicked.connect(self._on_manual_update_check)  # type: ignore[arg-type]
            header_layout.addWidget(self._check_updates_button)
            container_layout.addLayout(header_layout)

            self._update_banner = self._build_update_banner()
            container_layout.addWidget(self._update_banner)

            self._profile_group = self._build_profile_group()
            container_layout.addWidget(self._profile_group)

            self._daily_group = self._build_daily_group()
            container_layout.addWidget(self._daily_group)

            self._favorites_group = self._build_favorites_group()
            container_layout.addWidget(self._favorites_group)

            self._quick_launch_group = self._build_quick_launch_group()
            container_layout.addWidget(self._quick_launch_group)

            self._recently_played_group = self._build_recently_played_group()
            container_layout.addWidget(self._recently_played_group)

            self._leaderboard_group = self._build_leaderboard_group()
            container_layout.addWidget(self._leaderboard_group)

            self._recommendations_group = self._build_recommendations_group()
            container_layout.addWidget(self._recommendations_group)

            self._catalogue_group = self._build_catalogue_group()
            container_layout.addWidget(self._catalogue_group, stretch=1)

        def _build_update_banner(self) -> QWidget:
            """Create the dismissible update notification banner."""

            banner = QWidget()
            banner.setObjectName("updateBanner")
            layout = QHBoxLayout()
            layout.setContentsMargins(12, 8, 12, 8)
            layout.setSpacing(10)
            banner.setLayout(layout)

            self._update_label = QLabel("Checking for updates…")
            self._update_label.setWordWrap(True)
            layout.addWidget(self._update_label, stretch=1)

            self._update_download_button = QPushButton("Download update")
            self._update_download_button.setEnabled(False)
            self._update_download_button.clicked.connect(self._on_download_update)  # type: ignore[arg-type]
            layout.addWidget(self._update_download_button)

            dismiss_button = QPushButton("Dismiss")
            dismiss_button.clicked.connect(banner.hide)  # type: ignore[arg-type]
            layout.addWidget(dismiss_button)

            self._auto_check_checkbox = QCheckBox("Check automatically on startup")
            self._auto_check_checkbox.setChecked(self._auto_check_enabled)
            self._auto_check_checkbox.stateChanged.connect(self._on_auto_check_toggled)  # type: ignore[arg-type]
            layout.addWidget(self._auto_check_checkbox)

            return banner

        def _on_manual_update_check(self) -> None:
            """Trigger a manual update check."""

            self._queue_update_check(manual=True)

        def _queue_update_check(self, manual: bool = False) -> None:
            """Schedule an update check on a background thread."""

            if self._check_updates_button is not None:
                self._check_updates_button.setEnabled(False)
            if self._update_banner is not None and self._update_label is not None:
                self._update_label.setText("Checking for updates…")
                if self._update_download_button is not None:
                    self._update_download_button.setEnabled(False)
                self._update_banner.show()
            thread = threading.Thread(target=self._run_update_check, args=(manual,), daemon=True)
            thread.start()

        def _run_update_check(self, manual: bool) -> None:
            """Perform the network request for update metadata."""

            result = check_for_updates(manager=self._settings_manager)
            self._update_check_result = result

            def _apply() -> None:
                if self._check_updates_button is not None:
                    self._check_updates_button.setEnabled(True)
                self._apply_update_result(result, manual)

            QTimer.singleShot(0, _apply)

        def _apply_update_result(self, result: UpdateCheckResult, manual: bool) -> None:
            """Update the banner contents after fetching update metadata."""

            release = result.release
            if release is None:
                if self._update_label is not None:
                    self._update_label.setText("Unable to contact the update service.")
                if self._update_download_button is not None:
                    self._update_download_button.setEnabled(False)
                if manual:
                    QMessageBox.warning(self, "Updates", "Unable to contact the update service.")
                if self._update_banner is not None:
                    self._update_banner.show()
                return

            latest_label = release.version or release.tag_name or "latest"
            installed_label = result.installed_version or "unknown"

            if result.update_available:
                if self._update_label is not None:
                    self._update_label.setText(
                        f"Update available: {latest_label} (installed {installed_label})."
                    )
                if self._update_download_button is not None:
                    self._update_download_button.setEnabled(True)
                if self._update_banner is not None:
                    self._update_banner.show()
                if manual and release.html_url:
                    QMessageBox.information(
                        self,
                        "Update available",
                        f"Version {latest_label} is available. Release notes:\n{release.html_url}",
                    )
                return

            if self._update_label is not None:
                self._update_label.setText("You are already using the latest version.")
            if self._update_download_button is not None:
                self._update_download_button.setEnabled(False)
            if manual:
                QMessageBox.information(self, "Updates", "You are already using the latest version.")
                if self._update_banner is not None:
                    self._update_banner.hide()
            else:
                if self._update_banner is not None:
                    self._update_banner.hide()

        def _on_auto_check_toggled(self, state: int) -> None:
            """Persist the user's preference for automatic update checks."""

            enabled = state == Qt.Checked
            set_auto_update_preference(enabled, self._settings_manager)
            self._auto_check_enabled = enabled

        def _on_download_update(self) -> None:
            """Download the selected release asset in the background."""

            release = self._update_check_result.release if self._update_check_result else None
            if release is None:
                QMessageBox.information(self, "Updates", "No update is currently available.")
                return

            if self._update_download_button is not None:
                self._update_download_button.setEnabled(False)
            QApplication.setOverrideCursor(Qt.WaitCursor)

            def _download() -> None:
                try:
                    path = download_release_asset(release, bundle_hint=self._bundle_hint)
                except RuntimeError as exc:
                    QTimer.singleShot(0, lambda: self._handle_download_failure(str(exc)))
                else:
                    QTimer.singleShot(0, lambda p=path: self._handle_download_success(p))
                finally:
                    QTimer.singleShot(0, QApplication.restoreOverrideCursor)

            threading.Thread(target=_download, daemon=True).start()

        def _handle_download_failure(self, error: str) -> None:
            """Display an error message when the update download fails."""

            if self._update_download_button is not None:
                self._update_download_button.setEnabled(True)
            QMessageBox.critical(self, "Download failed", error)

        def _handle_download_success(self, path: Path) -> None:
            """Prompt the user to launch the downloaded build."""

            if self._update_download_button is not None:
                self._update_download_button.setEnabled(True)

            prompt = QMessageBox.question(
                self,
                "Update downloaded",
                f"Update downloaded to:\n{path}\nRelaunch now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )

            if prompt == QMessageBox.Yes:
                self._profile_service.save_active_profile()
                try:
                    os.execv(str(path), [str(path)])
                except OSError as exc:
                    QMessageBox.critical(self, "Relaunch failed", f"Unable to relaunch the downloaded build: {exc}")
            else:
                QMessageBox.information(
                    self,
                    "Update downloaded",
                    f"Launch the downloaded file at {path} to start the new version.",
                )

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

        def _build_favorites_group(self) -> QGroupBox:
            """Create the favorites list widgets."""

            group = QGroupBox("Favorite games")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._favorites_list = QListWidget()
            self._favorites_list.setAlternatingRowColors(True)
            layout.addWidget(self._favorites_list)

            return group

        def _build_quick_launch_group(self) -> QGroupBox:
            """Create the quick-launch alias management widgets."""

            group = QGroupBox("Quick-launch aliases")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._quick_alias_hint = QLabel("Create shortcuts to launch games instantly.")
            self._quick_alias_hint.setWordWrap(True)
            layout.addWidget(self._quick_alias_hint)

            self._quick_alias_table = QTableWidget(0, 2)
            self._quick_alias_table.setHorizontalHeaderLabels(["Alias", "Game"])
            self._quick_alias_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self._quick_alias_table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self._quick_alias_table.setSelectionMode(QAbstractItemView.SingleSelection)
            self._quick_alias_table.setAlternatingRowColors(True)
            self._quick_alias_table.verticalHeader().setVisible(False)
            header = self._quick_alias_table.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self._quick_alias_table.itemSelectionChanged.connect(self._on_quick_alias_selection_changed)
            self._quick_alias_table.doubleClicked.connect(self._on_quick_alias_double_clicked)  # type: ignore[arg-type]
            layout.addWidget(self._quick_alias_table)

            button_layout = QHBoxLayout()
            self._quick_alias_add_button = QPushButton("Add alias")
            self._quick_alias_add_button.clicked.connect(self._on_add_quick_alias)  # type: ignore[arg-type]
            button_layout.addWidget(self._quick_alias_add_button)

            self._quick_alias_update_button = QPushButton("Update game")
            self._quick_alias_update_button.clicked.connect(self._on_update_quick_alias)  # type: ignore[arg-type]
            button_layout.addWidget(self._quick_alias_update_button)

            self._quick_alias_rename_button = QPushButton("Rename")
            self._quick_alias_rename_button.clicked.connect(self._on_rename_quick_alias)  # type: ignore[arg-type]
            button_layout.addWidget(self._quick_alias_rename_button)

            self._quick_alias_delete_button = QPushButton("Delete")
            self._quick_alias_delete_button.clicked.connect(self._on_delete_quick_alias)  # type: ignore[arg-type]
            button_layout.addWidget(self._quick_alias_delete_button)

            self._quick_alias_launch_button = QPushButton("Launch")
            self._quick_alias_launch_button.clicked.connect(self._on_launch_quick_alias)  # type: ignore[arg-type]
            button_layout.addWidget(self._quick_alias_launch_button)

            layout.addLayout(button_layout)
            self._update_quick_alias_buttons()

            return group

        def _build_recently_played_group(self) -> QGroupBox:
            """Create the recently played games list."""

            group = QGroupBox("Recently played")
            layout = QVBoxLayout()
            group.setLayout(layout)

            self._recently_played_list = QListWidget()
            self._recently_played_list.setAlternatingRowColors(True)
            layout.addWidget(self._recently_played_list)

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

            self._favorite_button = QPushButton("Add to favorites")
            self._favorite_button.setEnabled(False)
            self._favorite_button.clicked.connect(self._on_toggle_favorite)  # type: ignore[arg-type]
            detail_layout.addWidget(self._favorite_button)

            self._configure_button = QPushButton("Configure settings")
            self._configure_button.setEnabled(False)
            self._configure_button.clicked.connect(self._on_configure_game)  # type: ignore[arg-type]
            detail_layout.addWidget(self._configure_button)

            detail_layout.addStretch(1)
            self._set_detail_placeholder()

            return group

        def refresh_contents(self) -> None:
            """Refresh all sections with the latest profile insights."""

            self._catalogue = _sorted_catalogue()
            self._catalogue_index = {metadata.slug: metadata for metadata in self._catalogue}
            current_item = self._catalogue_tree.currentItem()
            selected_slug = current_item.data(0, Qt.UserRole) if current_item else None
            selected_slug_str = selected_slug if isinstance(selected_slug, str) else None
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

            favorites = list(snapshot.favorite_games)
            self._favorite_slugs = set(favorites)
            self._populate_favorites(favorites)
            self._populate_quick_launch_aliases(self._profile_service.get_quick_launch_aliases())
            self._populate_recently_played(snapshot.recently_played)
            self._populate_leaderboard(snapshot.leaderboard)
            self._populate_recommendations(snapshot.recommendations)
            self._populate_catalogue(selected_slug=selected_slug_str)

        def _set_detail_placeholder(self) -> None:
            """Display guidance when no game is selected."""

            self._selected_slug = None
            self._detail_title_label.setText("Select a game to view details")
            self._detail_description_label.setText("Browse the catalogue to preview descriptions, tags, and mechanics.")
            self._detail_synopsis_label.clear()
            self._detail_tags_label.clear()
            self._detail_mechanics_label.clear()
            self._detail_image_label.setPixmap(QPixmap())
            self._detail_image_label.setText("Screenshot preview unavailable")
            self._favorite_button.setEnabled(False)
            self._favorite_button.setText("Select a game to manage favorites")
            self._configure_button.setEnabled(False)
            self._configure_button.setText("Select a game to edit settings")

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

            if metadata.slug in self._favorite_slugs:
                self._favorite_button.setText("Remove from favorites")
            else:
                self._favorite_button.setText("Add to favorites")
            self._favorite_button.setEnabled(True)
            self._selected_slug = metadata.slug
            profile = get_configuration_profile(metadata.slug)
            if profile is None:
                self._configure_button.setEnabled(False)
                self._configure_button.setText("No configurable settings")
            else:
                self._configure_button.setEnabled(True)
                self._configure_button.setText("Configure settings")

        def _on_toggle_favorite(self) -> None:
            """Toggle the favorite status for the currently selected game."""

            current = self._catalogue_tree.currentItem()
            if current is None:
                return
            slug = current.data(0, Qt.UserRole)
            if not isinstance(slug, str):
                return

            if slug in self._favorite_slugs:
                changed = self._profile_service.unmark_favorite(slug)
            else:
                changed = self._profile_service.mark_favorite(slug)
            if not changed:
                return

            favorites = self._profile_service.get_favorites()
            self._favorite_slugs = set(favorites)
            self._populate_favorites(favorites)
            self._populate_catalogue(selected_slug=slug)
            metadata = self._catalogue_index.get(slug)
            if metadata is not None:
                self._update_detail_panel(metadata)

        def _on_configure_game(self) -> None:
            """Open the configuration dialog for the selected game."""

            if self._selected_slug is None:
                return
            profile = get_configuration_profile(self._selected_slug)
            if profile is None:
                QMessageBox.information(
                    self,
                    "Game settings",
                    "This game does not expose configurable settings yet.",
                )
                return
            dialog = ConfigurationDialog(self, self._selected_slug)
            dialog.exec_()

        def _populate_recently_played(self, entries: Sequence[RecentlyPlayedEntry]) -> None:
            """Populate the recently played list."""

            self._recently_played_list.clear()
            if not entries:
                self._recently_played_list.addItem("Play a game to populate this list.")
                return

            for entry in entries:
                metadata = self._catalogue_index.get(entry.game_id)
                if metadata is None:
                    game_name = entry.game_id.replace("_", " ").title()
                else:
                    game_name = metadata.name
                timestamp = format_recent_timestamp(entry.last_played)
                self._recently_played_list.addItem(QListWidgetItem(f"{game_name} — {timestamp}"))

        def _populate_favorites(self, favorite_slugs: Sequence[str]) -> None:
            """Populate the favorites list."""

            self._favorites_list.clear()
            if not favorite_slugs:
                self._favorites_list.addItem("Use the catalogue to star games you love.")
                return

            for slug in favorite_slugs:
                metadata = self._catalogue_index.get(slug)
                if metadata is None:
                    name = slug.replace("_", " ").title()
                else:
                    name = metadata.name
                self._favorites_list.addItem(QListWidgetItem(name))

        def _populate_quick_launch_aliases(self, aliases: Dict[str, str]) -> None:
            """Populate the quick-launch aliases table."""

            self._quick_alias_table.setRowCount(0)
            self._quick_alias_table.clearContents()
            self._quick_alias_table.clearSelection()
            self._quick_alias_map = dict(sorted(aliases.items()))
            self._quick_alias_rows = list(self._quick_alias_map.keys())
            if not self._quick_alias_map:
                self._quick_alias_hint.setText("No quick-launch aliases configured. Use 'Add alias' to create one.")
                self._update_quick_alias_buttons()
                return

            self._quick_alias_hint.setText("Select an alias to update, delete, launch, or rename it.")
            self._quick_alias_table.setRowCount(len(self._quick_alias_rows))
            for row, alias in enumerate(self._quick_alias_rows):
                slug = self._quick_alias_map[alias]
                alias_item = QTableWidgetItem(f"!{alias}")
                alias_item.setFlags(alias_item.flags() & ~Qt.ItemIsEditable)
                metadata = self._catalogue_index.get(slug)
                name = metadata.name if metadata is not None else slug.replace("_", " ").title()
                game_item = QTableWidgetItem(name)
                game_item.setFlags(game_item.flags() & ~Qt.ItemIsEditable)
                self._quick_alias_table.setItem(row, 0, alias_item)
                self._quick_alias_table.setItem(row, 1, game_item)
            self._update_quick_alias_buttons()

        def _get_selected_alias(self) -> tuple[Optional[str], Optional[str]]:
            """Return the currently selected alias and slug, if available."""

            selection = self._quick_alias_table.selectionModel()
            if selection is None:
                return None, None
            rows = selection.selectedRows()
            if not rows:
                return None, None
            row = rows[0].row()
            if row < 0 or row >= len(self._quick_alias_rows):
                return None, None
            alias = self._quick_alias_rows[row]
            return alias, self._quick_alias_map.get(alias)

        def _update_quick_alias_buttons(self) -> None:
            """Enable or disable alias management buttons based on selection."""

            alias, slug = self._get_selected_alias()
            has_selection = alias is not None and slug is not None
            for button in (
                self._quick_alias_update_button,
                self._quick_alias_rename_button,
                self._quick_alias_delete_button,
                self._quick_alias_launch_button,
            ):
                button.setEnabled(has_selection)

        def _on_quick_alias_selection_changed(self) -> None:
            """Refresh button states when the selection changes."""

            self._update_quick_alias_buttons()

        def _on_quick_alias_double_clicked(self, _index) -> None:  # noqa: ANN001 - Qt callback signature
            """Launch the selected alias when the row is double-clicked."""

            self._on_launch_quick_alias()

        def _prompt_alias_name(self, title: str, *, default: str = "") -> Optional[str]:
            """Prompt the user for an alias name."""

            text, accepted = QInputDialog.getText(self, title, "Alias name:", text=default)
            alias = text.strip()
            if not accepted or not alias:
                return None
            return alias

        def _choose_game_slug(self, title: str, *, current_slug: Optional[str] = None) -> Optional[str]:
            """Prompt the user to choose a game slug from the catalogue."""

            if not self._catalogue:
                QMessageBox.warning(self, title, "No games are available to associate with an alias.")
                return None
            entries = [f"{metadata.name} ({metadata.slug})" for metadata in self._catalogue]
            mapping = {label: metadata.slug for label, metadata in zip(entries, self._catalogue)}
            default_index = 0
            if current_slug:
                for idx, metadata in enumerate(self._catalogue):
                    if metadata.slug == current_slug:
                        default_index = idx
                        break
            selection, accepted = QInputDialog.getItem(
                self,
                title,
                "Select a game to associate with the alias:",
                entries,
                default_index,
                False,
            )
            if not accepted:
                return None
            return mapping.get(selection)

        def _show_quick_alias_error(self, message: str) -> None:
            """Display an error related to quick-launch management."""

            QMessageBox.warning(self, "Quick-launch aliases", message)

        def _show_quick_alias_info(self, message: str) -> None:
            """Display an informational message for quick-launch operations."""

            QMessageBox.information(self, "Quick-launch aliases", message)

        def _on_add_quick_alias(self) -> None:
            """Handle the Add alias button click."""

            alias = self._prompt_alias_name("Add quick-launch alias")
            if alias is None:
                return
            slug = self._choose_game_slug("Select game for alias")
            if slug is None:
                return
            try:
                self._profile_service.add_quick_launch_alias(alias, slug)
            except ProfileServiceError as exc:
                self._show_quick_alias_error(str(exc))
                return
            self._populate_quick_launch_aliases(self._profile_service.get_quick_launch_aliases())
            name = self._catalogue_index.get(slug)
            display = name.name if name is not None else slug.replace("_", " ").title()
            self._show_quick_alias_info(f"Alias !{alias.strip().lower()} now launches {display}.")

        def _on_update_quick_alias(self) -> None:
            """Handle updating the game associated with an alias."""

            alias, slug = self._get_selected_alias()
            if alias is None or slug is None:
                return
            new_slug = self._choose_game_slug("Update alias target", current_slug=slug)
            if new_slug is None:
                return
            try:
                self._profile_service.update_quick_launch_alias(alias, new_slug)
            except ProfileServiceError as exc:
                self._show_quick_alias_error(str(exc))
                return
            self._populate_quick_launch_aliases(self._profile_service.get_quick_launch_aliases())
            metadata = self._catalogue_index.get(new_slug)
            display = metadata.name if metadata is not None else new_slug.replace("_", " ").title()
            self._show_quick_alias_info(f"Alias !{alias} now launches {display}.")

        def _on_rename_quick_alias(self) -> None:
            """Handle renaming an existing alias."""

            alias, slug = self._get_selected_alias()
            if alias is None or slug is None:
                return
            new_alias = self._prompt_alias_name("Rename quick-launch alias", default=alias)
            if new_alias is None or new_alias == alias:
                return
            try:
                self._profile_service.rename_quick_launch_alias(alias, new_alias)
            except ProfileServiceError as exc:
                self._show_quick_alias_error(str(exc))
                return
            self._populate_quick_launch_aliases(self._profile_service.get_quick_launch_aliases())
            self._show_quick_alias_info(f"Alias renamed to !{new_alias.strip().lower()}.")

        def _on_delete_quick_alias(self) -> None:
            """Handle deleting the selected alias."""

            alias, _ = self._get_selected_alias()
            if alias is None:
                return
            confirmation = QMessageBox.question(
                self,
                "Delete quick-launch alias",
                f"Are you sure you want to remove !{alias}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirmation != QMessageBox.Yes:
                return
            removed = self._profile_service.delete_quick_launch_alias(alias)
            if not removed:
                self._show_quick_alias_error("Alias could not be removed; it may have already been deleted.")
                return
            self._populate_quick_launch_aliases(self._profile_service.get_quick_launch_aliases())
            self._show_quick_alias_info(f"Removed quick-launch alias !{alias}.")

        def _on_launch_quick_alias(self) -> None:
            """Launch the game associated with the selected alias."""

            alias, slug = self._get_selected_alias()
            if alias is None or slug is None:
                return
            entry = get_game_entry(slug)
            if entry is None:
                self._show_quick_alias_error("The associated game could not be found.")
                return
            _, launcher_callable = entry
            try:
                payload = prepare_launcher_settings(slug, self._settings_manager)
                launcher_callable(payload if payload else None)
            except Exception as exc:  # pragma: no cover - runtime guard
                self._show_quick_alias_error(f"Failed to launch the game: {exc}")
                return
            self._show_quick_alias_info(f"Launched quick alias !{alias}.")
            self.refresh_contents()

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

        def _populate_catalogue(self, selected_slug: Optional[str] = None) -> None:
            """Populate the catalogue tree with grouped entries."""

            self._catalogue_tree.clear()
            groups = _group_catalogue(self._catalogue)
            target_item: Optional[QTreeWidgetItem] = None
            for group in groups:
                parent = QTreeWidgetItem([group.title, ""])
                parent.setFlags(parent.flags() & ~Qt.ItemIsEditable)
                self._catalogue_tree.addTopLevelItem(parent)
                for metadata in group.entries:
                    label = metadata.name
                    if metadata.slug in self._favorite_slugs:
                        label = f"★ {metadata.name}"
                    child = QTreeWidgetItem([label, metadata.genre.title()])
                    child.setData(0, Qt.UserRole, metadata.slug)
                    child.setFlags(child.flags() & ~Qt.ItemIsEditable)
                    parent.addChild(child)
                    if selected_slug is not None and metadata.slug == selected_slug:
                        target_item = child
                    elif target_item is None:
                        target_item = child

            self._catalogue_tree.expandAll()
            if target_item is not None:
                self._catalogue_tree.setCurrentItem(target_item)
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
