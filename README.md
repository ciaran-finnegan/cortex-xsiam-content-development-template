# XSIAM Content Development Template

[![Demisto SDK](https://img.shields.io/badge/demisto--sdk-1.38+-blue)](https://github.com/demisto/demisto-sdk)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange)](https://github.com/ciaran-finnegan/cortex-xsiam-content-development-template)

> ⚠️ **Alpha Release**: This template is in early development and not suitable for production use. APIs, structure, and documentation may change without notice.

Template repository for developing Cortex XSIAM/XSOAR playbooks, scripts, and integrations with LLM coding assistant support.

## Features

- 🤖 **LLM Assistant Support** - Pre-configured for Cursor, Claude Code CLI, Amazon Q, Cline
- 🛠️ **Demisto SDK Integration** - Scaffolding, validation, and deployment tools
- 📋 **Pre-commit Hooks** - Automated quality checks
- 📚 **Pattern Library** - Reference documentation and examples
- 🔌 **MCP Tools** - Model Context Protocol server definitions

## Quick Start

### 1. Create from Template

```bash
# Using GitHub template
gh repo create my-xsiam-content --template your-username/xsiam-content-template

# Or clone directly
git clone https://github.com/your-username/xsiam-content-template.git my-xsiam-content
cd my-xsiam-content
rm -rf .git && git init
```

### 2. Install Dependencies

```bash
# Install demisto-sdk
pip install demisto-sdk

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your XSIAM credentials
# DEMISTO_BASE_URL=https://your-instance.xsoar.paloaltonetworks.com
# DEMISTO_API_KEY=your-api-key
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
├── .amazonq/
│   └── rules/                   # Amazon Q Developer rules
├── .pre-commit-config.yaml      # Pre-commit hooks
├── scripts/
│   └── xsiam_dev_helper.py     # SDK wrapper utilities
├── docs/
│   ├── LLM_ASSISTANT_SETUP.md  # LLM configuration guide
│   ├── ENTERPRISE_PACKAGING.md # Enterprise deployment options
│   └── XSIAM_LLM_DEVELOPMENT_PLAN.md
├── mcps/
│   └── demisto-sdk/            # MCP tool definitions
│       └── tools/
└── Packs/                       # Your content packs
    └── .gitkeep
```

## LLM Assistant Support

| Assistant | Config File | Documentation |
|-----------|-------------|---------------|
| [Cursor](https://cursor.sh) | `.cursorrules` | [Setup Guide](docs/LLM_ASSISTANT_SETUP.md#cursor) |
| [Claude Code CLI](https://github.com/anthropics/anthropic-cookbook) | `CLAUDE.md` | [Setup Guide](docs/LLM_ASSISTANT_SETUP.md#claude-code-cli) |
| [Amazon Q Developer](https://aws.amazon.com/q/developer/) | `.amazonq/rules/` | [Setup Guide](docs/LLM_ASSISTANT_SETUP.md#amazon-q-developer) |
| [Cline](https://github.com/cline/cline) | `.clinerules` | [Setup Guide](docs/LLM_ASSISTANT_SETUP.md#cline) |

## Development Workflow

```mermaid
flowchart LR
    A[Scaffold] --> B[Generate]
    B --> C[Format]
    C --> D[Validate]
    D --> E[Test]
    E --> F[Deploy]
    
    style A fill:#005A9C,color:#fff
    style F fill:#005A9C,color:#fff
```

### Commands

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

### Required

| Repository | Description |
|------------|-------------|
| [demisto/demisto-sdk](https://github.com/demisto/demisto-sdk) | Official Cortex XSOAR/XSIAM SDK |
| [demisto/content](https://github.com/demisto/content) | Official content library (patterns & examples) |

### MCP Servers (Optional)

| Repository | Description |
|------------|-------------|
| [your-username/mcp-demisto-sdk](https://github.com/your-username/mcp-demisto-sdk) | MCP server for demisto-sdk commands |
| [your-username/mcp-xsiam](https://github.com/your-username/mcp-xsiam) | MCP server for XSIAM API (XQL, cases, assets) |

## MCP Server Setup

For Cursor and Cline MCP support, see the tool definitions in `mcps/demisto-sdk/tools/`.

To create a functional MCP server, see [mcp-demisto-sdk](https://github.com/your-username/mcp-demisto-sdk).

### Available MCP Tools

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
| `run_command` | Execute commands remotely |
| `run_playbook` | Run playbooks remotely |

## Documentation

- [LLM Assistant Setup](docs/LLM_ASSISTANT_SETUP.md) - Configure your preferred coding assistant
- [Enterprise Packaging](docs/ENTERPRISE_PACKAGING.md) - Deployment options for organisations
- [Development Plan](docs/XSIAM_LLM_DEVELOPMENT_PLAN.md) - Architecture overview

## External Resources

- [Cortex XSOAR Developer Docs](https://xsoar.pan.dev/docs/)
- [Demisto SDK Documentation](https://xsoar.pan.dev/docs/concepts/demisto-sdk)
- [Content Contribution Guide](https://xsoar.pan.dev/docs/contributing/contributing)
- [Playbook Conventions](https://xsoar.pan.dev/docs/playbooks/playbook-conventions)

## Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Run validation: `demisto-sdk format -i . -y && demisto-sdk validate -i .`
5. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

---

**Note**: This is a template repository. Replace `your-username` with your GitHub username after forking.

