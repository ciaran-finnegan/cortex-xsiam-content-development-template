# Contributing

Guidelines for contributing to this XSIAM content repository.

## Development Setup

### Prerequisites

- Python 3.10+
- Git
- demisto-sdk (`pip install demisto-sdk`)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd <repository>

# Install dependencies
pip install demisto-sdk pre-commit

# Install pre-commit hooks
pre-commit install

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

## Creating Content

### New Pack

```bash
demisto-sdk init --pack -n "PackName" -o Packs/
```

### New Integration

```bash
demisto-sdk init --integration -n "IntegrationName" -o Packs/PackName/Integrations/
```

### New Script

```bash
demisto-sdk init --script -n "ScriptName" -o Packs/PackName/Scripts/
```

## Code Standards

### Python

- Python 3.10+
- Follow PEP 8
- Use type hints
- Import `demistomock` and `CommonServerPython`

### YAML

- Use demisto-sdk format for consistency
- Include descriptions for all fields
- Follow naming conventions

### Documentation

- Generate README with `demisto-sdk generate-docs`
- Include usage examples
- Document all inputs/outputs

## Validation

Before submitting:

```bash
# Format content
demisto-sdk format -i Packs/YourPack -y

# Validate structure
demisto-sdk validate -i Packs/YourPack

# Run linting
demisto-sdk lint -i Packs/YourPack

# Generate documentation
demisto-sdk generate-docs -i Packs/YourPack/path/to/yml -f
```

## Pull Request Process

1. Create feature branch from `main`
2. Make changes
3. Run validation (format, validate, lint)
4. Commit with descriptive message
5. Push and create pull request
6. Address review feedback

### Commit Messages

```
[PackName] Brief description

- Detail 1
- Detail 2
```

### Branch Naming

- `feature/pack-name-description`
- `fix/pack-name-issue`
- `docs/description`

## Testing

### Unit Tests

```bash
# Run tests for a pack
demisto-sdk lint -i Packs/YourPack --test
```

### Test Playbooks

Include test playbooks in `Packs/YourPack/TestPlaybooks/`.

## Release Process

1. Update release notes:
   ```bash
   demisto-sdk update-release-notes -i Packs/YourPack -u revision
   ```

2. Validate changes
3. Create pull request
4. Merge to main
5. Tag release (if applicable)

## Resources

- [Demisto SDK Documentation](https://xsoar.pan.dev/docs/concepts/demisto-sdk)
- [Content Contribution Guide](https://xsoar.pan.dev/docs/contributing/contributing)
- [Playbook Conventions](https://xsoar.pan.dev/docs/playbooks/playbook-conventions)

