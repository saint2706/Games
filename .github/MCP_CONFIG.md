# MCP Configuration Documentation

## Overview

This document describes the MCP (Model Context Protocol) configuration for the GitHub Copilot coding agent used in this repository.

## Configuration File

The MCP configuration is stored in `.github/mcp-config.json` and defines the external servers that the GitHub Copilot coding agent can connect to for enhanced capabilities.

## Configuration Structure

The configuration file follows this JSON schema:

```json
{
  "mcpServers": {
    "serverName": {
      "type": "http",
      "url": "https://server.endpoint.com/path",
      "tools": ["*"],
      "headers": {
        "Accept": "application/json"
      }
    }
  }
}
```

### Fields

- **mcpServers**: Root object containing all server configurations
  - **serverName**: Unique identifier for each server
    - **type**: Protocol type (currently "http")
    - **url**: Full HTTPS endpoint URL for the server
    - **tools**: Array of enabled tools (["*"] means all tools)
    - **headers**: HTTP headers to include in requests

## Configured Servers

This repository has three MCP servers configured:

### 1. DeepWiki

- **Purpose**: Provides access to DeepWiki knowledge base
- **Endpoint**: `https://mcp.deepwiki.com/mcp`
- **Tools**: All tools enabled (["*"])

### 2. FetchMCP

- **Purpose**: Fetches and processes external resources
- **Endpoint**: `https://remote.mcpservers.org/fetch/mcp`
- **Tools**: All tools enabled (["*"])

### 3. SequentialThinking

- **Purpose**: Provides sequential reasoning and thinking capabilities
- **Endpoint**: `https://remote.mcpservers.org/sequentialthinking/mcp`
- **Tools**: All tools enabled (["*"])

## Validation

The configuration is automatically validated using the test suite to ensure:

1. ✅ File exists and is valid JSON
2. ✅ All required fields are present
3. ✅ Exactly three servers are configured
4. ✅ All URLs use HTTPS for security
5. ✅ Server configurations are consistent
6. ✅ URLs are well-formed and valid

### Running Validation Tests

To validate the MCP configuration, run:

```bash
# Run MCP config validation tests
python -m pytest tests/test_mcp_config.py -v

# Run MCP config loader tests
python -m pytest tests/test_mcp_config_loader.py -v

# Run all MCP tests
python -m pytest tests/test_mcp_config*.py -v
```

## Using the Configuration

### Programmatic Access

You can load and validate the configuration programmatically using the `mcp_config_loader` module:

```python
from common.mcp_config_loader import load_default_mcp_config

# Load configuration
config = load_default_mcp_config()

# Check server count
print(f"Total servers: {config.get_server_count()}")

# Get server names
server_names = config.get_server_names()
print(f"Configured servers: {', '.join(server_names)}")

# Get specific server
deepwiki = config.get_server("deepwiki")
if deepwiki:
    print(f"DeepWiki URL: {deepwiki.url}")

# Validate configuration
if config.is_valid():
    print("✓ Configuration is valid")
else:
    print("✗ Configuration has errors:")
    for error in config.validate():
        print(f"  - {error}")
```

### Validation Utility

You can also validate the configuration file directly:

```python
from pathlib import Path
from common.mcp_config_loader import validate_mcp_config_file

config_path = Path(".github/mcp-config.json")
is_valid, errors = validate_mcp_config_file(config_path)

if is_valid:
    print("✓ Configuration is valid")
else:
    print("✗ Configuration errors:")
    for error in errors:
        print(f"  - {error}")
```

## Modifying the Configuration

If you need to add, remove, or modify servers:

1. Edit `.github/mcp-config.json`
2. Ensure the JSON syntax is valid
3. Run validation tests: `pytest tests/test_mcp_config.py -v`
4. Update tests if server names or URLs change

### Adding a New Server

To add a new server, add a new entry under `mcpServers`:

```json
{
  "mcpServers": {
    "newServer": {
      "type": "http",
      "url": "https://new-server.example.com/mcp",
      "tools": ["*"],
      "headers": {
        "Accept": "application/json"
      }
    }
  }
}
```

Then update the tests to reflect the new server count and name.

## Security Considerations

1. **HTTPS Only**: All server URLs must use HTTPS for secure communication
2. **Trusted Sources**: Only configure servers from trusted sources
3. **Headers**: Review headers to ensure they don't expose sensitive information
4. **Validation**: Always run validation tests after modifying the configuration

## Troubleshooting

### Configuration Not Loading

If the configuration fails to load:

1. Check that the file exists at `.github/mcp-config.json`
2. Validate JSON syntax using `python -m json.tool .github/mcp-config.json`
3. Run tests to identify specific issues: `pytest tests/test_mcp_config.py -v`

### Validation Errors

Common validation errors and solutions:

- **Missing required field**: Ensure all servers have `type`, `url`, `tools`, and `headers`
- **Invalid URL**: Check that URLs use HTTPS and have valid hosts
- **Wrong server type**: Ensure `type` is set to "http"
- **Invalid JSON**: Use a JSON validator or linter to check syntax

### Getting Help

For issues with the MCP configuration:

1. Run the test suite to identify specific problems
2. Check the error messages in test output
3. Review this documentation for correct format
4. Consult the MCP protocol documentation

## Related Files

- **Configuration**: `.github/mcp-config.json`
- **Loader Module**: `common/mcp_config_loader.py`
- **Validation Tests**: `tests/test_mcp_config.py`
- **Loader Tests**: `tests/test_mcp_config_loader.py`

## References

- [Model Context Protocol (MCP) Documentation](https://modelcontextprotocol.io/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
