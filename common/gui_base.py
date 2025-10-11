"""Abstract base class and utilities for GUI components.

This module provides reusable GUI components and a common interface for
game GUIs, reducing code duplication and providing consistent behavior.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

try:
    import tkinter as tk
    from tkinter import scrolledtext, ttk

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    # Create placeholder types for type hints
    tk = None  # type: ignore
    scrolledtext = None  # type: ignore
    ttk = None  # type: ignore


@dataclass
class GUIConfig:
    """Configuration options for GUI components.

    Attributes:
        window_title: Title of the main window
        window_width: Width of the window in pixels
        window_height: Height of the window in pixels
        background_color: Background color for the window
        font_family: Default font family
        font_size: Default font size
        log_height: Height of the log widget in lines
        log_width: Width of the log widget in characters
    """

    window_title: str = "Game"
    window_width: int = 800
    window_height: int = 600
    background_color: str = "#FFFFFF"
    font_family: str = "Helvetica"
    font_size: int = 12
    log_height: int = 10
    log_width: int = 60


class BaseGUI(ABC):
    """Abstract base class for game GUIs.

    This class provides common functionality for building game interfaces
    including layout management, logging, and status updates.
    """

    def __init__(self, root: tk.Tk, config: Optional[GUIConfig] = None) -> None:
        """Initialize the base GUI.

        Args:
            root: The root Tkinter window.
            config: Optional configuration for the GUI.
        """
        self.root = root
        self.config = config or GUIConfig()
        self._setup_window()

    def _setup_window(self) -> None:
        """Configure the main window with default settings."""
        self.root.title(self.config.window_title)
        self.root.geometry(f"{self.config.window_width}x{self.config.window_height}")
        if self.config.background_color:
            self.root.configure(bg=self.config.background_color)

    @abstractmethod
    def build_layout(self) -> None:
        """Build the main layout of the GUI.

        This method must be implemented by subclasses to create their
        specific interface components.
        """
        pass

    @abstractmethod
    def update_display(self) -> None:
        """Update the display to reflect the current game state.

        This method must be implemented by subclasses to update their
        specific components based on game state changes.
        """
        pass

    def create_header(self, parent: tk.Widget, text: str) -> tk.Label:
        """Create a standard header label.

        Args:
            parent: Parent widget for the header.
            text: Text to display in the header.

        Returns:
            The created label widget.
        """
        header = tk.Label(
            parent,
            text=text,
            font=(self.config.font_family, self.config.font_size + 6, "bold"),
            pady=8,
        )
        return header

    def create_status_label(self, parent: tk.Widget, text: str = "") -> tk.Label:
        """Create a standard status label.

        Args:
            parent: Parent widget for the label.
            text: Initial text to display.

        Returns:
            The created label widget.
        """
        label = tk.Label(
            parent,
            text=text,
            font=(self.config.font_family, self.config.font_size),
        )
        return label

    def create_log_widget(self, parent: tk.Widget) -> scrolledtext.ScrolledText:
        """Create a standard scrolled text log widget.

        Args:
            parent: Parent widget for the log.

        Returns:
            The created scrolled text widget.
        """
        log = scrolledtext.ScrolledText(
            parent,
            width=self.config.log_width,
            height=self.config.log_height,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Courier New", self.config.font_size - 1),
        )
        return log

    def log_message(self, log_widget: scrolledtext.ScrolledText, message: str) -> None:
        """Append a message to a log widget.

        Args:
            log_widget: The log widget to append to.
            message: The message to append.
        """
        log_widget.configure(state=tk.NORMAL)
        log_widget.insert(tk.END, message + "\n")
        log_widget.see(tk.END)
        log_widget.configure(state=tk.DISABLED)

    def clear_log(self, log_widget: scrolledtext.ScrolledText) -> None:
        """Clear all text from a log widget.

        Args:
            log_widget: The log widget to clear.
        """
        log_widget.configure(state=tk.NORMAL)
        log_widget.delete("1.0", tk.END)
        log_widget.configure(state=tk.DISABLED)

    def create_button_frame(
        self,
        parent: tk.Widget,
        buttons: List[Dict[str, Any]],
    ) -> tk.Frame:
        """Create a frame with multiple buttons.

        Args:
            parent: Parent widget for the button frame.
            buttons: List of button specifications. Each dict should have:
                - 'text': Button text
                - 'command': Button command callback
                - 'state': Optional button state (default: 'normal')

        Returns:
            The created frame containing the buttons.
        """
        frame = tk.Frame(parent)
        for i, btn_spec in enumerate(buttons):
            btn = tk.Button(
                frame,
                text=btn_spec["text"],
                command=btn_spec["command"],
                state=btn_spec.get("state", "normal"),
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        return frame

    def create_label_frame(
        self,
        parent: tk.Widget,
        title: str,
        **pack_options: Any,
    ) -> tk.LabelFrame:
        """Create a labeled frame with standard styling.

        Args:
            parent: Parent widget for the frame.
            title: Title of the labeled frame.
            **pack_options: Additional options to pass to pack().

        Returns:
            The created label frame.
        """
        frame = tk.LabelFrame(
            parent,
            text=title,
            font=(self.config.font_family, self.config.font_size, "bold"),
            padx=10,
            pady=10,
        )
        return frame
