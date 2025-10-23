"""Shared configuration profiles and helpers for launcher settings panels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Optional, Tuple

from games_collection.core.architecture.settings import Settings, SettingsManager

SettingType = str

APPLICATION_SLUG = "launcher"
APPLICATION_DEFAULTS: Mapping[str, Any] = {
    "auto_check_updates": True,
    "detected_version": "",
    "latest_release_version": "",
    "latest_release_tag": "",
}


@dataclass(frozen=True)
class SettingField:
    """Describe a single configurable field for a game profile."""

    key: str
    label: str
    field_type: SettingType
    description: str = ""
    choices: Tuple[Any, ...] = ()

    def parse_user_value(self, raw: str) -> Any:
        """Parse a string entered by the user into the correct python value."""

        text = raw.strip()
        if self.field_type == "string":
            return text
        if self.field_type == "integer":
            if not text:
                raise ValueError("Enter an integer value.")
            return int(text)
        if self.field_type == "float":
            if not text:
                raise ValueError("Enter a numeric value.")
            return float(text)
        if self.field_type == "boolean":
            normalized = text.lower()
            truthy = {"y", "yes", "true", "1", "on"}
            falsy = {"n", "no", "false", "0", "off"}
            if normalized in truthy:
                return True
            if normalized in falsy:
                return False
            raise ValueError("Enter yes or no (y/n).")
        if self.field_type == "choice":
            if not self.choices:
                raise ValueError("No choices available for this option.")
            if not text:
                raise ValueError("Select one of the available options.")
            mapping = {str(choice).lower(): choice for choice in self.choices}
            normalized = text.lower()
            if normalized not in mapping:
                raise ValueError(f"Choose from: {', '.join(map(str, self.choices))}.")
            return mapping[normalized]
        raise ValueError(f"Unsupported field type: {self.field_type}")

    def normalise_value(self, value: Any) -> Any:
        """Coerce ``value`` into a canonical representation for storage."""

        if self.field_type == "string":
            return str(value)
        if self.field_type == "integer":
            return int(value)
        if self.field_type == "float":
            return float(value)
        if self.field_type == "boolean":
            if isinstance(value, str):
                return self.parse_user_value(value)
            return bool(value)
        if self.field_type == "choice":
            if not self.choices:
                raise ValueError("No choices defined for this option.")
            if value in self.choices:
                return value
            value_as_text = str(value).lower()
            for option in self.choices:
                if str(option).lower() == value_as_text:
                    return option
            raise ValueError(f"Value '{value}' is not in {self.choices}.")
        raise ValueError(f"Unsupported field type: {self.field_type}")

    def format_value(self, value: Any) -> str:
        """Return a human-readable representation of ``value``."""

        if self.field_type == "boolean":
            return "Yes" if bool(value) else "No"
        return str(value)


@dataclass(frozen=True)
class GameConfigurationProfile:
    """Describe configuration defaults and editable fields for a game."""

    slug: str
    title: str
    description: str
    defaults: Mapping[str, Any]
    fields: Tuple[SettingField, ...]

    def current_settings(self, settings: Mapping[str, Any]) -> Mapping[str, Any]:
        """Return ``settings`` merged with defaults for display purposes."""

        merged: dict[str, Any] = dict(self.defaults)
        merged.update(settings)
        return merged


_GLOBAL_SETTINGS_MANAGER = SettingsManager()


def get_settings_manager() -> SettingsManager:
    """Return the shared settings manager used by launcher utilities."""

    return _GLOBAL_SETTINGS_MANAGER


def get_launcher_settings(manager: Optional[SettingsManager] = None) -> Settings:
    """Return the launcher-level settings used to persist global preferences."""

    return load_settings(APPLICATION_SLUG, manager)


def get_auto_update_preference(manager: Optional[SettingsManager] = None) -> bool:
    """Return whether update checks should run automatically on startup."""

    settings = load_settings(APPLICATION_SLUG, manager)
    return bool(settings.get("auto_check_updates", True))


def set_auto_update_preference(enabled: bool, manager: Optional[SettingsManager] = None) -> bool:
    """Persist the automatic update checking preference."""

    settings = load_settings(APPLICATION_SLUG, manager)
    settings.set("auto_check_updates", bool(enabled))
    return save_settings(APPLICATION_SLUG, settings, manager)


def _profiles() -> dict[str, GameConfigurationProfile]:
    """Return the lazily constructed configuration profile mapping."""

    # Defaults capture commonly tweaked options for popular games. Additional
    # games can be added here without touching the launcher code.
    profiles: dict[str, GameConfigurationProfile] = {
        APPLICATION_SLUG: GameConfigurationProfile(
            slug=APPLICATION_SLUG,
            title="Launcher",
            description="Global launcher preferences including update behaviour and cached metadata.",
            defaults=dict(APPLICATION_DEFAULTS),
            fields=(
                SettingField(
                    "auto_check_updates",
                    "Automatically check for updates",
                    "boolean",
                    description="Run an update check on startup and show a banner when new releases are available.",
                ),
            ),
        ),
        "blackjack": GameConfigurationProfile(
            slug="blackjack",
            title="Blackjack",
            description="Tune bankroll, bet limits, and preferred GUI backend.",
            defaults={"bankroll": 500, "min_bet": 10, "decks": 6, "gui_framework": "pyqt5", "cli_mode": False},
            fields=(
                SettingField("bankroll", "Starting bankroll", "integer"),
                SettingField("min_bet", "Minimum bet", "integer"),
                SettingField("decks", "Number of decks", "integer"),
                SettingField("gui_framework", "Preferred GUI framework", "choice", choices=("pyqt5", "tkinter")),
                SettingField("cli_mode", "Always launch CLI", "boolean"),
            ),
        ),
        "spades": GameConfigurationProfile(
            slug="spades",
            title="Spades",
            description="Control GUI backend, theme, and audiovisual preferences.",
            defaults={
                "backend": "auto",
                "theme": "dark",
                "enable_sounds": True,
                "enable_animations": True,
            },
            fields=(
                SettingField("backend", "GUI backend", "choice", choices=("auto", "pyqt", "tk")),
                SettingField("theme", "Theme", "string"),
                SettingField("enable_sounds", "Enable sounds", "boolean"),
                SettingField("enable_animations", "Enable animations", "boolean"),
            ),
        ),
        "crossword": GameConfigurationProfile(
            slug="crossword",
            title="Crossword",
            description="Select dictionary pack and helper options for the CLI version.",
            defaults={"pack": "classic", "allow_hints": True},
            fields=(
                SettingField("pack", "Puzzle pack", "string"),
                SettingField("allow_hints", "Allow hints", "boolean"),
            ),
        ),
    }
    return profiles


def get_configuration_profiles() -> Tuple[GameConfigurationProfile, ...]:
    """Return all configuration profiles sorted by display title."""

    profiles = tuple(_profiles().values())
    return tuple(sorted(profiles, key=lambda profile: profile.title.lower()))


def get_configuration_profile(slug: str) -> Optional[GameConfigurationProfile]:
    """Return the profile for ``slug`` if a configuration is defined."""

    normalized = slug.strip().lower()
    return _profiles().get(normalized)


def storage_key(slug: str) -> str:
    """Return the settings namespace for ``slug``."""

    normalized = slug.strip().lower()
    return f"game::{normalized}"


def load_settings(slug: str, manager: Optional[SettingsManager] = None) -> Settings:
    """Load settings for ``slug`` using optional ``manager`` override."""

    profile = get_configuration_profile(slug)
    defaults: Mapping[str, Any] = profile.defaults if profile else {}
    return (manager or get_settings_manager()).load_settings(storage_key(slug), dict(defaults))


def save_settings(slug: str, settings: Settings, manager: Optional[SettingsManager] = None) -> bool:
    """Persist ``settings`` for ``slug``."""

    return (manager or get_settings_manager()).save_settings(storage_key(slug), settings)


def reset_settings(slug: str, manager: Optional[SettingsManager] = None) -> bool:
    """Reset stored overrides for ``slug`` back to defaults."""

    settings = load_settings(slug, manager)
    settings.reset()
    return save_settings(slug, settings, manager)


def merge_defaults(slug: str, overrides: Mapping[str, Any]) -> Mapping[str, Any]:
    """Merge ``overrides`` with defaults for display or launch contexts."""

    profile = get_configuration_profile(slug)
    combined: dict[str, Any] = {}
    if profile is not None:
        combined.update(profile.defaults)
    combined.update(overrides)
    return combined


def prepare_launcher_settings(slug: str, manager: Optional[SettingsManager] = None) -> dict[str, Any]:
    """Return the settings payload to provide when launching ``slug``."""

    settings = load_settings(slug, manager)
    return settings.to_dict()


def update_settings_from_mapping(
    slug: str,
    values: Mapping[str, Any],
    *,
    manager: Optional[SettingsManager] = None,
) -> bool:
    """Replace stored overrides for ``slug`` with ``values``."""

    profile = get_configuration_profile(slug)
    settings = load_settings(slug, manager)
    settings.reset()
    if profile is not None:
        working: MutableMapping[str, Any] = dict(profile.defaults)
    else:
        working = {}
    working.update(values)
    settings.update(working)
    return save_settings(slug, settings, manager)


__all__ = [
    "GameConfigurationProfile",
    "SettingField",
    "APPLICATION_SLUG",
    "get_settings_manager",
    "get_launcher_settings",
    "get_auto_update_preference",
    "set_auto_update_preference",
    "get_configuration_profile",
    "get_configuration_profiles",
    "load_settings",
    "save_settings",
    "reset_settings",
    "merge_defaults",
    "prepare_launcher_settings",
    "update_settings_from_mapping",
]
