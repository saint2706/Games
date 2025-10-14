---
applyTo: "**/gui.py"
---

# GUI Implementation Requirements

When implementing or modifying GUI files, follow these guidelines:

## Framework

- **Primary**: Tkinter (pre-installed with Python)
- **Alternative**: PyQt5 (for advanced features, already in dependencies)
- **Base Class**: Inherit from `BaseGUI` in `common/gui_base.py`

## GUI Structure

Every GUI should follow this pattern:

```python
from __future__ import annotations

from common import BaseGUI
import tkinter as tk
from typing import Optional

class MyGameGUI(BaseGUI):
    """GUI for MyGame.
    
    Provides graphical interface for playing MyGame with:
    - Visual game board
    - Interactive controls
    - Score display
    - AI opponent support
    """
    
    def __init__(self):
        """Initialize GUI components."""
        super().__init__()
        self.game = None
        self.setup_window("My Game", 800, 600)
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout GUI widgets."""
        # Use helper methods from BaseGUI
        self.create_board()
        self.create_controls()
        self.create_status_display()
    
    def update_display(self):
        """Update GUI to reflect current game state."""
        # Refresh visual elements
        pass
```

## Key Principles

1. **Separation of Concerns**: Keep game logic separate from GUI code
1. **Observer Pattern**: Use events to synchronize GUI with game state
1. **Responsive**: GUI should remain responsive during AI moves
1. **Error Handling**: Gracefully handle and display errors

## Required Components

### Window Setup

```python
def setup_window(self, title: str, width: int, height: int):
    """Set up main window with proper configuration."""
    self.window = tk.Tk()
    self.window.title(title)
    self.window.geometry(f"{width}x{height}")
    self.window.resizable(False, False)
```

### Board Display

```python
def create_board(self):
    """Create visual game board."""
    self.board_frame = tk.Frame(self.window)
    self.board_frame.pack(side=tk.LEFT, padx=10, pady=10)
    # Create board elements
```

### Controls

```python
def create_controls(self):
    """Create game control buttons."""
    self.control_frame = tk.Frame(self.window)
    self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    
    tk.Button(
        self.control_frame,
        text="New Game",
        command=self.new_game
    ).pack(pady=5)
    
    tk.Button(
        self.control_frame,
        text="Quit",
        command=self.quit_game
    ).pack(pady=5)
```

### Status Display

```python
def create_status_display(self):
    """Create status message area."""
    self.status_var = tk.StringVar(value="Welcome to MyGame!")
    self.status_label = tk.Label(
        self.window,
        textvariable=self.status_var,
        font=("Arial", 12)
    )
    self.status_label.pack(side=tk.BOTTOM, pady=10)
```

## Event Handling

### Mouse Clicks

```python
def on_board_click(self, event):
    """Handle mouse click on game board."""
    x, y = event.x, event.y
    # Convert to board coordinates
    row, col = self.pixel_to_board(x, y)
    # Process move
    self.handle_move(row, col)
```

### Keyboard Input

```python
def setup_keyboard_bindings(self):
    """Bind keyboard shortcuts."""
    self.window.bind('<Escape>', lambda e: self.quit_game())
    self.window.bind('<n>', lambda e: self.new_game())
    self.window.bind('<h>', lambda e: self.show_help())
```

## Visual Guidelines

1. **Colors**: Use consistent color scheme
   - Consider colorblind-friendly palettes
   - Maintain good contrast ratios
1. **Fonts**: Use readable fonts (Arial, Helvetica) at appropriate sizes
1. **Layout**: Keep interface clean and uncluttered
1. **Feedback**: Provide immediate visual feedback for actions

## Accessibility

- Support keyboard navigation
- Provide tooltips for buttons
- Use descriptive labels
- Ensure color is not the only indicator

## Threading

For AI moves, use threading to keep GUI responsive:

```python
import threading

def ai_move(self):
    """Execute AI move in separate thread."""
    def _ai_move_thread():
        move = self.game.get_ai_move()
        # Use after() to update GUI from main thread
        self.window.after(0, lambda: self.apply_move(move))
    
    thread = threading.Thread(target=_ai_move_thread)
    thread.daemon = True
    thread.start()
```

## Error Handling

```python
def handle_error(self, error: Exception):
    """Display error message to user."""
    import tkinter.messagebox as messagebox
    messagebox.showerror(
        "Error",
        f"An error occurred: {str(error)}"
    )
```

## Resource Management

- Clean up resources properly
- Cancel pending callbacks on window close
- Release locks and threads

```python
def quit_game(self):
    """Clean up and close window."""
    # Cancel any pending after() calls
    # Stop threads
    # Close resources
    self.window.destroy()
```

## Testing

- Test GUI components with pytest-qt
- Test user interactions
- Test error conditions
- Test with different screen sizes/resolutions

## Documentation

- Document all GUI methods with clear docstrings
- Include screenshots in game README
- Document keyboard shortcuts
- Explain GUI features in module docstring
