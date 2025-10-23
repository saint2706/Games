"""Serializable launcher context for the PyScript frontend."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from games_collection.catalog.registry import get_all_games
from games_collection.core.daily_challenges import DailyChallengeScheduler, DailyChallengeSelection
from games_collection.core.leaderboard_service import CrossGameLeaderboardEntry
from games_collection.core.profile_service import ProfileService, RecentlyPlayedEntry
from games_collection.core.recommendation_service import RecommendationResult
from games_collection.launcher import LauncherSnapshot, build_launcher_snapshot


@dataclass(frozen=True)
class WebProfileSummary:
    """Serializable summary of the active profile for display in the browser."""

    name: str
    identifier: str
    level: int
    experience: int
    experience_to_next: int
    achievements_unlocked: int
    achievements_total: int
    achievement_points: int
    daily_completed: bool
    daily_streak: int
    best_daily_streak: int
    total_daily_completed: int


@dataclass(frozen=True)
class WebDailyChallenge:
    """Serializable representation of the scheduled daily challenge."""

    date: str
    pack_name: str
    pack_description: str
    challenge_id: str
    challenge_title: str
    difficulty: str
    description: str
    goal: str
    summary: str
    metadata: Mapping[str, Any]
    completed: bool


@dataclass(frozen=True)
class WebLeaderboardEntry:
    """Serializable representation of a leaderboard row."""

    player_id: str
    display_name: str
    level: int
    experience: int
    total_games: int
    total_wins: int
    win_rate: float
    achievement_points: int
    achievements_unlocked: int
    favorite_game: str | None
    daily_challenge_streak: int
    is_self: bool


@dataclass(frozen=True)
class WebRecommendation:
    """Serializable representation of a recommendation for the player."""

    game_id: str
    game_name: str
    score: float
    reasons: Tuple[str, ...]
    explanation: str


@dataclass(frozen=True)
class WebRecentGame:
    """Serializable representation of a recently played game."""

    game_id: str
    last_played: str | None


@dataclass(frozen=True)
class WebLauncherSnapshot:
    """Collection of data needed to render the launcher in a browser."""

    profile: WebProfileSummary
    daily_challenge: WebDailyChallenge
    leaderboard: Tuple[WebLeaderboardEntry, ...]
    recommendations: Tuple[WebRecommendation, ...]
    recently_played: Tuple[WebRecentGame, ...]
    favorites: Tuple[str, ...]

    def to_payload(self) -> Dict[str, Any]:
        """Return the snapshot as a JSON-serialisable mapping."""

        return {
            "profile": asdict(self.profile),
            "daily_challenge": asdict(self.daily_challenge),
            "leaderboard": [asdict(entry) for entry in self.leaderboard],
            "recommendations": [asdict(item) for item in self.recommendations],
            "recently_played": [asdict(item) for item in self.recently_played],
            "favorites": list(self.favorites),
        }

    @classmethod
    def from_launcher_snapshot(cls, snapshot: LauncherSnapshot) -> "WebLauncherSnapshot":
        """Create a :class:`WebLauncherSnapshot` from a CLI snapshot."""

        daily = _serialise_daily_challenge(snapshot.daily_selection, snapshot.daily_completed)
        leaderboard = _serialise_leaderboard(snapshot.leaderboard, snapshot.profile_identifier)
        recommendations = tuple(_serialise_recommendation(item) for item in snapshot.recommendations)
        recent = tuple(_serialise_recent(entry) for entry in snapshot.recently_played)

        profile = WebProfileSummary(
            name=snapshot.profile_name,
            identifier=snapshot.profile_identifier,
            level=snapshot.profile_level,
            experience=snapshot.experience,
            experience_to_next=snapshot.experience_to_next,
            achievements_unlocked=snapshot.achievements_unlocked,
            achievements_total=snapshot.achievements_total,
            achievement_points=snapshot.achievement_points,
            daily_completed=snapshot.daily_completed,
            daily_streak=snapshot.daily_streak,
            best_daily_streak=snapshot.best_daily_streak,
            total_daily_completed=snapshot.total_daily_completed,
        )

        return cls(
            profile=profile,
            daily_challenge=daily,
            leaderboard=leaderboard,
            recommendations=recommendations,
            recently_played=recent,
            favorites=tuple(snapshot.favorite_games),
        )


def build_web_launcher_snapshot(
    service: ProfileService,
    scheduler: DailyChallengeScheduler,
    *,
    leaderboard_limit: int = 3,
    recommendation_limit: int = 3,
) -> WebLauncherSnapshot:
    """Return a :class:`WebLauncherSnapshot` suitable for browser consumption."""

    snapshot = build_launcher_snapshot(
        service,
        scheduler,
        leaderboard_limit=leaderboard_limit,
        recommendation_limit=recommendation_limit,
    )
    return WebLauncherSnapshot.from_launcher_snapshot(snapshot)


def get_catalogue_payload() -> Dict[str, Any]:
    """Return a serialisable payload describing all registered games."""

    metadata = get_all_games()
    genres = sorted({item.genre for item in metadata})
    games: List[Dict[str, Any]] = [
        {
            "slug": item.slug,
            "name": item.name,
            "genre": item.genre,
            "package": item.package,
            "entry_point": item.entry_point,
            "description": item.description,
            "synopsis": item.synopsis,
            "tags": list(item.tags),
            "mechanics": list(item.mechanics),
            "average_duration": item.average_duration,
            "difficulty": item.difficulty,
            "screenshot_path": item.screenshot_path,
            "thumbnail_path": item.thumbnail_path,
        }
        for item in metadata
    ]
    return {"genres": genres, "games": games}


def _serialise_daily_challenge(selection: DailyChallengeSelection, completed: bool) -> WebDailyChallenge:
    return WebDailyChallenge(
        date=selection.target_date.isoformat(),
        pack_name=selection.pack.name,
        pack_description=selection.pack.description,
        challenge_id=selection.challenge.id,
        challenge_title=selection.challenge.title,
        difficulty=selection.challenge.difficulty.value,
        description=selection.challenge.description,
        goal=selection.challenge.goal,
        summary=selection.summary(),
        metadata=dict(selection.challenge.metadata),
        completed=completed,
    )


def _serialise_leaderboard(
    entries: Sequence[CrossGameLeaderboardEntry],
    player_id: str,
) -> Tuple[WebLeaderboardEntry, ...]:
    serialised = []
    for entry in entries:
        serialised.append(
            WebLeaderboardEntry(
                player_id=entry.player_id,
                display_name=entry.display_name,
                level=entry.level,
                experience=entry.experience,
                total_games=entry.total_games,
                total_wins=entry.total_wins,
                win_rate=entry.win_rate,
                achievement_points=entry.achievement_points,
                achievements_unlocked=entry.achievements_unlocked,
                favorite_game=entry.favorite_game,
                daily_challenge_streak=entry.daily_challenge_streak,
                is_self=entry.player_id == player_id,
            )
        )
    return tuple(serialised)


def _serialise_recommendation(result: RecommendationResult) -> WebRecommendation:
    return WebRecommendation(
        game_id=result.game_id,
        game_name=result.game_name,
        score=result.score,
        reasons=tuple(result.reasons),
        explanation=result.explanation,
    )


def _serialise_recent(entry: RecentlyPlayedEntry) -> WebRecentGame:
    return WebRecentGame(game_id=entry.game_id, last_played=entry.last_played)
