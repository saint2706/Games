# Copilot Instructions Guide

This document explains the GitHub Copilot instructions setup for this repository.

## Overview

This repository uses GitHub Copilot's custom instructions feature to provide context-specific guidance for AI-assisted
development. The instructions follow the
[best practices for Copilot coding agent](https://gh.io/copilot-coding-agent-tips).

## Instruction Files

### Repository-Wide Instructions

**File**: `.github/copilot-instructions.md`

This is the main instruction file that applies to all tasks assigned to GitHub Copilot in this repository. It contains:

- Repository overview and architecture
- Code quality standards and formatting rules
- Development workflow and pre-commit hooks
- Common patterns for game implementation
- Testing requirements and coverage goals
- Quick reference commands

This file is automatically loaded by GitHub Copilot when working on any file in the repository.

### Path-Specific Instructions

**Directory**: `.github/instructions/`

These files provide targeted guidance for specific types of files:

#### Test Files (`test-files.instructions.md`)

- **Applies to**: `**/test_*.py`
- **Covers**: pytest requirements, test patterns, fixture usage, coverage goals
- **Key Points**:
  - All test files must start with `test_` prefix
  - Include unit tests, integration tests, and performance benchmarks
  - Aim for 90%+ code coverage
  - Use descriptive docstrings for all test functions

#### Game Implementation Files (`game-implementations.instructions.md`)

- **Applies to**: `**/{card_games,paper_games,dice_games,logic_games,word_games}/**/*.py`
- **Covers**: game structure, core game engine requirements, AI opponents, code quality
- **Key Points**:
  - Inherit from `GameEngine` base class
  - Implement required methods: `is_valid_move()`, `make_move()`, `is_game_over()`
  - Keep function complexity ≤ 10
  - Include comprehensive game rules in module docstring

#### GUI Files (`gui-files.instructions.md`)

- **Applies to**: `**/gui.py`
- **Covers**: GUI framework, structure, event handling, accessibility, threading
- **Key Points**:
  - Inherit from `BaseGUI` base class
  - Separate game logic from GUI code
  - Use threading for AI moves to keep GUI responsive
  - Support keyboard navigation and accessibility features

### Agent-Specific Instructions

**File**: `.github/AGENTS.md`

Specialized instruction file following OpenAI Codex best practices. This file provides:

- Clear role definition for AI coding agents
- Actionable code templates and patterns
- Step-by-step development workflow
- Explicit validation requirements
- Success criteria for code changes
- Quick reference commands

This file follows OpenAI Codex best practices including:

1. Clear role and context definition
1. Specific, measurable requirements
1. Copy-paste code examples
1. Error prevention guidelines
1. Validation checklists

**File**: `.github/instructions/AGENTS.md`

Path-specific agent instructions that complement the repository-wide AGENTS.md. This file provides:

- Instructions for different file types (tests, GUI, games)
- File-type-specific patterns and templates
- Validation checklists by file type
- Quick reference commands for each file type
- Integration guidance with repository-wide instructions

Both AGENTS.md files are maintained alongside copilot-instructions.md for compatibility with different AI coding assistants and to provide specialized guidance following OpenAI Codex best practices.

## How Copilot Uses These Instructions

1. **Repository-Wide Context**: When Copilot works on any file, it reads `.github/copilot-instructions.md` to understand
   the project structure, coding standards, and development practices.

1. **Path-Specific Guidance**: When Copilot works on specific file types (tests, game implementations, GUIs), it also
   reads the relevant path-specific instructions from `.github/instructions/`.

1. **Combined Context**: Copilot combines both repository-wide and path-specific instructions to provide more accurate
   and context-aware suggestions.

## Maintaining Instructions

### When to Update Repository-Wide Instructions

- Project structure changes
- New architectural patterns are introduced
- Development workflow changes
- Code quality standards are updated
- New dependencies are added

### When to Update Path-Specific Instructions

- Testing framework changes
- New patterns for specific file types emerge
- Requirements for game implementations evolve
- GUI framework or patterns change

### Best Practices for Updates

1. **Keep Instructions Focused**: Each instruction file should focus on its specific domain
1. **Use Examples**: Include code examples to illustrate patterns
1. **Be Prescriptive**: Clearly state requirements and expectations
1. **Update Together**: When patterns change, update both the main instructions and relevant path-specific instructions
1. **Test Changes**: Verify that instructions don't conflict with each other

## Verifying Instructions

### Manual Verification

1. Check that all instruction files have valid YAML frontmatter (for path-specific files):

```bash
python -c "
import yaml
import pathlib

files = pathlib.Path('.github/instructions').glob('*.instructions.md')
for f in files:
    content = f.read_text()
    if content.startswith('---'):
        parts = content.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        print(f'{f.name}: {frontmatter}')
"
```

2. Verify file paths exist and are correct
1. Check for consistency between different instruction files

### Automated Testing

The repository includes tests for configuration files:

```bash
# Run MCP config tests (which validate related configuration)
pytest tests/test_mcp_config.py -v
```

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Best Practices for Copilot Coding Agent](https://gh.io/copilot-coding-agent-tips)
- [Adding Repository Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)

## Structure Summary

```
.github/
├── copilot-instructions.md              # Main repository-wide instructions
├── AGENTS.md                            # OpenAI Codex best practices (repository-wide)
├── COPILOT_INSTRUCTIONS_GUIDE.md       # This file (documentation)
└── instructions/                        # Path-specific instructions
    ├── test-files.instructions.md       # Test file requirements
    ├── game-implementations.instructions.md  # Game implementation requirements
    ├── gui-files.instructions.md        # GUI file requirements
    └── AGENTS.md                        # Path-specific agent instructions
```

**Note**: AGENTS.md files are placed at both levels:

- `.github/AGENTS.md` - Repository-wide agent instructions
- `.github/instructions/AGENTS.md` - Path-specific agent instructions

This dual placement ensures AI coding agents have comprehensive context regardless of which file they're working on.

## Impact on Development

These instructions help GitHub Copilot:

- **Understand Context**: Know the project structure and conventions
- **Generate Better Code**: Follow established patterns and standards
- **Maintain Consistency**: Apply the same coding style across the codebase
- **Improve Quality**: Automatically consider testing, documentation, and complexity requirements
- **Speed Development**: Reduce back-and-forth by getting it right the first time

By providing clear, comprehensive instructions, we enable GitHub Copilot to be a more effective coding partner.
