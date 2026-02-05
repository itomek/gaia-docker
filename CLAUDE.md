# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository provides Docker containers for AMD GAIA (AI framework). Two container variants are maintained:
- **gaia-linux**: Runtime container where GAIA is installed from PyPI at startup
- **gaia-dev**: Development container with GAIA source code, Claude Code, and development tools pre-installed

## Repository Structure

```
gaia-linux/
  Dockerfile           # Runtime container definition
  entrypoint.sh        # Startup script that installs GAIA from PyPI

gaia-dev/
  Dockerfile           # Development container definition
  entrypoint.sh        # Startup script that clones GAIA and configures dev tools

tests/                 # pytest-based test suite
  test_dockerfile.py        # Tests for gaia-linux Dockerfile
  test_dockerfile_dev.py    # Tests for gaia-dev Dockerfile
  test_entrypoint.py        # Tests for gaia-linux entrypoint
  test_entrypoint_dev.py    # Tests for gaia-dev entrypoint
  test_container.py         # Integration tests (marked with @pytest.mark.integration)

VERSION.json           # Single source of truth for container versions
```

## Development Commands

### Testing

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest tests/ -v

# Run specific test suites
uv run pytest tests/test_dockerfile.py -v           # gaia-linux Dockerfile tests
uv run pytest tests/test_dockerfile_dev.py -v       # gaia-dev Dockerfile tests
uv run pytest tests/test_entrypoint.py -v           # gaia-linux entrypoint tests
uv run pytest tests/test_entrypoint_dev.py -v       # gaia-dev entrypoint tests

# Run integration tests (requires Docker)
uv run pytest tests/test_container.py -v -m integration
```

### Building Images

```bash
# Build gaia-linux
docker build -f gaia-linux/Dockerfile -t itomek/gaia-linux:0.15.3 .

# Build gaia-dev
docker build -f gaia-dev/Dockerfile -t itomek/gaia-dev:1.0.0 .

# Build with specific GAIA version
docker build -f gaia-linux/Dockerfile --build-arg GAIA_VERSION=0.15.2 -t itomek/gaia-linux:0.15.2 .
```

### Running Containers Locally

```bash
# gaia-linux
docker run -dit \
  --name gaia-linux-test \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.3

# gaia-dev
docker run -dit \
  --name gaia-dev-test \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GITHUB_TOKEN=ghp_... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  itomek/gaia-dev:1.0.0

# Connect to container
docker exec -it gaia-linux-test zsh
```

## Architecture

### gaia-linux Container Flow
1. Base: Ubuntu 24.04 LTS with system Python 3.12 and Node.js 20
2. System dependencies installed (git, audio libraries, build tools)
3. User `gaia` created with passwordless sudo
4. uv (fast Python package installer) installed
5. **At runtime** (entrypoint.sh):
   - Validates LEMONADE_BASE_URL is set
   - Installs `amd-gaia[dev,mcp,eval,rag]==<version>` from PyPI using uv
   - First run: ~2-3 minutes, cached runs: ~30 seconds

### gaia-dev Container Flow
1. Base: Ubuntu 24.04 LTS with uv-managed Python 3.12 and Node.js 20
   - Claude Code installed globally via npm
   - Network isolation packages (iptables, ipset, iproute2) for sandboxing
   - Virtual environment created at /home/gaia/.venv (owned by gaia user)
2. **At runtime** (entrypoint.sh):
   - Validates LEMONADE_BASE_URL is set
   - Clones GAIA from GitHub (if not present in volume)
   - Installs GAIA in editable mode with uv (into virtual environment, no sudo required)
   - Configures GitHub CLI if GITHUB_TOKEN provided
   - Sets up ANTHROPIC_API_KEY for Claude Code

### Key Design Decisions
- **gaia-linux** installs from PyPI for production use cases and reproducibility
- **gaia-dev** clones from source for development and contributions
- Both use uv for 10-100x faster Python package installation vs pip
- **gaia-dev** uses virtual environment for package isolation and user-owned files (no sudo required)
- VERSION.json file is single source of truth, read by CI/CD (independent versions per container)
- No `latest` tag - all versions explicitly tagged

## Version Management

Container versions are managed in the `VERSION.json` file at repository root. This file contains independent version numbers for each container type.

### VERSION.json Format
```json
{
  "gaia-linux": "0.15.3",
  "gaia-dev": "1.0.0"
}
```

- **gaia-linux**: Matches PyPI's `amd-gaia` package version
- **gaia-dev**: Independent versioning for development container features

### Updating Version
1. Edit `VERSION.json` file (e.g., change `"gaia-linux": "0.15.1"` to `"0.15.2"`)
2. Commit and push to main branch
3. CI automatically:
   - Reads VERSION.json using jq
   - Builds both containers with their respective GAIA_VERSION build args
   - Tags as `itomek/gaia-linux:<version>` and `itomek/gaia-dev:<version>`
   - Pushes to Docker Hub
   - Creates GitHub release

## CI/CD Pipeline

GitHub Actions workflow (.github/workflows/publish.yml):
1. **test** job: Runs pytest on all test files
2. **build-and-push** job: Builds and publishes gaia-linux
3. **build-dev** job: Builds and publishes gaia-dev
4. **update-description** job: Updates Docker Hub README
5. **create-release** job: Creates GitHub release with version tag

Integration tests only run on pushes to main (not PRs) to save CI time.

## Environment Variables

### gaia-linux
- `LEMONADE_BASE_URL` (required): Lemonade server API endpoint
- `GAIA_VERSION` (default: 0.15.3): PyPI version to install
- `SKIP_INSTALL` (default: false): Skip package installation for faster restarts

### gaia-dev
- `LEMONADE_BASE_URL` (required): Lemonade server API endpoint
- `GAIA_REPO_URL` (required): Git repository to clone
- `GITHUB_TOKEN` (required): Token for authenticated cloning and gh CLI
- `ANTHROPIC_API_KEY` (optional): Claude Code API key (fallback: interactive login)
- `SKIP_GAIA_CLONE` (default: false): Skip cloning GAIA repository

## Testing Strategy

- **Unit tests**: Test Dockerfile syntax and entrypoint script logic without building containers
- **Integration tests**: Build and run containers, verify GAIA installation and functionality
- pytest markers:
  - `@pytest.mark.integration` - Tests requiring actual container builds
- Use testcontainers library for container-based tests
- CI runs unit tests on all PRs, integration tests only on main branch pushes
