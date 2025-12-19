# XSIAM LLM-Assisted Development Plan

## Overview

Integration of Demisto SDK with LLM coding assistants (Cursor, Claude Code CLI, Codex) for automated playbook and script development.

## Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#005A9C', 'primaryTextColor': '#fff', 'primaryBorderColor': '#003d66', 'lineColor': '#FFD700', 'secondaryColor': '#FFD700', 'tertiaryColor': '#f0f0f0'}}}%%
flowchart TB
    subgraph LLM["LLM Coding Assistant"]
        direction TB
        A[Cursor/Claude/Codex]
    end

    subgraph Context["Knowledge Base"]
        direction TB
        B1[CLAUDE.md]
        B2[Agents.md]
        B3[Pattern Library]
        B4[Schema Definitions]
    end

    subgraph MCP["MCP Server Layer"]
        direction TB
        C1[demisto-sdk MCP]
        C2[user-cortex MCP]
    end

    subgraph SDK["Demisto SDK"]
        direction TB
        D1[init]
        D2[validate]
        D3[format]
        D4[generate-docs]
        D5[lint]
    end

    subgraph Output["Generated Content"]
        direction TB
        E1[Playbooks]
        E2[Scripts]
        E3[Integrations]
    end

    A --> Context
    A --> MCP
    MCP --> SDK
    SDK --> Output
    Output -->|pre-commit| SDK

    style LLM fill:#005A9C,stroke:#003d66,color:#fff
    style Context fill:#FFD700,stroke:#cc9900,color:#000
    style MCP fill:#005A9C,stroke:#003d66,color:#fff
    style SDK fill:#f0f0f0,stroke:#ccc,color:#000
    style Output fill:#FFD700,stroke:#cc9900,color:#000
```

## Development Workflow

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#005A9C', 'primaryTextColor': '#fff', 'lineColor': '#FFD700'}}}%%
sequenceDiagram
    participant Dev as Developer
    participant LLM as LLM Assistant
    participant SDK as Demisto SDK
    participant XSIAM as XSIAM Platform

    Dev->>LLM: Request playbook/script
    LLM->>LLM: Reference knowledge base
    LLM->>SDK: demisto-sdk init
    SDK-->>LLM: Scaffold structure
    LLM->>LLM: Generate code
    LLM->>SDK: demisto-sdk format
    SDK-->>LLM: Formatted output
    LLM->>SDK: demisto-sdk validate
    alt Validation fails
        SDK-->>LLM: Errors
        LLM->>LLM: Fix errors
        LLM->>SDK: Re-validate
    end
    SDK-->>LLM: Valid
    LLM->>SDK: demisto-sdk generate-docs
    SDK-->>LLM: Documentation
    LLM-->>Dev: Complete package
    Dev->>SDK: demisto-sdk upload
    SDK->>XSIAM: Deploy content
```

## Component Structure

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#005A9C', 'primaryTextColor': '#fff', 'lineColor': '#FFD700'}}}%%
graph LR
    subgraph Root["Project Root"]
        A[CLAUDE.md]
        B[Agents.md]
        C[.cursorrules]
        D[.pre-commit-config.yaml]
    end

    subgraph Scripts["scripts/"]
        E[xsiam_dev_helper.py]
    end

    subgraph MCP["mcps/demisto-sdk/"]
        F1[init_pack.json]
        F2[validate_content.json]
        F3[format_content.json]
        F4[generate_docs.json]
    end

    subgraph Docs["docs/xsiam-kb/"]
        G1[schemas/]
        G2[patterns/]
        G3[examples/]
    end

    Root --> Scripts
    Root --> MCP
    Root --> Docs

    style Root fill:#005A9C,stroke:#003d66,color:#fff
    style Scripts fill:#FFD700,stroke:#cc9900,color:#000
    style MCP fill:#005A9C,stroke:#003d66,color:#fff
    style Docs fill:#FFD700,stroke:#cc9900,color:#000
```

## Implementation Tasks

| Task | Description | Output |
|------|-------------|--------|
| MCP Extension | SDK command wrappers | `mcps/demisto-sdk/tools/*.json` |
| CLAUDE.md | Primary LLM context | `CLAUDE.md` |
| Agents.md | Agent-specific guidance | `Agents.md` |
| Helper Script | SDK automation wrapper | `scripts/xsiam_dev_helper.py` |
| Pre-commit | Validation hooks | `.pre-commit-config.yaml` |

## SDK Command Reference

| Command | Purpose | When Used |
|---------|---------|-----------|
| `init --pack` | Create pack structure | New pack |
| `init --integration` | Scaffold integration | New integration |
| `init --script` | Scaffold script | New script |
| `format` | Standardise formatting | After generation |
| `validate` | Check validity | Before commit |
| `generate-docs` | Create README | After validation |
| `lint` | Code quality | CI/CD |
| `upload` | Deploy to platform | Testing |

## Quality Gates

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#005A9C', 'primaryTextColor': '#fff', 'lineColor': '#FFD700'}}}%%
flowchart LR
    A[Code Generated] --> B{Format}
    B -->|Pass| C{Validate}
    B -->|Fail| A
    C -->|Pass| D{Lint}
    C -->|Fail| A
    D -->|Pass| E{Tests}
    D -->|Fail| A
    E -->|Pass| F[Commit]
    E -->|Fail| A

    style A fill:#FFD700,stroke:#cc9900,color:#000
    style F fill:#005A9C,stroke:#003d66,color:#fff
```

