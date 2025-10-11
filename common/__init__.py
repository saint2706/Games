"""Common utilities and architecture components for all games.

This package provides shared functionality including:
- Event-driven architecture
- Plugin system
- Save/load functionality
- Settings management
- Replay/undo system
- Observer pattern for GUI synchronization
- Game engine abstractions
- Educational features (tutorials, strategy tips, probability calculators)
- Enhanced CLI utilities
- GUI enhancements (themes, sounds, animations, accessibility, i18n, shortcuts)
"""

from .ai_strategy import AIStrategy, HeuristicStrategy, MinimaxStrategy, RandomStrategy
from .architecture.engine import GameEngine, GamePhase, GameState
from .architecture.events import Event, EventBus, EventHandler, FunctionEventHandler
from .architecture.observer import Observable, Observer, PropertyObservable
from .architecture.persistence import (
    GameStateSerializer,
    JSONSerializer,
    PickleSerializer,
    SaveLoadManager,
)
from .architecture.plugin import GamePlugin, PluginManager, PluginMetadata
from .architecture.replay import ReplayAction, ReplayManager, ReplayRecorder
from .architecture.settings import Settings, SettingsManager
from .challenges import Challenge, ChallengePack, ChallengeManager, DifficultyLevel, get_default_challenge_manager
from .educational import (
    AIExplainer,
    GameTheoryExplanation,
    GameTheoryExplainer,
    ProbabilityCalculator,
    StrategyTip,
    StrategyTipProvider,
    TutorialMode,
    TutorialStep,
)
from .cli_utils import (
    ASCIIArt,
    Color,
    CommandHistory,
    InteractiveMenu,
    ProgressBar,
    RichText,
    Spinner,
    THEMES,
    TextStyle,
    Theme,
    clear_screen,
    get_terminal_size,
)

# GUI enhancement imports (optional, only if tkinter available)
try:
    from .themes import ThemeConfig, ThemeManager, get_theme_manager
    from .sound_manager import SoundManager, create_sound_manager
    from .accessibility import AccessibilityManager, get_accessibility_manager
    from .i18n import TranslationManager, get_translation_manager, _, set_language
    from .keyboard_shortcuts import KeyboardShortcut, ShortcutManager, get_shortcut_manager

    GUI_ENHANCEMENTS_AVAILABLE = True
except ImportError:
    GUI_ENHANCEMENTS_AVAILABLE = False

__all__ = [
    # Core abstractions
    "GameEngine",
    "GameState",
    "GamePhase",
    # AI Strategy
    "AIStrategy",
    "RandomStrategy",
    "MinimaxStrategy",
    "HeuristicStrategy",
    # Event system
    "Event",
    "EventBus",
    "EventHandler",
    "FunctionEventHandler",
    # Observer pattern
    "Observable",
    "Observer",
    "PropertyObservable",
    # Persistence
    "GameStateSerializer",
    "SaveLoadManager",
    "JSONSerializer",
    "PickleSerializer",
    # Plugin system
    "GamePlugin",
    "PluginManager",
    "PluginMetadata",
    # Replay system
    "ReplayManager",
    "ReplayRecorder",
    "ReplayAction",
    # Settings
    "Settings",
    "SettingsManager",
    # Educational
    "TutorialMode",
    "TutorialStep",
    "StrategyTip",
    "StrategyTipProvider",
    "ProbabilityCalculator",
    "GameTheoryExplainer",
    "GameTheoryExplanation",
    "AIExplainer",
    # Challenges
    "Challenge",
    "ChallengePack",
    "ChallengeManager",
    "DifficultyLevel",
    "get_default_challenge_manager",
    # CLI utilities
    "Color",
    "TextStyle",
    "Theme",
    "THEMES",
    "ASCIIArt",
    "RichText",
    "ProgressBar",
    "Spinner",
    "InteractiveMenu",
    "CommandHistory",
    "clear_screen",
    "get_terminal_size",
]

# Add GUI enhancements to __all__ if available
if GUI_ENHANCEMENTS_AVAILABLE:
    __all__.extend(
        [
            "ThemeConfig",
            "ThemeManager",
            "get_theme_manager",
            "SoundManager",
            "create_sound_manager",
            "AccessibilityManager",
            "get_accessibility_manager",
            "TranslationManager",
            "get_translation_manager",
            "_",
            "set_language",
            "KeyboardShortcut",
            "ShortcutManager",
            "get_shortcut_manager",
        ]
    )
