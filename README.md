# XSIAM Content Development Template

**Alpha** - Not suitable for production use. APIs, structure, and documentation may change.

Template for developing Cortex XSIAM/XSOAR playbooks, scripts, and integrations with LLM coding assistant support.

## Features

- LLM assistant configurations for Cursor, Claude Code CLI, Amazon Q, Cline
- Demisto SDK integration for scaffolding, validation, and deployment
- Pre-commit hooks for automated quality checks
- MCP tool definitions for Model Context Protocol servers

## Quick Start

### 1. Create from Template

```bash
gh repo create my-xsiam-content --template ciaran-finnegan/cortex-xsiam-content-development-template

# Or clone directly
git clone https://github.com/ciaran-finnegan/cortex-xsiam-content-development-template.git my-xsiam-content
cd my-xsiam-content
rm -rf .git && git init
```

### 2. Install Dependencies

```bash
pip install demisto-sdk pre-commit
pre-commit install
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit with your XSIAM credentials
```

### 4. Create Your First Pack

```bash
demisto-sdk init --pack -n "MyPack" -o Packs/
```

## Repository Structure

```
.
├── CLAUDE.md                    # Claude Code CLI context
├── Agents.md                    # Agent role definitions
├── .cursorrules                 # Cursor IDE rules
├── .clinerules                  # Cline assistant rules
├── .amazonq/rules/              # Amazon Q Developer rules
├── .pre-commit-config.yaml      # Pre-commit hooks
├── scripts/xsiam_dev_helper.py  # SDK wrapper utilities
├── docs/                        # Documentation
├── mcps/demisto-sdk/tools/      # MCP tool definitions
└── Packs/                       # Your content packs
```

## LLM Assistant Support

| Assistant | Config File |
|-----------|-------------|
| [Cursor](https://cursor.sh) | `.cursorrules` |
| [Claude Code CLI](https://github.com/anthropics/anthropic-cookbook) | `CLAUDE.md` |
| [Amazon Q Developer](https://aws.amazon.com/q/developer/) | `.amazonq/rules/` |
| [Cline](https://github.com/cline/cline) | `.clinerules` |

## Commands

| Task | Command |
|------|---------|
| Create pack | `demisto-sdk init --pack -n "PackName" -o Packs/` |
| Create integration | `demisto-sdk init --integration -n "Name" -o Packs/PackName/Integrations/` |
| Create script | `demisto-sdk init --script -n "Name" -o Packs/PackName/Scripts/` |
| Format | `demisto-sdk format -i Packs/PackName -y` |
| Validate | `demisto-sdk validate -i Packs/PackName` |
| Generate docs | `demisto-sdk generate-docs -i <yml_path> -f` |
| Upload | `demisto-sdk upload -i Packs/PackName` |

## Related Repositories

| Repository | Description |
|------------|-------------|
| [demisto/demisto-sdk](https://github.com/demisto/demisto-sdk) | Official Cortex XSOAR/XSIAM SDK |
| [demisto/content](https://github.com/demisto/content) | Official content library |
| [cortex-xsiam-sdk-mcp-tools](https://github.com/ciaran-finnegan/cortex-xsiam-sdk-mcp-tools) | MCP server for demisto-sdk |

## MCP Tools

Tool definitions in `mcps/demisto-sdk/tools/`:

| Tool | Purpose |
|------|---------|
| `init_pack` | Create pack structure |
| `init_integration` | Scaffold integration |
| `init_script` | Scaffold script |
| `format_content` | Standardise formatting |
| `validate_content` | Check validity |
| `generate_docs` | Create documentation |
| `upload_content` | Deploy to platform |
| `download_content` | Sync from platform |

## Resources

- [Cortex XSOAR Developer Docs](https://xsoar.pan.dev/docs/)
- [Demisto SDK Documentation](https://xsoar.pan.dev/docs/concepts/demisto-sdk)
- [Content Contribution Guide](https://xsoar.pan.dev/docs/contributing/contributing)

## Licence

MIT - See [LICENSE](LICENSE).
