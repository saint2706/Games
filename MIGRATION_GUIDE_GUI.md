# GUI Enhancements Migration Guide

This guide helps you migrate existing game GUIs to use the new enhancement features.

## Overview

The GUI enhancements provide:
- **Theme System**: Unified color schemes and theming
- **Sound Manager**: Cross-platform sound effects
- **Animations**: Smooth visual transitions
- **Accessibility**: High contrast, screen readers, keyboard navigation
- **Internationalization**: Multi-language support
- **Keyboard Shortcuts**: Centralized shortcut management

## Step-by-Step Migration

### Step 1: Update Imports

**Before:**
```python
import tkinter as tk
from tkinter import ttk
```

**After:**
```python
import tkinter as tk
from tkinter import ttk
from common.gui_base import BaseGUI, GUIConfig
from common.i18n import _
```

### Step 2: Update Class Definition

**Before:**
```python
class MyGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Game")
        self.root.geometry("800x600")
```

**After:**
```python
class MyGameGUI(BaseGUI):
    def __init__(self, root):
        config = GUIConfig(
            window_title="My Game",
            window_width=800,
            window_height=600,
            enable_sounds=True,
            enable_animations=True,
            theme_name="light",
            language="en",
        )
        super().__init__(root, config)
        self.build_layout()
```

### Step 3: Implement Required Methods

**Add these methods to your class:**

```python
def build_layout(self):
    """Build the GUI layout."""
    # Your existing GUI building code goes here
    pass

def update_display(self):
    """Update display based on state changes."""
    # Your existing update code goes here
    pass

def _setup_shortcuts(self):
    """Set up keyboard shortcuts."""
    self.register_shortcut("<Control-n>", self.new_game, "New Game")
    self.register_shortcut("<F1>", self.show_help, "Show Help")
```

### Step 4: Replace Hardcoded Colors with Theme Colors

**Before:**
```python
button = tk.Button(
    parent,
    text="Click Me",
    bg="#FFFFFF",
    fg="#000000",
)
```

**After:**
```python
button = tk.Button(
    parent,
    text=_("click_me"),  # Also added translation
    bg=self.current_theme.colors.button_bg,
    fg=self.current_theme.colors.button_fg,
)
```

### Step 5: Add Translations to Text

**Before:**
```python
label = tk.Label(root, text="New Game")
title = tk.Label(root, text="Score: 100")
```

**After:**
```python
label = tk.Label(root, text=_("new_game"))
title = tk.Label(root, text=_("score_display", score=100))
```

### Step 6: Add Sound Effects

**If you want to add sound effects:**

```python
def play_card(self):
    """Play a card with sound effect."""
    # Your card playing logic
    self.play_sound("card_play", volume=0.8)

def win_game(self):
    """Handle game win with sound."""
    # Your win logic
    self.play_sound("win")
```

### Step 7: Add Animations

**For visual feedback:**

```python
from common.animations import animate_widget_highlight

def make_move(self):
    """Make a move with animation."""
    # Your move logic
    if self.config.enable_animations:
        animate_widget_highlight(self.move_button)
```

### Step 8: Add Accessibility Features

**For better accessibility:**

```python
def build_layout(self):
    # Create buttons with accessibility
    button = tk.Button(parent, text=_("new_game"), command=self.new_game)
    
    # Add focus indicators and screen reader support
    self.accessibility_manager.add_focus_indicator(button)
    self.accessibility_manager.add_screen_reader_label(
        button,
        _("start_new_game_description")
    )
```

## Complete Migration Example

### Before (Old Code)

```python
import tkinter as tk

class BlackjackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.configure(bg="#FFFFFF")
        self.setup_gui()
    
    def setup_gui(self):
        # Title
        title = tk.Label(
            self.root,
            text="Blackjack",
            font=("Arial", 24, "bold"),
            bg="#FFFFFF",
            fg="#000000",
        )
        title.pack(pady=20)
        
        # Deal button
        self.deal_button = tk.Button(
            self.root,
            text="Deal",
            command=self.deal_cards,
            bg="#E0E0E0",
            fg="#000000",
        )
        self.deal_button.pack(pady=10)
    
    def deal_cards(self):
        print("Dealing cards...")

def main():
    app = BlackjackGUI()
    app.root.mainloop()
```

### After (Migrated Code)

```python
import tkinter as tk
from common.gui_base import BaseGUI, GUIConfig
from common.i18n import _
from common.animations import animate_widget_highlight

class BlackjackGUI(BaseGUI):
    def __init__(self, root):
        config = GUIConfig(
            window_title="blackjack",
            window_width=800,
            window_height=600,
            enable_sounds=True,
            enable_animations=True,
            theme_name="light",
            language="en",
        )
        super().__init__(root, config)
        self.build_layout()
    
    def build_layout(self):
        """Build the GUI layout."""
        # Title with theme colors
        title = tk.Label(
            self.root,
            text=_("blackjack"),
            font=(self.current_theme.font_family, 24, "bold"),
            bg=self.current_theme.colors.background,
            fg=self.current_theme.colors.foreground,
        )
        title.pack(pady=20)
        
        # Deal button with theme colors
        self.deal_button = tk.Button(
            self.root,
            text=_("deal"),
            command=self.deal_cards,
            bg=self.current_theme.colors.button_bg,
            fg=self.current_theme.colors.button_fg,
        )
        self.deal_button.pack(pady=10)
        
        # Add accessibility
        self.accessibility_manager.add_focus_indicator(self.deal_button)
        self.accessibility_manager.add_screen_reader_label(
            self.deal_button,
            _("deal_cards_description")
        )
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts."""
        self.register_shortcut("<Control-d>", self.deal_cards, "Deal Cards")
        self.register_shortcut("<F1>", self.show_shortcuts_help, "Show Help")
    
    def deal_cards(self):
        """Deal cards with sound and animation."""
        print("Dealing cards...")
        
        # Play sound
        self.play_sound("card_deal")
        
        # Animate button
        if self.config.enable_animations:
            animate_widget_highlight(self.deal_button)
        
        # Announce for screen reader
        self.accessibility_manager.announce(_("cards_dealt"))
    
    def update_display(self):
        """Update display when theme changes."""
        if hasattr(self, 'deal_button'):
            self.deal_button.config(
                bg=self.current_theme.colors.button_bg,
                fg=self.current_theme.colors.button_fg,
            )

def main():
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

## Benefits of Migration

After migration, your GUI will have:

1. ✅ **Theme Support**: Users can switch between light/dark/high contrast themes
2. ✅ **Sound Effects**: Enhanced user experience with audio feedback
3. ✅ **Animations**: Smooth visual transitions and highlights
4. ✅ **Accessibility**: Support for screen readers and high contrast
5. ✅ **Multi-language**: Easy to add support for multiple languages
6. ✅ **Keyboard Shortcuts**: Power users can use keyboard navigation
7. ✅ **Responsive Design**: Better window resizing behavior
8. ✅ **Consistent Style**: Unified look across all games

## Adding Translations

Create a translations file for your game:

```python
from common.i18n import get_translation_manager

# Add translations
i18n = get_translation_manager()

# English (default)
i18n.add_translation("en", "blackjack", "Blackjack")
i18n.add_translation("en", "deal", "Deal")
i18n.add_translation("en", "hit", "Hit")
i18n.add_translation("en", "stand", "Stand")

# Spanish
i18n.add_translation("es", "blackjack", "Veintiuno")
i18n.add_translation("es", "deal", "Repartir")
i18n.add_translation("es", "hit", "Pedir")
i18n.add_translation("es", "stand", "Plantarse")

# Save translations
i18n.save_translations("es")
```

## Adding Sound Files

Organize your sound files:

```
your_game/
├── sounds/
│   ├── card_deal.wav
│   ├── win.wav
│   ├── lose.wav
│   └── button_click.wav
```

Then initialize with sound directory:

```python
config = GUIConfig(
    # ... other config
    enable_sounds=True,
)

# Sound manager will be auto-initialized
# You can also set a custom sounds directory
if self.sound_manager:
    self.sound_manager.add_sound("custom_sound", "path/to/sound.wav")
```

## Testing Your Migrated GUI

After migration, test:

1. ✅ Theme switching works (light → dark → high contrast)
2. ✅ Sounds play (if pygame installed and sound files present)
3. ✅ Animations run smoothly
4. ✅ Keyboard shortcuts work (F1 shows help)
5. ✅ Window resizes properly
6. ✅ All text is translatable
7. ✅ High contrast mode works

## Troubleshooting

### Import Errors

If you get import errors:
```python
from common import GUI_ENHANCEMENTS_AVAILABLE

if not GUI_ENHANCEMENTS_AVAILABLE:
    print("Warning: GUI enhancements not available")
```

### Theme Not Applying

Make sure to call `self.apply_theme()` after initialization or use `self.set_theme(name)` to change themes.

### Sounds Not Playing

Check:
1. pygame is installed: `pip install pygame`
2. Sound files exist in the sounds directory
3. Sound manager is enabled: `self.sound_manager.is_available()`

### Animations Not Working

Ensure:
1. `enable_animations=True` in GUIConfig
2. tkinter is available (it should be)
3. Widgets are properly created before animating

## Additional Resources

- [GUI Enhancements Documentation](common/GUI_ENHANCEMENTS.md)
- [Demo Application](examples/gui_enhancements_demo.py)
- [Test Suite](tests/test_gui_enhancements.py)
- [BaseGUI API](common/gui_base.py)

## Need Help?

If you encounter issues during migration:

1. Check the demo application for working examples
2. Review the test suite for usage patterns
3. Read the comprehensive documentation
4. Look at existing migrated games (e.g., Uno)

Happy migrating! 🎮✨
