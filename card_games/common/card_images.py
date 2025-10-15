"""Utilities for loading and rendering playing card imagery for GUIs."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Tuple

from card_games.common.cards import Card, Suit

try:
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover - optional dependency
    Image = None  # type: ignore
    ImageTk = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from PyQt5 import QtGui
except ImportError:  # pragma: no cover - optional dependency
    QtGui = None  # type: ignore


CardDimensions = Tuple[int, int]


@dataclass(frozen=True)
class CardImageRequest:
    """Descriptor for a requested card face or back image."""

    key: str
    height: int


class CardImageRepository:
    """Lazy loader and cache for playing card images sourced from SVG-cards.

    The repository exposes helpers for both Tkinter and PyQt widgets so that card
    games can easily render authentic card faces instead of ad-hoc rectangles.
    Images are cached by deck key and target height to avoid reloading the PNG
    assets repeatedly.
    """

    _ASSET_ROOT = Path(__file__).resolve().parent / "assets" / "svg_cards" / "1x"
    _BACK_VARIANT = "back-blue"
    _BASE_DIMENSIONS: CardDimensions = (169, 244)

    def __init__(self, *, back_variant: str | None = None) -> None:
        if Image is None:
            raise RuntimeError("Pillow is required to use CardImageRepository")
        self._back_variant = back_variant or self._BACK_VARIANT
        self._pil_cache: Dict[CardImageRequest, Image.Image] = {}
        self._tk_cache: Dict[CardImageRequest, ImageTk.PhotoImage] = {}
        self._qt_cache: Dict[CardImageRequest, "QtGui.QPixmap"] = {}

    @classmethod
    @lru_cache(maxsize=None)
    def base_dimensions(cls) -> CardDimensions:
        """Return the native width and height of the source assets."""

        return cls._BASE_DIMENSIONS

    def get_tk_image(self, card: Optional[Card], *, height: int, hidden: bool = False) -> ImageTk.PhotoImage:
        """Return a ``PhotoImage`` for use in Tkinter widgets."""

        request = self._image_request(card, height, hidden)
        if request in self._tk_cache:
            return self._tk_cache[request]
        image = self._ensure_pil_image(request)
        photo = ImageTk.PhotoImage(image)
        self._tk_cache[request] = photo
        return photo

    def get_qt_pixmap(self, card: Optional[Card], *, height: int, hidden: bool = False) -> "QtGui.QPixmap":
        """Return a ``QPixmap`` suitable for QLabel/QPushButton widgets."""

        if QtGui is None:
            raise RuntimeError("PyQt5 is required for Qt card imagery")
        request = self._image_request(card, height, hidden)
        if request in self._qt_cache:
            return self._qt_cache[request]
        image = self._ensure_pil_image(request)
        pixmap = QtGui.QPixmap()
        payload = self._image_bytes(image)
        pixmap.loadFromData(payload.getvalue(), "PNG")
        payload.close()
        self._qt_cache[request] = pixmap
        return pixmap

    def _ensure_pil_image(self, request: CardImageRequest) -> Image.Image:
        if request in self._pil_cache:
            return self._pil_cache[request]
        path = self._asset_path(request.key)
        image = Image.open(path).convert("RGBA")
        scale = request.height / image.height
        if scale != 1:
            width = int(round(image.width * scale))
            height = int(round(image.height * scale))
            image = image.resize((width, height), Image.LANCZOS)
        self._pil_cache[request] = image
        return image

    def _asset_path(self, key: str) -> Path:
        path = self._ASSET_ROOT / f"{key}.png"
        if not path.exists():
            raise FileNotFoundError(f"Card asset not found for key '{key}' at {path}")
        return path

    def _image_request(self, card: Optional[Card], height: int, hidden: bool) -> CardImageRequest:
        key = self._back_variant if hidden else self._card_to_key(card)
        return CardImageRequest(key=key, height=height)

    @staticmethod
    def _card_to_key(card: Optional[Card]) -> str:
        if card is None:
            raise ValueError("Card must be provided when hidden is False")
        suit_prefix = {
            Suit.CLUBS: "club",
            Suit.DIAMONDS: "diamond",
            Suit.HEARTS: "heart",
            Suit.SPADES: "spade",
        }[card.suit]
        rank_map = {
            "A": "1",
            "K": "king",
            "Q": "queen",
            "J": "jack",
            "T": "10",
            "9": "9",
            "8": "8",
            "7": "7",
            "6": "6",
            "5": "5",
            "4": "4",
            "3": "3",
            "2": "2",
        }
        try:
            rank_key = rank_map[card.rank]
        except KeyError as exc:  # pragma: no cover - defensive branch for jokers
            raise ValueError(f"Unsupported rank for imagery: {card.rank!r}") from exc
        return f"{suit_prefix}_{rank_key}"

    @staticmethod
    def _image_bytes(image: Image.Image):
        from io import BytesIO

        payload = BytesIO()
        image.save(payload, format="PNG")
        payload.seek(0)
        return payload
