# TODO: Future Expansions and Upgrades

This document tracks the highest-impact follow-up work for the Games repository. Items are grouped by priority so that the next development cycles can focus on the most impactful gaps.

## 🔥 High Priority

- [ ] **Ship a fully interactive CLI for Bluff** – wire the existing CLI prompts into the game loop, add tournament/replay flows, and cover the path with tests so players who cannot use the GUI still have a complete experience.
- [ ] **Implement real telemetry delivery for CrashReporter** – replace the placeholder `_send_telemetry` method with a concrete transport (e.g., HTTPS or file-based queue), configuration hooks, and integration tests so opt-in telemetry actually sends data.

## ⚖️ Medium Priority

- [ ] **Finish the full Backgammon ruleset** – add bearing off, doubling cube handling, and remaining rule enforcement noted in the in-game documentation to bring the title to parity with the tabletop game.
- [ ] **Complete Pentago mechanics and AI** – implement quadrant rotation logic and provide at least a baseline computer opponent to match the feature list promised in the README.

## 🧊 Low Priority

- [ ] **Expand Sprouts beyond the prototype** – finish enforcing the full topological rule set and add a proper visual representation so the abstract mechanics are playable.
- [ ] **Optimize the 20 Questions decision tree** – replace the basic binary search with a tuned tree/knowledge base so question depth aligns with the README roadmap.

## ✅ Recently Completed Highlights

- 🎨 Bluff now detects PyQt5 availability at runtime and falls back to the Tk GUI automatically, keeping the desktop experience resilient across environments.
- 🛡️ CrashReporter consistently writes structured crash reports and installs a global exception hook so unexpected errors are captured with context for every game.
