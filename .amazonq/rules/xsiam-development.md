# XSIAM Development Rules for Amazon Q

## Project Context
This repository contains Cortex XSIAM/XSOAR content including playbooks, scripts, and integrations for security automation.

## Key References
- `CLAUDE.md` - Detailed development guide
- `Agents.md` - Agent role definitions
- `Packs/CommonPlaybooks/Playbooks/` - Playbook patterns
- `Packs/CommonScripts/Scripts/` - Script patterns
- `Packs/HelloWorld/Integrations/` - Integration template

## Development Commands

### Scaffolding
```bash
demisto-sdk init --pack -n "PackName" -o Packs/
demisto-sdk init --integration -n "IntegrationName" -o Packs/PackName/Integrations/
demisto-sdk init --script -n "ScriptName" -o Packs/PackName/Scripts/
```

### Validation
```bash
demisto-sdk format -i <path> -y
demisto-sdk validate -i <path>
demisto-sdk generate-docs -i <yml_path> -f
```

## Code Standards

### Playbook Structure
```yaml
id: Playbook_Name
name: Playbook Name
description: Description
starttaskid: "0"
tasks:
  "0":
    type: start
    nexttasks:
      '#none#': ["1"]
inputs:
  - key: InputName
    description: Description
outputs:
  - contextPath: Output.Path
    description: Description
```

### Script Structure
```python
import demistomock as demisto
from CommonServerPython import *

def main():
    try:
        args = demisto.args()
        result = process(args)
        return_results(CommandResults(
            outputs_prefix='ScriptName',
            outputs=result
        ))
    except Exception as e:
        return_error(f'Error: {str(e)}')

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
```

### Integration Structure
```python
import demistomock as demisto
from CommonServerPython import *

class Client(BaseClient):
    def __init__(self, base_url, verify, proxy, headers):
        super().__init__(base_url=base_url, verify=verify, proxy=proxy, headers=headers)

def main():
    params = demisto.params()
    command = demisto.command()
    client = Client(...)
    
    if command == 'test-module':
        return_results('ok')
    # Handle other commands

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
```

## Context Paths
- `Endpoint.*` - Endpoint data
- `Account.*` - User accounts  
- `File.*`, `IP.*`, `Domain.*`, `URL.*` - Indicators
- `incident.*` - Incident fields

## Best Practices
1. Use sub-playbooks for reusable logic
2. Single responsibility for scripts
3. Inherit from BaseClient for integrations
4. Include unit tests
5. Generate documentation
6. Run format and validate before commit

