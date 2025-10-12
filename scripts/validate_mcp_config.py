#!/usr/bin/env python3
"""Command-line utility to validate MCP configuration.

This script validates the MCP configuration file and reports any issues.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.mcp_config_loader import load_default_mcp_config


def main() -> int:
    """Main entry point for validation script.

    Returns:
        Exit code (0 for success, 1 for errors).
    """
    print("=" * 70)
    print("MCP Configuration Validator")
    print("=" * 70)
    print()

    try:
        # Load configuration
        print("Loading configuration from .github/mcp-config.json...")
        config = load_default_mcp_config()
        print("✓ Configuration loaded successfully")
        print()

        # Validate configuration
        print("Validating configuration...")
        errors = config.validate()

        if errors:
            print("✗ Configuration has errors:")
            for error in errors:
                print(f"  - {error}")
            print()
            return 1

        print("✓ Configuration is valid")
        print()

        # Display summary
        print("-" * 70)
        print("Configuration Summary")
        print("-" * 70)
        print(f"Total servers: {config.get_server_count()}")
        print()

        for name, server in config.servers.items():
            print(f"Server: {name}")
            print(f"  Type: {server.type}")
            print(f"  URL: {server.url}")
            print(f"  Tools: {server.tools}")
            print(f"  Headers: {server.headers}")
            print()

        print("=" * 70)
        print("✓ All servers are properly configured")
        print("✓ Configuration is valid for GitHub Copilot coding agent")
        print("=" * 70)

        return 0

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print()
        print("Please ensure mcp-config.json exists in .github/ directory")
        return 1

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        print()
        print("Please check the configuration file for issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
