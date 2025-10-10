# Uno Sound Effects Implementation Guide

## Overview

This guide explains how to add sound effects to the Uno game. Sound effects enhance the user experience by providing audio feedback for game events.

## Sound Architecture

The sound system is designed to be:
- **Optional**: Can be disabled without affecting gameplay
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Non-blocking**: Sounds play asynchronously
- **Extensible**: Easy to add new sounds

## Sound Hooks

The game engine calls `interface.play_sound(sound_type)` at key events:

### Game Events and Sound Types

| Event | Sound Type | Description |
|-------|-----------|-------------|
| Card played | `"card_play"` | Regular card play |
| Wild card | `"wild"` | Wild card played |
| Skip card | `"skip"` | Skip action card |
| Reverse card | `"reverse"` | Reverse action card |
| +2 or +4 card | `"draw_penalty"` | Draw penalty card |
| UNO called | `"uno"` | Player declares UNO |
| Player wins | `"win"` | Victory sound |
| Hand swap (7) | `"swap"` | 7-0 rule: hands swapped |
| Hand rotate (0) | `"rotate"` | 7-0 rule: hands rotated |
| Card drawn | `"draw"` | Player draws a card |

## Implementation Options

### Option 1: pygame (Recommended)

**Advantages**: Cross-platform, simple API, reliable
**Installation**: `pip install pygame`

```python
import pygame
from pathlib import Path

class SoundManager:
    """Manages sound effects using pygame.mixer."""
    
    def __init__(self, sounds_dir: str = "sounds/"):
        pygame.mixer.init()
        self.sounds_dir = Path(sounds_dir)
        self.sounds = {}
        self.enabled = True
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound files from the sounds directory."""
        sound_files = {
            "card_play": "card_play.wav",
            "wild": "wild.wav",
            "skip": "skip.wav",
            "reverse": "reverse.wav",
            "draw_penalty": "draw_penalty.wav",
            "uno": "uno.wav",
            "win": "win.wav",
            "swap": "swap.wav",
            "rotate": "rotate.wav",
            "draw": "draw.wav",
        }
        
        for sound_type, filename in sound_files.items():
            filepath = self.sounds_dir / filename
            if filepath.exists():
                try:
                    self.sounds[sound_type] = pygame.mixer.Sound(str(filepath))
                except pygame.error as e:
                    print(f"Warning: Could not load {filename}: {e}")
    
    def play(self, sound_type: str, volume: float = 1.0):
        """Play a sound effect.
        
        Args:
            sound_type: Type of sound to play
            volume: Volume level (0.0 to 1.0)
        """
        if not self.enabled or sound_type not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_type]
            sound.set_volume(volume)
            sound.play()
        except Exception as e:
            print(f"Error playing sound {sound_type}: {e}")
    
    def set_enabled(self, enabled: bool):
        """Enable or disable sound effects."""
        self.enabled = enabled
    
    def set_volume(self, volume: float):
        """Set master volume for all sounds (0.0 to 1.0)."""
        for sound in self.sounds.values():
            sound.set_volume(volume)
```

**Integration with TkUnoInterface**:

```python
class TkUnoInterface(UnoInterface):
    def __init__(self, root: tk.Tk, players: Sequence[UnoPlayer], 
                 *, enable_sounds: bool = False):
        # ... existing initialization ...
        self.enable_sounds = enable_sounds
        if enable_sounds:
            self.sound_manager = SoundManager()
        else:
            self.sound_manager = None
    
    def play_sound(self, sound_type: str) -> None:
        """Play a sound effect."""
        if self.sound_manager:
            self.sound_manager.play(sound_type)
```

### Option 2: playsound (Simple)

**Advantages**: Very simple, no dependencies
**Installation**: `pip install playsound`

```python
from playsound import playsound
import threading

class SimpleSoundManager:
    """Simple sound manager using playsound."""
    
    def __init__(self, sounds_dir: str = "sounds/"):
        self.sounds_dir = Path(sounds_dir)
        self.enabled = True
    
    def play(self, sound_type: str):
        """Play a sound effect asynchronously."""
        if not self.enabled:
            return
        
        filepath = self.sounds_dir / f"{sound_type}.wav"
        if filepath.exists():
            # Play in separate thread to avoid blocking
            threading.Thread(
                target=playsound,
                args=(str(filepath),),
                daemon=True
            ).start()
```

### Option 3: Platform-Specific

#### Windows (winsound)

```python
import winsound
import threading

class WindowsSoundManager:
    """Sound manager for Windows using winsound."""
    
    def play(self, sound_type: str):
        filepath = f"sounds/{sound_type}.wav"
        threading.Thread(
            target=winsound.PlaySound,
            args=(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC),
            daemon=True
        ).start()
```

#### macOS (afplay)

```python
import subprocess

class MacSoundManager:
    """Sound manager for macOS using afplay."""
    
    def play(self, sound_type: str):
        filepath = f"sounds/{sound_type}.wav"
        subprocess.Popen(['afplay', filepath])
```

#### Linux (aplay)

```python
import subprocess

class LinuxSoundManager:
    """Sound manager for Linux using aplay."""
    
    def play(self, sound_type: str):
        filepath = f"sounds/{sound_type}.wav"
        subprocess.Popen(['aplay', filepath])
```

## Sound File Format

- **Format**: WAV (recommended) or MP3
- **Sample Rate**: 44100 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono or Stereo
- **Duration**: 0.5-2 seconds for most effects

## Creating Sound Effects

### Using Free Tools

1. **Audacity** (Free, cross-platform)
   - Record custom sounds
   - Apply effects
   - Export as WAV

2. **LMMS** (Free music creation)
   - Create synthetic sounds
   - Use built-in instruments

3. **Bfxr** (Free web-based)
   - Generate retro game sounds
   - Great for card play effects

### Free Sound Resources

- **Freesound.org**: Community sound library
- **Zapsplat.com**: Free sound effects
- **SoundBible.com**: Public domain sounds

### Recommended Sounds

| Sound Type | Suggestion |
|-----------|------------|
| `card_play` | Light tap or slide sound |
| `wild` | Magical chime |
| `skip` | Quick whoosh |
| `reverse` | Rewind sound effect |
| `draw_penalty` | Descending tones |
| `uno` | Voice saying "UNO!" |
| `win` | Victory fanfare |
| `swap` | Shuffle/swap sound |
| `rotate` | Rotation whoosh |

## Configuration

Add sound settings to the game:

```python
# settings.py or config
SOUND_SETTINGS = {
    "enabled": True,
    "volume": 0.7,
    "sounds_dir": "card_games/uno/sounds/",
    "sound_files": {
        "card_play": "card_play.wav",
        "wild": "wild.wav",
        # ... other sounds
    }
}
```

## GUI Sound Controls

Add sound controls to the GUI:

```python
class TkUnoInterface(UnoInterface):
    def _build_settings_menu(self):
        """Add settings menu with sound controls."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Sound toggle
        self.sound_enabled = tk.BooleanVar(value=self.enable_sounds)
        settings_menu.add_checkbutton(
            label="Enable Sounds",
            variable=self.sound_enabled,
            command=self._toggle_sounds
        )
        
        # Volume slider
        settings_menu.add_separator()
        volume_frame = tk.Frame(self.root)
        tk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT)
        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self._change_volume
        )
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT)
    
    def _toggle_sounds(self):
        """Toggle sound effects on/off."""
        if self.sound_manager:
            self.sound_manager.set_enabled(self.sound_enabled.get())
    
    def _change_volume(self, value):
        """Change master volume."""
        if self.sound_manager:
            self.sound_manager.set_volume(int(value) / 100.0)
```

## Command-Line Usage

```bash
# Enable sounds
python -m card_games.uno --gui --sounds

# Disable sounds
python -m card_games.uno --gui --no-sounds

# Set volume
python -m card_games.uno --gui --sounds --volume 0.5
```

## Testing

```python
# test_sounds.py
def test_sound_manager():
    """Test all sound effects."""
    manager = SoundManager("sounds/")
    
    sounds_to_test = [
        "card_play", "wild", "skip", "reverse",
        "draw_penalty", "uno", "win", "swap", "rotate"
    ]
    
    for sound in sounds_to_test:
        print(f"Testing {sound}...")
        manager.play(sound)
        time.sleep(1)

if __name__ == "__main__":
    test_sound_manager()
```

## Performance Considerations

1. **Preload sounds**: Load all sounds at startup to avoid delays
2. **Limit concurrent sounds**: Don't play too many sounds simultaneously
3. **Sound pooling**: Reuse sound objects instead of creating new ones
4. **Async playback**: Always play sounds asynchronously to avoid blocking

## Troubleshooting

### Common Issues

**Sound not playing**:
- Check file exists and path is correct
- Verify file format is supported
- Check system volume is not muted

**Delayed playback**:
- Preload sounds at startup
- Use smaller file sizes
- Use async playback

**Crackling or distortion**:
- Check sample rate matches system
- Reduce file size
- Adjust buffer size in pygame.mixer.init()

### Debug Mode

```python
class SoundManager:
    def __init__(self, sounds_dir: str = "sounds/", debug: bool = False):
        self.debug = debug
        # ... rest of init
    
    def play(self, sound_type: str, volume: float = 1.0):
        if self.debug:
            print(f"Playing sound: {sound_type} at volume {volume}")
        # ... rest of play logic
```

## Future Enhancements

- Music background tracks
- Voice announcements
- Positional audio (stereo panning based on player position)
- Custom sound themes
- Sound effect variations (randomize from multiple files)
- Volume fade in/out
- Sound effects for network events (player joined, disconnected)
