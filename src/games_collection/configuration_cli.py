"""Interactive command-line helpers for editing game configuration profiles."""

from __future__ import annotations

from typing import Callable, Mapping

from games_collection.core.architecture.settings import SettingsManager
from games_collection.core.configuration import (
    GameConfigurationProfile,
    SettingField,
    get_configuration_profile,
    get_configuration_profiles,
    load_settings,
    reset_settings,
    save_settings,
)


InputFunc = Callable[[str], str]
OutputFunc = Callable[[str], None]


def _format_field_row(field: SettingField, current: Mapping[str, object], defaults: Mapping[str, object], index: int) -> str:
    current_value = current.get(field.key, defaults.get(field.key))
    default_value = defaults.get(field.key)
    marker = " *" if current_value != default_value else ""
    description = field.format_value(current_value) if current_value is not None else "<unset>"
    return f"{index}. {field.label}: {description} (default: {field.format_value(default_value)}){marker}"


def _edit_profile(
    profile: GameConfigurationProfile,
    manager: SettingsManager,
    *,
    input_func: InputFunc,
    output_func: OutputFunc,
) -> None:
    settings = load_settings(profile.slug, manager)
    working = settings.to_dict()

    while True:
        output_func("\n" + profile.title)
        output_func("-" * len(profile.title))
        output_func(profile.description)
        merged = profile.current_settings(working)
        for index, field in enumerate(profile.fields, start=1):
            output_func(_format_field_row(field, merged, profile.defaults, index))

        output_func("\nOptions: [number] edit value, [R]eset to defaults, [S]ave changes, [B]ack")
        choice = input_func("Select an option: ").strip().lower()

        if choice in {"", "b", "back"}:
            return
        if choice in {"r", "reset"}:
            if reset_settings(profile.slug, manager):
                output_func("Settings restored to defaults.")
            else:
                output_func("Unable to reset settings; check file permissions.")
            working = load_settings(profile.slug, manager).to_dict()
            continue
        if choice in {"s", "save"}:
            settings.reset()
            settings.update(working)
            if save_settings(profile.slug, settings, manager):
                output_func("Settings saved.")
            else:
                output_func("Unable to save settings; check file permissions.")
            continue

        try:
            index = int(choice)
        except ValueError:
            output_func("Unknown option. Enter a number, R, S, or B.")
            continue

        if index < 1 or index > len(profile.fields):
            output_func("Select one of the listed fields.")
            continue

        field = profile.fields[index - 1]
        prompt = f"Enter new value for {field.label}: "
        user_input = input_func(prompt)
        try:
            new_value = field.parse_user_value(user_input)
        except ValueError as exc:
            output_func(f"Invalid value: {exc}")
            continue
        try:
            working[field.key] = field.normalise_value(new_value)
        except ValueError as exc:
            output_func(f"Could not update value: {exc}")
            continue
        output_func(f"Updated {field.label}.")


def run_configuration_cli(
    manager: SettingsManager,
    *,
    input_func: InputFunc = input,
    output_func: OutputFunc = print,
) -> None:
    """Launch the configuration manager loop."""

    profiles = get_configuration_profiles()
    if not profiles:
        output_func("\nNo games currently expose configurable settings.")
        input_func("Press Enter to return to the launcher…")
        return

    while True:
        output_func("\nGame configuration manager")
        output_func("===========================")
        for index, profile in enumerate(profiles, start=1):
            output_func(f"{index}. {profile.title} ({profile.slug})")

        output_func("\nOptions: [number] open profile, [slug] open profile, [Q]uit")
        choice = input_func("Select a profile: ").strip()
        if not choice or choice.lower() in {"q", "quit", "exit"}:
            return

        profile: GameConfigurationProfile | None
        if choice.isdigit():
            position = int(choice) - 1
            if position < 0 or position >= len(profiles):
                output_func("Select one of the listed profiles.")
                continue
            profile = profiles[position]
        else:
            profile = get_configuration_profile(choice)
            if profile is None:
                output_func(f"Unknown profile '{choice}'.")
                continue

        _edit_profile(profile, manager, input_func=input_func, output_func=output_func)


__all__ = ["run_configuration_cli"]
