# Demisto SDK MCP Tools

**Alpha** - Tool definitions may change.

MCP tool definitions for demisto-sdk commands.

## Overview

JSON files defining MCP tools that wrap demisto-sdk commands for LLM assistants supporting MCP (Cursor, Cline).

## Usage

### Option 1: Tool Definitions Only

Copy `tools/` to your MCP server configuration:

```
~/.cursor/projects/<project>/mcps/demisto-sdk/tools/
```

### Option 2: Full MCP Server

See [cortex-xsiam-sdk-mcp-tools](https://github.com/ciaran-finnegan/cortex-xsiam-sdk-mcp-tools).

## Tools

| Tool | Description |
|------|-------------|
| `init_pack` | Create pack structure |
| `init_integration` | Scaffold integration |
| `init_script` | Scaffold script |
| `format_content` | Standardise formatting |
| `validate_content` | Check validity |
| `lint_content` | Code quality checks |
| `generate_docs` | Create README |
| `generate_unit_tests` | Generate test scaffolds |
| `generate_test_playbook` | Create test playbook |
| `generate_outputs` | Generate context paths |
| `upload_content` | Deploy to XSIAM/XSOAR |
| `download_content` | Sync from platform |
| `run_command` | Execute commands remotely |
| `run_playbook` | Run playbooks remotely |
| `find_dependencies` | Analyse dependencies |
| `update_release_notes` | Version management |
| `zip_packs` | Create archives |
| `openapi_codegen` | Generate from OpenAPI |
| `postman_codegen` | Generate from Postman |

## Tool Definition Format

```json
{
  "name": "tool_name",
  "description": "What the tool does",
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

## Related

- [demisto-sdk](https://github.com/demisto/demisto-sdk)
- [MCP Specification](https://modelcontextprotocol.io/)
- [cortex-xsiam-sdk-mcp-tools](https://github.com/ciaran-finnegan/cortex-xsiam-sdk-mcp-tools)
- [cortex-xsiam-content-development-template](https://github.com/ciaran-finnegan/cortex-xsiam-content-development-template)
