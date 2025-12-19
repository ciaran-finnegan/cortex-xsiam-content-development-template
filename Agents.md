# XSIAM Development Agents

> **Supported**: Cursor, Claude Code CLI, Amazon Q Developer, Cline, Codex CLI

## LLM Assistant Configuration

| Assistant | Context File | MCP Support |
|-----------|-------------|-------------|
| Cursor | `.cursorrules` | ✓ |
| Claude Code CLI | `CLAUDE.md` | ✓ |
| Amazon Q | `.amazonq/rules/` | ✗ |
| Cline | `.clinerules` | ✓ |
| Codex CLI | Context files | ✗ |

See `docs/LLM_ASSISTANT_SETUP.md` for detailed configuration.

---

## Agent Roles

### Playbook Developer Agent

**Purpose**: Generate XSIAM playbooks from requirements.

**Workflow**:
1. Analyse requirement
2. Identify required integrations
3. Reference pattern library
4. Generate playbook YAML
5. Run `demisto-sdk format`
6. Run `demisto-sdk validate`
7. Generate documentation

**Context Required**:
- `Packs/CommonPlaybooks/Playbooks/` - Pattern examples
- `CLAUDE.md` - Structure reference
- `demisto-sdk` MCP tools

**Output Format**:
```yaml
id: Generated_Playbook_Name
name: Generated Playbook Name
description: |
  Generated playbook description.
  Requirements addressed: <list>
starttaskid: "0"
tasks:
  # Task definitions
inputs:
  # Input definitions
outputs:
  # Output definitions
```

---

### Script Developer Agent

**Purpose**: Generate XSIAM automation scripts.

**Workflow**:
1. Parse requirements
2. Identify inputs/outputs
3. Generate Python code
4. Generate YAML metadata
5. Run `demisto-sdk format`
6. Run `demisto-sdk validate`
7. Generate unit tests

**Context Required**:
- `Packs/CommonScripts/Scripts/` - Script patterns
- `Packs/ApiModules/Scripts/` - API modules
- `CLAUDE.md` - Structure reference

**Output Format**:
```
Scripts/
├── ScriptName/
│   ├── ScriptName.py
│   ├── ScriptName.yml
│   ├── ScriptName_test.py
│   └── README.md
```

---

### Integration Developer Agent

**Purpose**: Generate XSIAM integrations for external APIs.

**Workflow**:
1. Analyse API specification
2. Design command structure
3. Generate client class
4. Implement commands
5. Generate YAML configuration
6. Run validation
7. Generate documentation

**Context Required**:
- `Packs/HelloWorld/Integrations/` - Template
- `Packs/ApiModules/Scripts/` - Base classes
- API documentation (external)

**Output Format**:
```
Integrations/
├── IntegrationName/
│   ├── IntegrationName.py
│   ├── IntegrationName.yml
│   ├── IntegrationName_test.py
│   ├── IntegrationName_image.png
│   └── README.md
```

---

### Content Validator Agent

**Purpose**: Validate and fix generated content.

**Workflow**:
1. Run `demisto-sdk format -i <path> -y`
2. Run `demisto-sdk validate -i <path>`
3. Parse validation errors
4. Apply fixes
5. Re-validate
6. Report status

**Tools**:
- `format_content` MCP tool
- `validate_content` MCP tool
- `lint_content` MCP tool

**Error Handling**:
```
Validation Error → Parse Error Code → Apply Fix → Re-validate
                                    ↓
                              Report if unfixable
```

---

### Documentation Agent

**Purpose**: Generate and maintain documentation.

**Workflow**:
1. Run `demisto-sdk generate-docs -i <yml_path> -f`
2. Enhance generated README
3. Add usage examples
4. Add troubleshooting

**Output**:
- README.md for each content item
- Pack README.md
- Release notes

---

## Agent Communication

### Task Handoff

```yaml
handoff:
  from: playbook_developer
  to: content_validator
  payload:
    path: Packs/MyPack/Playbooks/MyPlaybook.yml
    action: validate
```

### Validation Response

```yaml
response:
  from: content_validator
  status: success|failure
  errors: []
  warnings: []
  path: <validated_path>
```

---

## SDK Command Reference

### Scaffolding

| Command | Agent | Purpose |
|---------|-------|---------|
| `init --pack` | All | Create pack |
| `init --integration` | Integration Agent | Scaffold integration |
| `init --script` | Script Agent | Scaffold script |

### Validation

| Command | Agent | Purpose |
|---------|-------|---------|
| `format -i <path> -y` | Validator | Standardise |
| `validate -i <path>` | Validator | Check validity |
| `lint -i <path>` | Validator | Code quality |

### Documentation

| Command | Agent | Purpose |
|---------|-------|---------|
| `generate-docs -i <yml> -f` | Documentation | Create README |
| `generate-unit-tests -i <yml>` | Script/Integration | Test scaffolds |

### Deployment

| Command | Agent | Purpose |
|---------|-------|---------|
| `upload -i <path>` | All | Deploy to instance |
| `run-playbook -n <name>` | Playbook Agent | Test execution |

---

## Pattern Library

### Enrichment Pattern

```yaml
# Pattern: Multi-source enrichment with fallback
tasks:
  "1":
    type: title
    name: Enrichment Sources
    nexttasks:
      '#none#': ["2", "3", "4"]  # Parallel execution
  "2":
    type: condition
    name: Is Source A Available?
    # Check integration availability
  "3":
    type: condition
    name: Is Source B Available?
  "4":
    type: condition
    name: Is Source C Available?
```

### Remediation Pattern

```yaml
# Pattern: Approval-gated remediation
tasks:
  "1":
    type: condition
    name: Auto-remediate?
    conditions:
      - label: "yes"
        condition:
          - - operator: isEqualString
              left:
                value:
                  simple: ${inputs.AutoRemediate}
              right:
                value:
                  simple: "true"
    nexttasks:
      '#default#': ["manual_approval"]
      "yes": ["auto_remediate"]
```

### Polling Pattern

```yaml
# Pattern: Async operation polling
tasks:
  "1":
    type: playbook
    name: GenericPolling
    scriptarguments:
      ids:
        simple: ${operation_id}
      pollingCommand:
        simple: integration-get-status
      pollingCommandArgName:
        simple: id
      dt:
        simple: Status.state
      pendingIds:
        simple: pending,running
```

---

## Error Codes

### Common Validation Errors

| Code | Description | Fix |
|------|-------------|-----|
| `BA100` | Missing required field | Add field |
| `BA101` | Invalid field value | Correct value |
| `IF100` | Invalid fromversion | Update version |
| `IN100` | Invalid integration name | Rename |
| `PB100` | Invalid playbook structure | Fix YAML |
| `SC100` | Invalid script structure | Fix YAML |

### Auto-fixable Errors

Run `demisto-sdk format -i <path> -y` to auto-fix:
- Field ordering
- Missing default values
- YAML formatting
- Docker image updates

---

## Environment Variables

```bash
# Required for upload/download
export DEMISTO_BASE_URL="https://your-instance.xsoar.paloaltonetworks.com"
export DEMISTO_API_KEY="your-api-key"

# Optional
export DEMISTO_VERIFY_SSL="false"  # For self-signed certs
```

---

## Agent Prompts

### Playbook Generation Prompt

```
Create an XSIAM playbook that:
- Purpose: <description>
- Inputs: <list>
- Integrations: <list>
- Outputs: <list>

Reference: Packs/CommonPlaybooks/Playbooks/ for patterns
Validate with: demisto-sdk format && demisto-sdk validate
```

### Script Generation Prompt

```
Create an XSIAM script that:
- Purpose: <description>
- Arguments: <list>
- Outputs: <list>
- Dependencies: <list>

Reference: Packs/CommonScripts/Scripts/ for patterns
Include: Unit tests, README
Validate with: demisto-sdk format && demisto-sdk validate
```

### Integration Generation Prompt

```
Create an XSIAM integration for:
- API: <name/url>
- Authentication: <method>
- Commands: <list>

Reference: Packs/HelloWorld/Integrations/HelloWorld/
Include: Test module, unit tests, README
Validate with: demisto-sdk format && demisto-sdk validate
```

