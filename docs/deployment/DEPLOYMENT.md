# Deployment Guide

This guide covers different deployment methods for the Games Collection.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation from PyPI](#installation-from-pypi)
- [Homebrew Tap](#homebrew-tap)
- [Standalone Executables](#standalone-executables)
- [Auto-Update Workflow](#auto-update-workflow)
- [Web (PyScript)](#web-pyscript)
- [Mobile Deployments](#mobile-deployments)
- [Linux Packages](#linux-packages)
  - [Snap](#snap)
  - [Flatpak](#flatpak)
- [Docker Deployment](#docker-deployment)
- [Building from Source](#building-from-source)
- [Cross-Platform Compatibility](#cross-platform-compatibility)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Minimum Requirements

- Python 3.9 or higher (for source installation)
- 50 MB disk space (100 MB recommended)
- Terminal/Command Prompt access

### Recommended

- Python 3.11 or higher
- 100 MB disk space
- 2 GB RAM

### Platform Support

✅ **Fully Supported:**

- Linux (Ubuntu 20.04+, Debian 11+, Fedora 35+)
- macOS (10.15 Catalina or later)
- Windows (10/11)

✅ **Tested Python Versions:**

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## Release Validation

All PyPI releases are gated by an automated smoke test that runs in GitHub Actions whenever a release is published or the workflow is dispatched manually. The workflow builds the source and wheel distributions, installs the generated wheel into an isolated virtual environment, and verifies two representative entry points: `games-collection --help` and `python -m games_collection.games.card.go_fish --gui-framework pyqt5 --help`. The PyPI upload proceeds only if these commands succeed, ensuring that the published artifacts are installable and expose their CLI help correctly.

## Installation from PyPI

### Standard Installation

```bash
pip install games-collection
```

### With GUI Support

```bash
pip install games-collection[gui]
```

### Development Installation

```bash
pip install games-collection[dev]
```

### Running Games

After installation, you can run games using the `games-*` commands:

```bash
# Card games
games-poker
games-blackjack
games-uno
games-war

# Paper games
games-tic-tac-toe
games-battleship
games-checkers

# Dice games
games-craps
games-bunco

# See all available games
pip show games-collection
```

## Homebrew Tap

The Homebrew tap provides a fully managed macOS installation backed by the GitHub release artifacts.

### Adding the Tap

```bash
brew tap saint2706/games-collection https://github.com/saint2706/Games
```

This command registers the tap and enables automatic updates whenever new versions are published.

### Installing the CLI

```bash
brew install games-collection
```

Homebrew installs the Python 3.11 runtime declared in the formula and wires the `games-collection` command into your `$PATH`.

### Updating to the Latest Release

```bash
brew update
brew upgrade games-collection
```

### macOS Troubleshooting

- **Missing Command Line Tools:** Run `xcode-select --install` if Homebrew reports missing developer tools.
- **Python Linking Issues:** If `/usr/local/opt/python@3.11` is not found, run `brew doctor` and reinstall `python@3.11`.
- **Stale Tap Cache:** Execute `brew update-reset` before `brew upgrade` when the tap URL changes or if audits fail.

## Standalone Executables

Standalone executables bundle all dependencies, requiring no Python installation.

### Downloading Pre-built Executables

1. Go to the [Releases page](https://github.com/saint2706/Games/releases)
1. Download the executable for your platform:
   - **Linux**: `games-collection-linux`
   - **macOS**: `games-collection-macos`
   - **Windows**: `games-collection-windows.exe`

### Running the Executable

#### Linux/macOS

```bash
# Make executable
chmod +x games-collection-linux

# Run
./games-collection-linux
```

#### Windows

```cmd
games-collection-windows.exe
```

### Building Your Own Executable

#### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller build_configs/pyinstaller/games.spec --clean

# Find executable in dist/
```

#### Using Nuitka

```bash
# Install Nuitka
pip install nuitka

# Build executable
python build_configs/nuitka/build.py

# Find executable in dist/nuitka/
```

#### Using Build Script

```bash
# Build with PyInstaller (default)
./scripts/build_executable.sh pyinstaller

# Or build with Nuitka
./scripts/build_executable.sh nuitka
```

## Auto-Update Workflow

Automatic update checks are available in both the CLI launcher and the PyQt launcher. The launcher contacts two services:

- **PyPI** to determine the installed version of the `games-collection` package.
- **GitHub Releases** to retrieve metadata and download URLs for bundled executables. Allow outbound HTTPS access to `api.github.com` and the GitHub release CDN; SSL interception appliances must trust the GitHub certificate chain.

### CLI usage

- Run `games-collection --check-updates` to perform a one-off check and report the result.
- Run `games-collection --update` to download the latest PyInstaller/Nuitka bundle for your platform and print the saved location.
- Press **U** inside the interactive launcher to open an update workflow that can download the bundle and relaunch into the downloaded binary when it is executable.
- Persistently enable or disable automatic checks with `--enable-auto-update-check` or `--disable-auto-update-check`. The preference is stored in `config/game__launcher_settings.json`.

Pip-based deployments should continue to rely on `pip install --upgrade games-collection`; the automatic downloader primarily serves standalone bundles.

### GUI notifications

- On startup the PyQt launcher displays a banner when a newer release is detected. The banner includes a download button and a checkbox to opt out of future automatic checks.
- The header button labelled “Check for updates” performs a manual check and surfaces the outcome in a message box.
- Downloaded executables are saved to the system temporary directory. After a successful download, the GUI offers to relaunch into the new bundle when possible.

If your environment performs SSL inspection, install the corporate root certificate so Python can validate HTTPS connections. Without a trusted certificate the update check gracefully falls back to offline mode.
## Web (PyScript)

The PyScript bundle allows the launcher to run directly in the browser. It packages the Python wheel, static assets, and a PyScript front-end that communicates with the cooperative game runners.

### Building the bundle

```bash
python scripts/build_pyscript_bundle.py
```

The script creates a `dist/web/` directory containing the HTML, CSS, JavaScript, and packaged wheel. The generated `bundle.json` file records which wheel was embedded.

### Local preview

```bash
cd dist/web
python -m http.server 8000
# Visit http://localhost:8000 in your browser
```

PyScript runs entirely in the browser, so no additional backend process is required for testing.

### Publishing to GitHub Pages

1. Commit the contents of `dist/web/` to a branch (for example, `gh-pages`).
1. Enable GitHub Pages for that branch via the repository settings.
1. Subsequent runs of the builder can overwrite the branch contents and push updates.

### Current limitations

- Games rely on their text-based interfaces; GUI launchers are not exposed yet.
- Network multiplayer modes are unavailable because the PyScript runtime runs in an isolated browser sandbox.
- Larger games may require additional browser memory compared to native execution.
## Mobile Deployments

The mobile toolchain is optional and gated behind the `mobile` extras group. Install the
dependencies locally before building:

```bash
pip install .[mobile]
```

### Local Tooling

- **Android:** Use the official Buildozer container or install the Android SDK/NDK locally.
- **Apple:** Install Xcode 15 or later and enable command line tools. BeeWare's Briefcase
  CLI orchestrates the signing and packaging flow.
- **Shared assets:** Mobile builds reuse `src/games_collection/assets`. Update the assets
  before packaging to ensure brand consistency.

### Android Builds with Buildozer

```bash
export ANDROID_KEYSTORE_PATH=$PWD/build/mobile/signing/release.keystore
export ANDROID_KEYSTORE_PASSWORD=...  # Keystore password
export ANDROID_KEY_PASSWORD=...       # Key alias password

# Decode the keystore supplied as base64
mkdir -p build/mobile/signing
base64 -d < release.keystore.b64 > "$ANDROID_KEYSTORE_PATH"

# Run Buildozer using the curated spec
docker run --rm \
  -e ANDROID_KEYSTORE_PATH \
  -e ANDROID_KEYSTORE_PASSWORD \
  -e ANDROID_KEY_PASSWORD \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/kivy/buildozer:stable \
  bash -lc "python3 -m pip install .[mobile] && buildozer -v android release"

# Signed APKs land in build/mobile/android/bin/
ls build/mobile/android/bin
```

### Apple Builds with Briefcase

```bash
export MACOS_CODESIGN_IDENTITY="Developer ID Application: Example (ABCD123456)"
export MACOS_NOTARIZATION_PROFILE="GamesCollectionNotarization"
export IOS_SIGNING_PROFILE="GamesCollection-iOS"
export IOS_TEAM_ID="ABCD123456"

# Package macOS DMG
docker run --rm \
  -e MACOS_CODESIGN_IDENTITY \
  -e MACOS_NOTARIZATION_PROFILE \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/beeware/briefcase:latest \
  bash -lc "python3 -m pip install .[mobile] && briefcase package macOS -r"

# Package iOS IPA
docker run --rm \
  -e IOS_SIGNING_PROFILE \
  -e IOS_TEAM_ID \
  -v "$PWD":/workspace \
  -w /workspace \
  ghcr.io/beeware/briefcase:latest \
  bash -lc "python3 -m pip install .[mobile] && briefcase package iOS -r"

ls dist/macOS
ls dist/iOS
```

Briefcase automatically discovers the `games_collection.mobile.kivy_launcher:main` entry
point and bundles the shared assets directory for both platforms.

### Emulator Smoke Tests

- **Android:** Use `adb install build/mobile/android/bin/*.apk` to sideload the release
  build. The Pixel 6 API level 34 emulator is the default target used by QA.
- **iOS:** Target the `iPhone 15` simulator with `xcrun simctl install booted dist/iOS/*.ipa`.
  Launch with `xcrun simctl launch booted org.gamescollection` to verify touch navigation.
- **macOS:** Open the generated DMG, drag the app bundle to `/Applications`, and run the
  launcher to exercise game selection and favourites.

### GitHub Actions Pipeline

The `Mobile Packages` workflow (`.github/workflows/mobile-build.yml`) is available via the
**Run workflow** button. It runs a three-target matrix:

| Target  | Container Image                    | Command                          | Artifact   |
|---------|------------------------------------|----------------------------------|------------|
| Android | `ghcr.io/kivy/buildozer:stable`    | `buildozer -v android release`   | Signed APK |
| macOS   | `ghcr.io/beeware/briefcase:latest` | `briefcase package macOS -r`     | Signed DMG |
| iOS     | `ghcr.io/beeware/briefcase:latest` | `briefcase package iOS -r`       | Signed IPA |

Workflow inputs:

- `release_tag`: Used as an artifact suffix (e.g., `android-2.0.1`).
- `smoke_test_game` (optional): Launches the provided slug via the desktop launcher to
  validate metadata before publishing mobile builds.

### Artifact Locations

- **Android:** `build/mobile/android/bin/*.apk`
- **macOS:** `dist/macOS/*.dmg`
- **iOS:** `dist/iOS/*.ipa`
- **GitHub Actions:** Uploaded as `<target>-<release_tag>` artifacts.

### Required Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANDROID_KEYSTORE_B64` | Base64-encoded keystore injected into CI and decoded before the Buildozer run. |
| `ANDROID_KEYSTORE_PASSWORD` | Password used to unlock the Android keystore. |
| `ANDROID_KEY_PASSWORD` | Password for the `gamescollection` signing key alias. |
| `MACOS_CODESIGN_IDENTITY` | Identity passed to Briefcase for DMG signing. |
| `MACOS_NOTARIZATION_PROFILE` | App Store Connect notarization profile used post-signature. |
| `IOS_SIGNING_PROFILE` | Provisioning profile UUID for Briefcase iOS packaging. |
| `IOS_TEAM_ID` | Apple Developer team identifier required for iOS signing. |
## Linux Packages

Official Linux packages are produced automatically for tagged releases. Both packaging formats bundle the Python runtime, the Games Collection entry points, and GUI dependencies so you can launch the suite without a system-wide Python installation.

### Snap

The strict-mode snap exposes the CLI and GUI launchers and bundles PyQt/Pygame runtimes.

```bash
# Install from the Snap Store
sudo snap install games-collection

# Launch the main hub
games-collection
```

Strict confinement restricts access to specific hardware interfaces. Snap automatically connects the audio and display plugs, but joystick support must be granted manually:

```bash
sudo snap connect games-collection:joystick
```

The snap also declares `network`, `network-bind`, `opengl`, `x11`, and `wayland` plugs so the application can reach online leaderboards and render accelerated graphics in modern desktop environments.

### Flatpak

Tagged releases attach a Flatpak bundle that mirrors the snap payload. Install the bundle locally or add it to your Flatpak repo:

```bash
# Install the bundle in the current directory
flatpak install --user ./games-collection.flatpak

# Launch the application
flatpak run com.gamescollection.GamesCollection
```

The manifest grants access to X11, Wayland, PulseAudio/PipeWire, and the user's home directory for saving progress. Controller and joystick access is enabled via `--device=all` in the finish args. You can further relax or tighten the sandbox at runtime with overrides, for example:

```bash
flatpak override --user com.gamescollection.GamesCollection --filesystem=~/GamesCollectionSaves
```

If you only need CLI access, you can launch subcommands (such as Blackjack) directly by appending their names to the Flatpak run command (`flatpak run com.gamescollection.GamesCollection --game blackjack`).

## Docker Deployment

### Quick Start

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the container
docker-compose exec games bash

# Run a game
python -m games_collection.games.card.war
```

### Using Docker Directly

```bash
# Build the image
docker build -t games-collection .

# Run interactively
docker run -it games-collection

# Run with persistent statistics
docker run -it -v $(pwd)/game_stats:/home/games/.game_stats games-collection
```

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild image
docker-compose build --no-cache

# Remove everything
docker-compose down -v
```

## Building from Source

### Clone Repository

```bash
git clone https://github.com/saint2706/Games.git
cd Games
```

### Install in Development Mode

```bash
# Install with pip
pip install -e .

# Or with development dependencies
pip install -e .[dev]
```

### Run Games Directly

```bash
# Using Python module syntax
python -m games_collection.games.card.war
python -m games_collection.games.paper.tic_tac_toe

# Or using the launcher
python scripts/launcher.py
```

## Cross-Platform Compatibility

### Platform-Specific Considerations

#### Linux

- **GUI Games**: Requires Tkinter (usually pre-installed)

  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-tk

  # Fedora
  sudo dnf install python3-tkinter
  ```

- **Terminal**: Most games work in any terminal

- **Colors**: Requires terminal with ANSI color support

#### macOS

- **Python**: Use Python from python.org or Homebrew

  ```bash
  brew install python@3.11
  ```

- **Tkinter**: Included with official Python installers

- **Terminal**: Use Terminal.app or iTerm2

#### Windows

- **Python**: Download from python.org
- **Terminal**: Use Windows Terminal (recommended) or Command Prompt
- **Colors**: Enable ANSI colors in Windows Terminal settings
- **Tkinter**: Included with official Python installers

### Testing Your Installation

```bash
# Test basic import
python -c "from games_collection.games.card.war import WarGame; print('Success!')"

# Test crash reporter
python -c "from games_collection.core.crash_reporter import CrashReporter; print('Success!')"

# Test launcher
python scripts/launcher.py
```

## Troubleshooting

### Common Issues

#### "No module named 'colorama'"

```bash
pip install colorama
```

#### "No module named 'tkinter'"

See platform-specific instructions above for installing Tkinter.

#### Executable Won't Run (Linux/macOS)

```bash
# Make sure it's executable
chmod +x games-collection-linux

# Check if it's 64-bit (most systems)
file games-collection-linux
```

#### Windows Defender Blocks Executable

1. This is common with PyInstaller executables
1. Right-click → Properties → Unblock
1. Or add exception in Windows Defender

### Error Reporting

If you encounter errors:

1. **Check Logs**: Located in `~/.game_logs/`
1. **Crash Reports**: Located in `~/.game_logs/crashes/`
1. **Report Issues**: [GitHub Issues](https://github.com/saint2706/Games/issues)

### Getting Help

- **Documentation**: [GitHub Repository](https://github.com/saint2706/Games)
- **Issues**: [Report a Bug](https://github.com/saint2706/Games/issues/new)
- **Discussions**: [GitHub Discussions](https://github.com/saint2706/Games/discussions)

## Advanced Configuration

### Environment Variables

```bash
# Disable crash reporting
export GAMES_NO_CRASH_REPORT=1

# Enable telemetry (opt-in)
export GAMES_TELEMETRY=1

# Custom statistics directory
export GAMES_STATS_DIR=/custom/path
```

### Custom Build Options

#### PyInstaller

Edit `build_configs/pyinstaller/games.spec` to customize:

- Icon
- Console vs. windowed mode
- Additional data files
- Excluded modules

#### Nuitka

Edit `build_configs/nuitka/build.py` to customize:

- Output filename
- Optimization level
- Plugin options
- Icon

### Performance Tuning

```bash
# Use Nuitka for better performance
python build_configs/nuitka/build.py

# Or use PyInstaller with UPX compression
pyinstaller --upx-dir=/path/to/upx build_configs/pyinstaller/games.spec
```

## Uninstallation

### PyPI Installation

```bash
pip uninstall games-collection
```

### Remove User Data

```bash
# Remove statistics
rm -rf ~/.game_stats

# Remove logs
rm -rf ~/.game_logs
```

### Docker

```bash
# Remove containers and volumes
docker-compose down -v

# Remove image
docker rmi games-collection
```

## Security Considerations

- **Crash Reports**: May contain system information (opt-in)
- **Telemetry**: Disabled by default (opt-in only)
- **Statistics**: Stored locally in `~/.game_stats/`
- **Logs**: Stored locally in `~/.game_logs/`

All data is stored locally by default. No data is sent to external servers unless explicitly enabled.

## License

MIT License - See [LICENSE](../LICENSE) for details.
