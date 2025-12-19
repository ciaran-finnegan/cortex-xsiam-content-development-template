#!/usr/bin/env python3
"""XSIAM Development Helper - Wrapper for demisto-sdk operations."""

import json
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class ContentType(Enum):
    """Content types supported by demisto-sdk."""
    PACK = "pack"
    INTEGRATION = "integration"
    SCRIPT = "script"
    PLAYBOOK = "playbook"


@dataclass
class CommandResult:
    """Result of a demisto-sdk command execution."""
    success: bool
    stdout: str
    stderr: str
    return_code: int

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code
        }


def run_sdk_command(args: list[str], cwd: Optional[Path] = None) -> CommandResult:
    """Execute a demisto-sdk command."""
    cmd = ["demisto-sdk"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return CommandResult(
        success=result.returncode == 0,
        stdout=result.stdout,
        stderr=result.stderr,
        return_code=result.returncode
    )


def init_pack(name: str, output_dir: str = "Packs") -> CommandResult:
    """Initialise a new content pack.
    
    Args:
        name: Pack name (PascalCase)
        output_dir: Output directory
    
    Returns:
        CommandResult with execution details
    """
    return run_sdk_command([
        "init", "--pack",
        "-n", name,
        "-o", output_dir
    ])


def init_integration(name: str, pack_path: str, template: str = "HelloWorld") -> CommandResult:
    """Initialise a new integration.
    
    Args:
        name: Integration name (PascalCase)
        pack_path: Path to parent pack
        template: Template to use
    
    Returns:
        CommandResult with execution details
    """
    output = str(Path(pack_path) / "Integrations")
    args = [
        "init", "--integration",
        "-n", name,
        "-o", output
    ]
    if template:
        args.extend(["-t", template])
    return run_sdk_command(args)


def init_script(name: str, pack_path: str) -> CommandResult:
    """Initialise a new script.
    
    Args:
        name: Script name (PascalCase)
        pack_path: Path to parent pack
    
    Returns:
        CommandResult with execution details
    """
    output = str(Path(pack_path) / "Scripts")
    return run_sdk_command([
        "init", "--script",
        "-n", name,
        "-o", output
    ])


def format_content(path: str, update_docker: bool = False) -> CommandResult:
    """Format content to Cortex standards.
    
    Args:
        path: Path to content
        update_docker: Update Docker image
    
    Returns:
        CommandResult with execution details
    """
    args = ["format", "-i", path, "-y"]
    if update_docker:
        args.append("-ud")
    return run_sdk_command(args)


def validate_content(
    path: str,
    use_git: bool = False,
    no_backward_comp: bool = False
) -> CommandResult:
    """Validate content structure and schema.
    
    Args:
        path: Path to content
        use_git: Validate only changed files
        no_backward_comp: Skip backward compatibility
    
    Returns:
        CommandResult with execution details
    """
    args = ["validate", "-i", path]
    if use_git:
        args.append("-g")
    if no_backward_comp:
        args.append("--no-backward-comp")
    return run_sdk_command(args)


def lint_content(path: str, docker: bool = True, test: bool = True) -> CommandResult:
    """Run linting and tests on content.
    
    Args:
        path: Path to integration/script
        docker: Run in Docker
        test: Run unit tests
    
    Returns:
        CommandResult with execution details
    """
    args = ["lint", "-i", path]
    if not docker:
        args.append("--no-docker")
    if not test:
        args.append("--no-test")
    return run_sdk_command(args)


def generate_docs(input_path: str, output_dir: Optional[str] = None) -> CommandResult:
    """Generate README documentation.
    
    Args:
        input_path: Path to YAML file
        output_dir: Output directory
    
    Returns:
        CommandResult with execution details
    """
    args = ["generate-docs", "-i", input_path, "-f"]
    if output_dir:
        args.extend(["-o", output_dir])
    return run_sdk_command(args)


def generate_unit_tests(input_path: str, output_dir: Optional[str] = None) -> CommandResult:
    """Generate unit test scaffolds.
    
    Args:
        input_path: Path to YAML file
        output_dir: Output directory
    
    Returns:
        CommandResult with execution details
    """
    args = ["generate-unit-tests", "-i", input_path]
    if output_dir:
        args.extend(["-o", output_dir])
    return run_sdk_command(args)


def upload_content(path: str, insecure: bool = False) -> CommandResult:
    """Upload content to XSOAR/XSIAM instance.
    
    Requires DEMISTO_BASE_URL and DEMISTO_API_KEY environment variables.
    
    Args:
        path: Path to content
        insecure: Skip SSL verification
    
    Returns:
        CommandResult with execution details
    """
    args = ["upload", "-i", path]
    if insecure:
        args.append("--insecure")
    return run_sdk_command(args)


def validate_and_format(path: str) -> dict:
    """Format then validate content.
    
    Args:
        path: Path to content
    
    Returns:
        Dict with format and validate results
    """
    format_result = format_content(path)
    validate_result = validate_content(path)
    return {
        "format": format_result.to_dict(),
        "validate": validate_result.to_dict(),
        "overall_success": format_result.success and validate_result.success
    }


def full_pipeline(
    path: str,
    lint: bool = True,
    docs: bool = True,
    upload: bool = False
) -> dict:
    """Run full validation pipeline.
    
    Args:
        path: Path to content
        lint: Run linting
        docs: Generate documentation
        upload: Upload to instance
    
    Returns:
        Dict with all results
    """
    results = {
        "path": path,
        "steps": {}
    }
    
    # Format
    results["steps"]["format"] = format_content(path).to_dict()
    if not results["steps"]["format"]["success"]:
        results["overall_success"] = False
        return results
    
    # Validate
    results["steps"]["validate"] = validate_content(path).to_dict()
    if not results["steps"]["validate"]["success"]:
        results["overall_success"] = False
        return results
    
    # Lint (optional)
    if lint:
        results["steps"]["lint"] = lint_content(path).to_dict()
    
    # Docs (optional)
    if docs:
        yml_files = list(Path(path).rglob("*.yml"))
        for yml in yml_files:
            if not yml.name.startswith("_"):
                results["steps"][f"docs_{yml.stem}"] = generate_docs(str(yml)).to_dict()
    
    # Upload (optional)
    if upload:
        results["steps"]["upload"] = upload_content(path).to_dict()
    
    results["overall_success"] = all(
        step.get("success", True) 
        for step in results["steps"].values()
    )
    return results


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("""
XSIAM Development Helper

Usage:
    xsiam_dev_helper.py <command> [args]

Commands:
    init-pack <name> [output_dir]
    init-integration <name> <pack_path> [template]
    init-script <name> <pack_path>
    format <path>
    validate <path>
    lint <path>
    docs <yml_path>
    tests <yml_path>
    upload <path>
    pipeline <path> [--no-lint] [--no-docs] [--upload]
    validate-format <path>
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "init-pack": lambda: init_pack(args[0], args[1] if len(args) > 1 else "Packs"),
        "init-integration": lambda: init_integration(
            args[0], args[1], args[2] if len(args) > 2 else "HelloWorld"
        ),
        "init-script": lambda: init_script(args[0], args[1]),
        "format": lambda: format_content(args[0]),
        "validate": lambda: validate_content(args[0]),
        "lint": lambda: lint_content(args[0]),
        "docs": lambda: generate_docs(args[0]),
        "tests": lambda: generate_unit_tests(args[0]),
        "upload": lambda: upload_content(args[0]),
        "validate-format": lambda: validate_and_format(args[0]),
        "pipeline": lambda: full_pipeline(
            args[0],
            lint="--no-lint" not in args,
            docs="--no-docs" not in args,
            upload="--upload" in args
        )
    }
    
    if command not in commands:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    result = commands[command]()
    
    if isinstance(result, CommandResult):
        print(json.dumps(result.to_dict(), indent=2))
        sys.exit(0 if result.success else 1)
    else:
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("overall_success", False) else 1)


if __name__ == "__main__":
    main()

