# LLM Assistant Setup Guide

Configuration guide for XSIAM development with various LLM coding assistants.

## Supported Assistants

| Assistant | Context File | MCP Support | Enterprise Ready |
|-----------|-------------|-------------|------------------|
| **Cursor** | `.cursorrules` | ✓ | ✓ |
| **Claude Code CLI** | `CLAUDE.md` | ✓ | ✓ |
| **Amazon Q Developer** | `.amazonq/rules` | ✗ | ✓ |
| **Cline** | `.clinerules` | ✓ | ✓ |
| **Codex CLI** | Context files | ✗ | ✓ |

---

## Cursor

### Configuration Files

| File | Purpose |
|------|---------|
| `.cursorrules` | Project-specific rules |
| `CLAUDE.md` | Context documentation (auto-indexed) |
| `Agents.md` | Agent role definitions |

### MCP Server Setup

Add to Cursor settings (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "demisto-sdk": {
      "command": "python",
      "args": ["-m", "mcp_demisto_sdk"],
      "env": {
        "DEMISTO_BASE_URL": "${DEMISTO_BASE_URL}",
        "DEMISTO_API_KEY": "${DEMISTO_API_KEY}"
      }
    }
  }
}
```

---

## Claude Code CLI

### Configuration

Claude Code CLI reads `CLAUDE.md` from the project root automatically.

### Usage

```bash
# Start Claude Code in project directory
claude

# With specific context
claude --context docs/xsiam-kb/
```

### MCP Integration

Configure in `~/.claude/mcp_servers.json`:

```json
{
  "demisto-sdk": {
    "command": "python",
    "args": ["-m", "mcp_demisto_sdk"]
  }
}
```

---

## Amazon Q Developer

### IDE Integration

1. Install Amazon Q extension in VS Code or JetBrains IDE
2. Sign in with AWS Builder ID or IAM Identity Centre
3. Configure workspace context

### Project Context

Create `.amazonq/rules/xsiam.md`:

```markdown
# XSIAM Development Rules

## Context
This project contains Cortex XSIAM playbooks, scripts, and integrations.

## Commands
- Use `demisto-sdk init` to scaffold content
- Run `demisto-sdk format` after code generation
- Run `demisto-sdk validate` before commit

## Patterns
- Reference Packs/CommonPlaybooks/ for playbook patterns
- Reference Packs/CommonScripts/ for script patterns
- Follow CLAUDE.md for detailed structure

## Standards
- Python 3.10+ for scripts
- YAML for playbooks
- Include unit tests
```

### Enterprise Customisation

For private codebases, configure Amazon Q Developer Customisation:

1. Navigate to AWS Console → Amazon Q Developer
2. Add private repository connection
3. Create customisation with your codebase
4. Activate customisation in IDE

---

## Cline

### Installation

Install from VS Code Marketplace or Open VSX Registry.

### Configuration

Create `.clinerules` in project root:

```markdown
# XSIAM Development Assistant

## Role
You are an XSIAM content developer assistant. Generate playbooks, scripts, and integrations following Cortex standards.

## Context Files
- CLAUDE.md - Primary development reference
- Agents.md - Agent role definitions
- Packs/CommonPlaybooks/ - Playbook patterns
- Packs/CommonScripts/ - Script patterns

## Workflow
1. Use demisto-sdk init to scaffold
2. Generate code following patterns
3. Run demisto-sdk format -y
4. Run demisto-sdk validate
5. Generate docs with demisto-sdk generate-docs

## Commands
When asked to create content:
1. Check if pack exists, create if not
2. Use appropriate template
3. Follow naming conventions
4. Include tests and documentation
```

### MCP Server Configuration

Cline supports MCP servers. Add to settings:

```json
{
  "cline.mcpServers": {
    "demisto-sdk": {
      "command": "python",
      "args": ["-m", "mcp_demisto_sdk"]
    }
  }
}
```

### Provider Configuration

Configure your preferred AI provider:

```json
{
  "cline.provider": "anthropic",
  "cline.apiKey": "${ANTHROPIC_API_KEY}",
  "cline.model": "claude-sonnet-4-20250514"
}
```

For enterprise, use AWS Bedrock or Azure OpenAI:

```json
{
  "cline.provider": "bedrock",
  "cline.awsRegion": "us-east-1",
  "cline.model": "anthropic.claude-sonnet-4-20250514-v1:0"
}
```

---

## Codex CLI

### Context Setup

Codex CLI uses file context. Point to documentation:

```bash
# With context directory
codex --context docs/xsiam-kb/ "Create a playbook that enriches IP addresses"

# With specific files
codex --files CLAUDE.md,Agents.md "Create a script to parse email headers"
```

### System Prompt

Create `~/.codex/system_prompt.md`:

```markdown
You are an XSIAM content developer. Follow these rules:

1. Use demisto-sdk for scaffolding and validation
2. Reference CLAUDE.md for structure
3. Follow patterns in Packs/CommonPlaybooks/
4. Include tests and documentation
5. Run format and validate after generation
```

---

## Environment Variables

All assistants require these for platform integration:

```bash
# Required for upload/download/run commands
export DEMISTO_BASE_URL="https://your-instance.xsoar.paloaltonetworks.com"
export DEMISTO_API_KEY="your-api-key"

# Optional
export DEMISTO_VERIFY_SSL="true"
```

---

## Verification

Test your setup:

```bash
# Verify SDK installation
demisto-sdk --version

# Test platform connectivity
demisto-sdk download --list-files

# Validate existing content
demisto-sdk validate -i Packs/HelloWorld
```

