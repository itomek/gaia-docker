<test-skill>
# Test Skill

Run tests with appropriate options for the GAIA Docker project.

## Usage

```
/test
```

## Workflow

1. **Ask test scope**: unit tests, integration tests, or all
2. **Run appropriate pytest commands**
3. **Report results** with pass/fail summary

## Instructions

When the user invokes `/test`:

### Step 1: Ask Test Scope

Use AskUserQuestion to ask:
- "What tests would you like to run?"
  - **Unit tests** - Fast tests without container builds (test_dockerfile*.py, test_entrypoint*.py)
  - **Integration tests** - Tests requiring Docker (test_container.py)
  - **All tests** - Run complete test suite

### Step 2: Run Tests

For **Unit tests**:
```bash
uv run pytest tests/test_dockerfile.py tests/test_dockerfile_dev.py tests/test_entrypoint.py tests/test_entrypoint_dev.py -v
```

For **Integration tests**:
```bash
uv run pytest tests/test_container.py -v -m integration
```

For **All tests**:
```bash
uv run pytest tests/ -v
```

### Step 3: Report Results

After test completion, summarize:
- Total tests run
- Passed/failed count
- Any failed test names and brief error descriptions

## Example Interaction

```
User: /test

Claude: What tests would you like to run?
[Unit tests] [Integration tests] [All tests]

User: Unit tests

Claude: Running unit tests...

[Executes pytest]

Test Results:
- 24 tests passed
- 0 tests failed

All unit tests passing!
```

## Test Categories

### Unit Tests (fast, no Docker required)
- `test_dockerfile.py` - gaia-linux Dockerfile syntax and structure
- `test_dockerfile_dev.py` - gaia-dev Dockerfile syntax and structure
- `test_entrypoint.py` - gaia-linux entrypoint script logic
- `test_entrypoint_dev.py` - gaia-dev entrypoint script logic

### Integration Tests (slower, requires Docker)
- `test_container.py` - Actual container builds and runtime verification

## Prerequisites

- `uv sync` must have been run to install test dependencies
- Integration tests require Docker to be running
</test-skill>
