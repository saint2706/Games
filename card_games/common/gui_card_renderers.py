"""Reusable helpers for rendering playing cards in GUI toolkits."""

from __future__ import annotations

from typing import Callable, Collection, Optional, Sequence

from card_games.common.card_images import CardImageRepository
from card_games.common.cards import Card

try:  # pragma: no cover - optional dependency guards
    from tkinter import Misc, Button, Label  # type: ignore
except Exception:  # pragma: no cover - optional dependency guards
    Misc = Button = Label = None  # type: ignore

try:  # pragma: no cover - optional dependency guards
    from PyQt5 import QtGui, QtWidgets  # type: ignore
except Exception:  # pragma: no cover - optional dependency guards
    QtGui = QtWidgets = None  # type: ignore


_TkClickHandler = Callable[[int, Optional[Card]], None]
_QtClickHandler = Callable[[int, Optional[Card]], None]


def _normalize_hidden(hidden: Collection[int] | Callable[[int, Optional[Card]], bool] | None, index: int, card: Optional[Card]) -> bool:
    if hidden is None:
        return False
    if callable(hidden):
        return hidden(index, card)
    return index in hidden


def render_tk_card_strip(
    container: "Misc",
    *,
    repository: CardImageRepository,
    cards: Sequence[Optional[Card]],
    card_height: int = 120,
    spacing: int = 6,
    hidden: Collection[int] | Callable[[int, Optional[Card]], bool] | None = None,
    background: str | None = None,
    clickable: bool = False,
    command: _TkClickHandler | None = None,
    selected: Collection[int] | Callable[[int, Optional[Card]], bool] | None = None,
    selected_color: str = "#facc15",
) -> None:
    """Render a horizontal strip of playing card images within a Tk container."""

    if Misc is None:
        raise RuntimeError("Tkinter is required for render_tk_card_strip")

    for child in list(container.winfo_children()):
        child.destroy()

    bg = background or (container.cget("bg") if hasattr(container, "cget") else None)
    images: list = []

    for index, card in enumerate(cards):
        hidden_flag = _normalize_hidden(hidden, index, card)
        image = repository.get_tk_image(None if hidden_flag else card, height=card_height, hidden=hidden_flag)
        widget_cls = Button if clickable and command else Label
        widget = widget_cls(container)
        widget.configure(image=image, borderwidth=0, highlightthickness=0)
        if bg is not None:
            widget.configure(background=bg, activebackground=bg)
        if command:
            widget.configure(command=lambda idx=index, value=card: command(idx, value))
        if selected is not None and _normalize_hidden(selected, index, card):
            widget.configure(highlightthickness=3, highlightbackground=selected_color, highlightcolor=selected_color)
        widget.image = image  # type: ignore[attr-defined]
        widget.pack(side="left", padx=spacing, pady=4)
        images.append(image)

    container._card_images = images  # type: ignore[attr-defined]


def _clear_qt_layout(layout: "QtWidgets.QLayout") -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()


def render_qt_card_strip(
    container: "QtWidgets.QWidget",
    *,
    repository: CardImageRepository,
    cards: Sequence[Optional[Card]],
    card_height: int = 120,
    spacing: int = 6,
    hidden: Collection[int] | Callable[[int, Optional[Card]], bool] | None = None,
    clickable: bool = False,
    command: _QtClickHandler | None = None,
    selected: Collection[int] | Callable[[int, Optional[Card]], bool] | None = None,
    selected_color: str = "#facc15",
) -> None:
    """Render a row of playing card images inside a Qt widget."""

    if QtWidgets is None:
        raise RuntimeError("PyQt5 is required for render_qt_card_strip")

    layout = container.layout()
    if layout is None:
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing)
    else:
        _clear_qt_layout(layout)
        layout.setSpacing(spacing)

    pixmaps: list = []

    for index, card in enumerate(cards):
        hidden_flag = _normalize_hidden(hidden, index, card)
        pixmap = repository.get_qt_pixmap(None if hidden_flag else card, height=card_height, hidden=hidden_flag)
        if clickable and command:
            widget = QtWidgets.QPushButton(container)
            widget.setFlat(True)
            widget.setIconSize(pixmap.size())
            widget.setIcon(QtGui.QIcon(pixmap))  # type: ignore[attr-defined]
            widget.setCheckable(True)
            if selected is not None and _normalize_hidden(selected, index, card):
                widget.setChecked(True)
                widget.setStyleSheet(f"QPushButton:checked {{ border: 2px solid {selected_color}; }}")
            else:
                widget.setChecked(False)
                widget.setStyleSheet("QPushButton { border: none; }")
            widget.setProperty("card_index", index)
            widget.clicked.connect(lambda _=False, idx=index, value=card: command(idx, value))
        else:
            widget = QtWidgets.QLabel(container)
            widget.setPixmap(pixmap)
        layout.addWidget(widget)
        pixmaps.append(pixmap)

    container._card_pixmaps = pixmaps  # type: ignore[attr-defined]
