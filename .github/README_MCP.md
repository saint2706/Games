# MCP Configuration for GitHub Copilot

## Quick Start

The MCP (Model Context Protocol) configuration enables GitHub Copilot coding agent to use external servers for enhanced
capabilities.

### Validate Configuration

```bash
# Using the validation script
python scripts/validate_mcp_config.py

# Using pytest
pytest tests/test_mcp_config.py -v
```

### Programmatic Usage

```python
from common import load_default_mcp_config

# Load and use the configuration
config = load_default_mcp_config()
print(f"Servers: {config.get_server_names()}")
```

## Current Configuration

The repository is configured with **3 MCP servers**:

1. **deepwiki** - DeepWiki knowledge base access
1. **fetchMCP** - External resource fetching
1. **sequentialThinking** - Sequential reasoning capabilities

All servers use HTTPS and are properly validated.

## Testing

- **35 tests** validate the configuration
- **100% passing** - Configuration is valid ✅
- Tests cover JSON validity, server structure, URLs, and consistency

## Documentation

See [MCP_CONFIG.md](MCP_CONFIG.md) for detailed documentation.

## Files

- `mcp-config.json` - Configuration file
- `MCP_CONFIG.md` - Detailed documentation
- `tests/test_mcp_config.py` - Validation tests
- `tests/test_mcp_config_loader.py` - Utility tests
- `scripts/validate_mcp_config.py` - CLI validator
- `common/mcp_config_loader.py` - Utility module
