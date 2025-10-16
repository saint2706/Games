"""A common sound effects manager for all games.

This module provides a robust, cross-platform `SoundManager` that uses the
`pygame.mixer` library to play sound effects during gameplay. It is designed
to be resilient, failing gracefully if `pygame` is not installed or if sound
files are missing.

Key features include:
- **Optional Pygame**: The entire sound system is optional. If `pygame` is not
  found, the `SoundManager` will be disabled, but the game will run without
  errors.
- **Dynamic Sound Loading**: Sounds can be loaded from a specified directory
  or added individually.
- **Volume Control**: Master volume can be set for all sounds, and individual
  sounds can be played with a volume override.
- **Enable/Disable**: Sound effects can be toggled on and off at runtime.

The recommended way to create a `SoundManager` is through the
`create_sound_manager` factory function, which handles the check for `pygame`
availability.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional

# Attempt to import pygame, but treat it as an optional dependency.
# This allows the game to run without sound if pygame is not installed.
try:
    import pygame.mixer

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class SoundManager:
    """A class for managing and playing sound effects using `pygame.mixer`.

    This class handles the loading, playing, and management of sound files for
    various game events. It is designed to fail gracefully, so if `pygame` is
    not available or if sound files are missing, it will simply not play
    sounds, rather than crashing the application.

    Attributes:
        sounds_dir: The path to the directory containing the sound files.
        sounds: A dictionary mapping sound type identifiers (e.g., "click",
                "win") to the loaded `pygame.mixer.Sound` objects.
        enabled: A boolean indicating whether sound effects are currently
                 enabled.
        volume: The master volume level for all sounds, from 0.0 to 1.0.
    """

    def __init__(
        self,
        sounds_dir: Optional[str] = None,
        *,
        enabled: bool = True,
        volume: float = 1.0,
        preload: bool = False,
    ) -> None:
        """Initialize the sound manager.

        Args:
            sounds_dir: The directory path containing the sound files. This
                        can be a relative or absolute path.
            enabled: A flag to enable or disable sound effects upon
                     initialization.
            volume: The initial master volume level, from 0.0 (muted) to 1.0
                    (full volume).
            preload: Whether to eagerly load discovered sound files. If False,
                     sounds are loaded lazily upon first playback request.
        """
        self.sounds_dir = Path(sounds_dir) if sounds_dir else None
        self.sounds: Dict[str, "pygame.mixer.Sound"] = {}
        self._sound_paths: Dict[str, Path] = {}
        self.enabled = enabled and PYGAME_AVAILABLE
        self._volume = max(0.0, min(1.0, volume))
        self._initialized = False

        if self.sounds_dir and self.sounds_dir.exists():
            self._sound_paths = self._discover_sound_files()

        if PYGAME_AVAILABLE and self.enabled and self.sounds_dir:
            self._initialize_mixer()
            if preload:
                self._load_sounds()

    def _initialize_mixer(self) -> None:
        """Initialize the pygame mixer when available."""
        if self._initialized or not PYGAME_AVAILABLE or not self.enabled:
            return

        try:
            pygame.mixer.init()
            self._initialized = True
        except Exception as exc:  # pragma: no cover - depends on pygame setup
            print(f"Warning: Could not initialize pygame mixer: {exc}")
            self.enabled = False

    def _ensure_initialized(self) -> bool:
        """Ensure the pygame mixer is ready for use."""
        if not PYGAME_AVAILABLE or not self.enabled:
            return False

        if not self._initialized:
            self._initialize_mixer()

        return self._initialized

    def _discover_sound_files(self) -> Dict[str, Path]:
        """Discover sound files within the configured directory."""
        if not self.sounds_dir:
            return {}

        sound_paths: Dict[str, Path] = {}
        for extension in ("*.wav", "*.mp3"):
            for filepath in self.sounds_dir.glob(extension):
                sound_paths[filepath.stem] = filepath

        return sound_paths

    def _load_sounds(self, sound_types: Optional[Iterable[str]] = None) -> None:
        """Load sound files from the specified sounds directory."""
        if not self.sounds_dir or not self.sounds_dir.exists() or not self._ensure_initialized():
            return

        to_load = sound_types if sound_types is not None else self._sound_paths.keys()

        for sound_type in to_load:
            if sound_type in self.sounds:
                continue

            filepath = self._sound_paths.get(sound_type)
            if not filepath:
                continue

            try:
                self.sounds[sound_type] = pygame.mixer.Sound(str(filepath))
            except Exception as exc:
                # Log a warning if a specific sound file fails to load
                print(f"Warning: Could not load {filepath.name}: {exc}")

    def _ensure_sound_loaded(self, sound_type: str) -> None:
        """Load a sound on demand when it is requested for playback."""
        if sound_type in self.sounds:
            return

        self._load_sounds([sound_type])

    def add_sound(self, sound_type: str, filepath: str) -> bool:
        """Add a specific sound file to the manager.

        Args:
            sound_type: A unique identifier for the sound (e.g., "explosion").
            filepath: The path to the sound file.

        Returns:
            True if the sound was loaded successfully, False otherwise.
        """
        path = Path(filepath)
        self._sound_paths[sound_type] = path

        if not self.is_available() or not self._ensure_initialized():
            return False

        try:
            self.sounds[sound_type] = pygame.mixer.Sound(str(path))
            return True
        except Exception as exc:
            print(f"Warning: Could not load sound file {filepath}: {exc}")
            return False

    def play(self, sound_type: str, volume: Optional[float] = None) -> bool:
        """Play a sound effect.

        Args:
            sound_type: The identifier of the sound to play.
            volume: An optional volume override for this specific playback,
                    from 0.0 to 1.0. If not provided, the master volume is
                    used.

        Returns:
            True if the sound was played successfully, False otherwise.
        """
        if not self.is_available():
            return False

        self._ensure_sound_loaded(sound_type)

        if sound_type not in self.sounds:
            return False

        try:
            sound = self.sounds[sound_type]
            # Use the override volume if provided, otherwise use the master volume
            play_volume = volume if volume is not None else self._volume
            play_volume = max(0.0, min(1.0, play_volume))
            sound.set_volume(play_volume)
            sound.play()
            return True
        except Exception:
            # Fail silently if there's an issue during playback
            return False

    def stop(self, sound_type: Optional[str] = None) -> None:
        """Stop playing a specific sound or all sounds.

        Args:
            sound_type: The identifier of the sound to stop. If None, all
                        currently playing sounds will be stopped.
        """
        if not self.is_available():
            return

        try:
            if sound_type and sound_type in self.sounds:
                self.sounds[sound_type].stop()
            elif sound_type is None:
                pygame.mixer.stop()
        except Exception:
            # Fail silently if there's an issue stopping the sound
            pass

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable all sound effects.

        Args:
            enabled: Set to True to enable sounds, False to disable them.
        """
        self.enabled = enabled and PYGAME_AVAILABLE

    def set_volume(self, volume: float) -> None:
        """Set the master volume for all sounds.

        Args:
            volume: The new volume level, from 0.0 (muted) to 1.0 (full).
        """
        self._volume = max(0.0, min(1.0, volume))

        if not self.is_available():
            return

        # Update the volume of all loaded sounds
        for sound in self.sounds.values():
            try:
                sound.set_volume(self._volume)
            except Exception:
                pass

    def get_volume(self) -> float:
        """Get the current master volume level.

        Returns:
            The current volume level, from 0.0 to 1.0.
        """
        return self._volume

    def is_available(self) -> bool:
        """Check if the sound system is available and enabled.

        Returns:
            True if `pygame` is available and sounds are currently enabled,
            False otherwise.
        """
        return PYGAME_AVAILABLE and self.enabled

    def list_sounds(self) -> list[str]:
        """Get a list of all loaded sound types.

        Returns:
            A list of the string identifiers for all loaded sounds.
        """
        return list(self.sounds.keys())

    def available_sounds(self) -> list[str]:
        """Get a list of all discovered sound identifiers."""
        return sorted(set(self._sound_paths.keys()) | set(self.sounds.keys()))


def create_sound_manager(
    sounds_dir: Optional[str] = None,
    enabled: bool = True,
    volume: float = 1.0,
    *,
    preload: bool = False,
) -> Optional[SoundManager]:
    """A factory function to create a `SoundManager` instance.

    This is the recommended way to create a sound manager, as it handles the
    case where `pygame` is not available.

    Args:
        sounds_dir: An optional directory path for the sound files.
        enabled: A flag to enable or disable sound effects.
        volume: The initial master volume level, from 0.0 to 1.0.
        preload: Whether to eagerly load discovered sound files.

    Returns:
        A `SoundManager` instance if `pygame` is available, otherwise `None`.
    """
    if not PYGAME_AVAILABLE:
        return None

    return SoundManager(sounds_dir, enabled=enabled, volume=volume, preload=preload)
