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
- MCP configuration loading and validation
"""

from .ai_enhancements import (
    AIDifficultyLevel,
    AITrainingExample,
    AITrainingSession,
    DifficultyAdjuster,
    NeuralNetworkStrategy,
    NeuralNetworkTrainingExample,
    PersonalityProfile,
    ReinforcementLearningAgent,
    ReinforcementLearningConfig,
    TrainableEnvironment,
)
from .ai_strategy import AIStrategy, HeuristicStrategy, MinimaxStrategy, RandomStrategy
from .architecture.engine import GameEngine, GamePhase, GameState
from .architecture.events import Event, EventBus, EventHandler, FunctionEventHandler, GameEventType, get_global_event_bus, set_global_event_bus
from .architecture.observer import Observable, Observer, PropertyObservable
from .architecture.persistence import GameStateSerializer, JSONSerializer, PickleSerializer, SaveLoadManager
from .architecture.plugin import GamePlugin, PluginManager, PluginMetadata
from .architecture.replay import ReplayAction, ReplayManager, ReplayRecorder
from .architecture.settings import Settings, SettingsManager
from .configuration import (
    GameConfigurationProfile,
    SettingField,
    get_configuration_profile,
    get_configuration_profiles,
    get_settings_manager,
    merge_defaults,
    prepare_launcher_settings,
    reset_settings,
    save_settings,
    update_settings_from_mapping,
)
from .challenges import Challenge, ChallengeManager, ChallengePack, DifficultyLevel, get_default_challenge_manager
from .cli_utils import (
    THEMES,
    ASCIIArt,
    Color,
    CommandHistory,
    InteractiveMenu,
    ProgressBar,
    RichText,
    Spinner,
    TextStyle,
    Theme,
    clear_screen,
    get_terminal_size,
)
from .daily_challenges import DailyChallengeScheduler, DailyChallengeSelection
from .educational import (
    AIExplainer,
    DocumentationTutorialMode,
    GameTheoryExplainer,
    GameTheoryExplanation,
    ProbabilityCalculator,
    StrategyTip,
    StrategyTipProvider,
    TutorialMode,
    TutorialStep,
)
from .mcp_config_loader import MCPConfig, MCPServerConfig, load_default_mcp_config, validate_mcp_config_file
from .recommendation_service import GameDescriptor, RecommendationResult, RecommendationService, RecommendationWeights
from .tutorial_registry import GLOBAL_TUTORIAL_REGISTRY, TutorialMetadata, TutorialRegistration
from .tutorial_session import TutorialFeedback, TutorialSession
from .update_service import (
    DEFAULT_PACKAGE_NAME,
    DEFAULT_REPOSITORY,
    ReleaseAsset,
    ReleaseInfo,
    UpdateCheckResult,
    check_for_updates,
    detect_bundle,
    download_release_asset,
    fetch_latest_release,
    get_auto_update_preference,
    get_installed_version,
    is_update_available,
    set_auto_update_preference,
)

# GUI enhancement imports (optional, only if tkinter available)
try:
    from .accessibility import AccessibilityManager, get_accessibility_manager
    from .i18n import TranslationManager, _, get_translation_manager, set_language
    from .keyboard_shortcuts import KeyboardShortcut, ShortcutManager, get_shortcut_manager
    from .sound_manager import SoundManager, create_sound_manager
    from .themes import ThemeConfig, ThemeManager, get_theme_manager

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
    "ReinforcementLearningAgent",
    "ReinforcementLearningConfig",
    "NeuralNetworkStrategy",
    "AITrainingSession",
    "AITrainingExample",
    "NeuralNetworkTrainingExample",
    "DifficultyAdjuster",
    "AIDifficultyLevel",
    "PersonalityProfile",
    "TrainableEnvironment",
    # Event system
    "Event",
    "EventBus",
    "EventHandler",
    "FunctionEventHandler",
    "GameEventType",
    "get_global_event_bus",
    "set_global_event_bus",
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
    "SettingField",
    "GameConfigurationProfile",
    "get_configuration_profiles",
    "get_configuration_profile",
    "get_settings_manager",
    "merge_defaults",
    "prepare_launcher_settings",
    "save_settings",
    "reset_settings",
    "update_settings_from_mapping",
    # Educational
    "TutorialMode",
    "DocumentationTutorialMode",
    "TutorialStep",
    "StrategyTip",
    "StrategyTipProvider",
    "ProbabilityCalculator",
    "GameTheoryExplainer",
    "GameTheoryExplanation",
    "AIExplainer",
    "TutorialSession",
    "TutorialFeedback",
    "GLOBAL_TUTORIAL_REGISTRY",
    "TutorialMetadata",
    "TutorialRegistration",
    # Challenges
    "Challenge",
    "ChallengePack",
    "ChallengeManager",
    "DifficultyLevel",
    "get_default_challenge_manager",
    "DailyChallengeScheduler",
    "DailyChallengeSelection",
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
    # MCP Configuration
    "MCPConfig",
    "MCPServerConfig",
    "load_default_mcp_config",
    "validate_mcp_config_file",
    # Recommendations
    "RecommendationService",
    "RecommendationWeights",
    "RecommendationResult",
    "GameDescriptor",
    "ReleaseAsset",
    "ReleaseInfo",
    "UpdateCheckResult",
    "DEFAULT_PACKAGE_NAME",
    "DEFAULT_REPOSITORY",
    "get_installed_version",
    "fetch_latest_release",
    "check_for_updates",
    "is_update_available",
    "download_release_asset",
    "detect_bundle",
    "get_auto_update_preference",
    "set_auto_update_preference",
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
