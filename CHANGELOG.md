# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-12

### Added

#### Infrastructure & Framework

- **Achievement System**: Cross-game achievement framework with categories, rarities, and persistence
  - Achievement tracking across all games
  - Point system and progress tracking
  - JSON-based save/load functionality
  - Common achievements for progression, mastery, and special accomplishments
- **Player Profile System**: Unified player profile with statistics and progression
  - Game-specific profiles with win/loss tracking
  - Experience and level system
  - Favorite game tracking
  - Profile persistence and preferences
  - Total playtime and statistics across all games

#### Card Games

- **Uno**: Complete jump-in rule implementation
  - Players can play identical cards out of turn
  - Clockwise priority system
  - Bot personality-based decision making
  - CLI and GUI support
  - Comprehensive test coverage (14 tests)

### Changed

- **Uno House Rules**: Updated documentation to reflect fully implemented jump-in rule
- **PyPI Configuration**: Enhanced pyproject.toml with complete metadata, classifiers, and entry points
- **Documentation**: Updated TODO.md to track Q4 2025 roadmap progress (30% complete)

### Technical Details

- Added 50+ tests for achievement and profile systems
- All tests passing (100% success rate)
- Code formatted with Black and linted with Ruff
- Type hints and comprehensive docstrings

## [Unreleased]

### Planned

- Standalone executables (PyInstaller/Nuitka)
- Docker containers for easy deployment
- GitHub Actions for automated releases
- Full cross-platform compatibility testing
- Crash reporting and error analytics
- New card games: Cribbage, Euchre, Rummy 500

[1.0.0]: https://github.com/saint2706/Games/releases/tag/v1.0.0
