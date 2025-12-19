# Demisto SDK MCP Tools

[![Status](https://img.shields.io/badge/status-alpha-orange)](https://github.com/ciaran-finnegan/cortex-xsiam-sdk-mcp-tools)

> ⚠️ **Alpha Release**: These MCP tool definitions are in early development and not suitable for production use. Tool schemas and implementations may change without notice.

Model Context Protocol (MCP) tool definitions for demisto-sdk commands.

## Overview

These JSON files define MCP tools that wrap demisto-sdk commands for use with LLM coding assistants that support MCP (Cursor, Cline).

## Usage

### Option 1: Use Tool Definitions Only

Copy the `tools/` directory to your MCP server configuration:

```
~/.cursor/projects/<project>/mcps/demisto-sdk/tools/
```

### Option 2: Create a Full MCP Server

For a functional MCP server implementation, see:
- [mcp-demisto-sdk](https://github.com/your-username/mcp-demisto-sdk) - Python MCP server

## Available Tools

| Tool | Description |
|------|-------------|
| `init_pack` | Create pack structure |
| `init_integration` | Scaffold integration |
| `init_script` | Scaffold script |
| `format_content` | Standardise formatting |
| `validate_content` | Check validity |
| `lint_content` | Code quality checks |
| `generate_docs` | Create README documentation |
| `generate_unit_tests` | Generate test scaffolds |
| `generate_test_playbook` | Create test playbook |
| `generate_outputs` | Generate context paths from JSON |
| `upload_content` | Deploy to XSIAM/XSOAR |
| `download_content` | Sync from platform |
| `run_command` | Execute commands remotely |
| `run_playbook` | Run playbooks remotely |
| `find_dependencies` | Analyse pack dependencies |
| `update_release_notes` | Version management |
| `zip_packs` | Create distributable archives |
| `openapi_codegen` | Generate from OpenAPI spec |
| `postman_codegen` | Generate from Postman collection |

## Tool Definition Format

Each tool is defined as a JSON file:

```json
{
  "name": "tool_name",
  "description": "What the tool does...",
  "arguments": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["param_name"]
  }
}
```

## Creating an MCP Server

To create a functional MCP server that executes these tools:

```python
# mcp_demisto_sdk/server.py
from mcp import Server
import subprocess

server = Server("demisto-sdk")

@server.tool("init_pack")
async def init_pack(name: str, output_dir: str = "Packs"):
    result = subprocess.run(
        ["demisto-sdk", "init", "--pack", "-n", name, "-o", output_dir],
        capture_output=True, text=True
    )
    return {"success": result.returncode == 0, "output": result.stdout}

# ... implement other tools
```

## Related

- [demisto-sdk](https://github.com/demisto/demisto-sdk) - Official SDK
- [MCP Specification](https://modelcontextprotocol.io/) - Protocol documentation
- [cortex-xsiam-sdk-mcp-tools](https://github.com/ciaran-finnegan/cortex-xsiam-sdk-mcp-tools) - MCP server implementation
- [cortex-xsiam-content-development-template](https://github.com/ciaran-finnegan/cortex-xsiam-content-development-template) - Development template

