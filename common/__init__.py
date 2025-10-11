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
]
