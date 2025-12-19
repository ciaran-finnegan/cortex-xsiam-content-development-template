# XSIAM Content Development

> **Supported LLM Assistants**: Cursor, Claude Code CLI, Amazon Q Developer, Cline, Codex CLI

## Repository

Cortex XSOAR/XSIAM content library containing playbooks, scripts, and integrations.

## External References

- **Demisto SDK**: [github.com/demisto/demisto-sdk](https://github.com/demisto/demisto-sdk)
- **Content Library**: [github.com/demisto/content](https://github.com/demisto/content)
- **Developer Docs**: [xsoar.pan.dev](https://xsoar.pan.dev/docs/)

## Quick Reference

### Creating Content

```bash
# New pack
demisto-sdk init --pack -n "PackName" -o Packs/

# New integration
demisto-sdk init --integration -n "IntegrationName" -o Packs/PackName/Integrations/

# New script
demisto-sdk init --script -n "ScriptName" -o Packs/PackName/Scripts/
```

### Validation Workflow

```bash
demisto-sdk format -i Packs/PackName -y
demisto-sdk validate -i Packs/PackName
demisto-sdk generate-docs -i <yml_path> -f
```

## Playbook Structure

```yaml
id: Playbook_Name
name: Playbook Name
description: Brief description
starttaskid: "0"
tasks:
  "0":
    id: "0"
    taskid: <uuid>
    type: start
    nexttasks:
      '#none#': ["1"]
  "1":
    id: "1"
    taskid: <uuid>
    type: regular
    task:
      id: <uuid>
      name: Task Name
      script: integration|||command
      iscommand: true
    scriptarguments:
      arg_name:
        simple: ${inputs.InputName}
    nexttasks:
      '#none#': ["2"]
inputs:
  - key: InputName
    value: {}
    required: false
    description: Input description
outputs:
  - contextPath: Output.Path
    description: Output description
    type: string
```

### Task Types

| Type | Purpose |
|------|---------|
| `start` | Entry point |
| `title` | Section header |
| `condition` | Branch logic |
| `regular` | Execute command |
| `playbook` | Sub-playbook |
| `manual` | Human task |

### Condition Syntax

```yaml
type: condition
conditions:
  - label: "yes"
    condition:
      - - operator: isNotEmpty
          left:
            value:
              simple: ${SomeContext.Value}
            iscontext: true
nexttasks:
  '#default#': ["fallback_task"]
  "yes": ["success_task"]
```

## Script Structure

```python
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *


def main():
    try:
        args = demisto.args()
        # Implementation
        result = process_data(args)
        return_results(CommandResults(
            outputs_prefix='ScriptName',
            outputs_key_field='id',
            outputs=result
        ))
    except Exception as e:
        return_error(f'Error: {str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
```

### Script YAML

```yaml
args:
  - name: input_arg
    description: Argument description
    required: true
comment: Script description
commonfields:
  id: ScriptName
  version: -1
name: ScriptName
outputs:
  - contextPath: ScriptName.Output
    description: Output description
    type: String
script: ''
type: python
subtype: python3
dockerimage: demisto/python3:3.10.13.86272
fromversion: 6.5.0
```

## Integration Structure

```python
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

INTEGRATION_NAME = 'IntegrationName'


class Client(BaseClient):
    def __init__(self, base_url: str, verify: bool, proxy: bool, headers: dict):
        super().__init__(base_url=base_url, verify=verify, proxy=proxy, headers=headers)

    def api_call(self, endpoint: str) -> dict:
        return self._http_request(method='GET', url_suffix=endpoint)


def test_module(client: Client) -> str:
    client.api_call('/test')
    return 'ok'


def command_handler(client: Client, args: dict) -> CommandResults:
    result = client.api_call(args.get('endpoint'))
    return CommandResults(
        outputs_prefix=f'{INTEGRATION_NAME}.Result',
        outputs_key_field='id',
        outputs=result,
        readable_output=tableToMarkdown('Results', result)
    )


def main():
    params = demisto.params()
    command = demisto.command()
    args = demisto.args()

    base_url = params.get('url')
    verify = not params.get('insecure', False)
    proxy = params.get('proxy', False)
    headers = {'Authorization': f"Bearer {params.get('api_key')}"}

    client = Client(base_url=base_url, verify=verify, proxy=proxy, headers=headers)

    commands = {
        'test-module': test_module,
        f'{INTEGRATION_NAME.lower()}-command': command_handler,
    }

    try:
        return_results(commands[command](client, args) if command != 'test-module' 
                       else commands[command](client))
    except Exception as e:
        return_error(f'Error: {str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
```

## Context Paths

### Standard Indicators

| Path | Type | Description |
|------|------|-------------|
| `IP.Address` | String | IP address |
| `Domain.Name` | String | Domain name |
| `File.SHA256` | String | File hash |
| `URL.Data` | String | URL |
| `Account.Username` | String | Account name |

### Endpoint Data

| Path | Description |
|------|-------------|
| `Endpoint.Hostname` | Hostname |
| `Endpoint.ID` | Endpoint identifier |
| `Endpoint.IPAddress` | IP addresses |
| `Endpoint.OS` | Operating system |
| `Endpoint.Status` | Online/Offline |
| `Endpoint.IsIsolated` | Isolation status |

### Incident Fields

| Path | Description |
|------|-------------|
| `incident.id` | Incident ID |
| `incident.name` | Incident name |
| `incident.severity` | Severity (1-4) |
| `incident.type` | Incident type |
| `incident.labels` | Labels array |

## Transformers

```yaml
# Common transformers in scriptarguments
transformers:
  - operator: uniq           # Remove duplicates
  - operator: toLowerCase    # Convert to lowercase
  - operator: toUpperCase    # Convert to uppercase
  - operator: split
    args:
      delimiter:
        value:
          simple: ","
  - operator: join
    args:
      separator:
        value:
          simple: ", "
  - operator: getField
    args:
      field:
        value:
          simple: fieldName
```

## Reference Examples

For patterns and examples, see the official content library:
- **Enrichment**: `CommonPlaybooks/Playbooks/playbook-Endpoint_Enrichment_-_Generic_v2.1.yml`
- **XDR Handling**: `CortexXDR/Playbooks/Cortex_XDR_incident_handling_v3_6_5.yml`
- **Script**: `CommonScripts/Scripts/Set/Set.py`
- **Integration**: `HelloWorld/Integrations/HelloWorld/HelloWorld.py`

Browse at: [github.com/demisto/content/tree/master/Packs](https://github.com/demisto/content/tree/master/Packs)

## Best Practices

1. **Playbooks**: Use sub-playbooks for reusable logic
2. **Scripts**: Single responsibility, clear inputs/outputs
3. **Integrations**: Inherit from `BaseClient`, use `CommandResults`
4. **Testing**: Include test playbooks and unit tests
5. **Documentation**: Generate docs with `demisto-sdk generate-docs`
6. **Validation**: Run `format` then `validate` before commit

