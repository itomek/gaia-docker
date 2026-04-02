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

VERSION.json           # Single source of truth for Docker image versions
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
# Build gaia-linux (version from VERSION.json)
docker build -f gaia-linux/Dockerfile -t itomek/gaia-linux:$(jq -r '."gaia-linux"' VERSION.json) .

# Build gaia-dev (version from VERSION.json)
docker build -f gaia-dev/Dockerfile -t itomek/gaia-dev:$(jq -r '."gaia-dev"' VERSION.json) .
```

### Running Containers Locally

```bash
# gaia-linux — installs latest GAIA from PyPI
docker run -dit \
  --name gaia-linux-test \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:$(jq -r '."gaia-linux"' VERSION.json)

# gaia-linux — pin specific GAIA version
docker run -dit \
  --name gaia-linux-test \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_VERSION=0.15.3.2 \
  itomek/gaia-linux:$(jq -r '."gaia-linux"' VERSION.json)

# gaia-dev
docker run -dit \
  --name gaia-dev-test \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GITHUB_TOKEN=ghp_... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  itomek/gaia-dev:$(jq -r '."gaia-dev"' VERSION.json)

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
   - If `GAIA_VERSION` is set: installs `amd-gaia[dev,mcp,eval,rag]==<version>` from PyPI
   - If `GAIA_VERSION` is not set: installs latest `amd-gaia[dev,mcp,eval,rag]` from PyPI
   - First run: ~2-3 minutes, cached runs: ~30 seconds

### gaia-dev Container Flow
1. Base: Ubuntu 24.04 LTS with uv-managed Python 3.12 and Node.js 20
   - Claude Code installed via native installer (user-owned, auto-updates enabled)
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
- VERSION.json is single source of truth for **Docker image versions** (independent from GAIA PyPI versions)
- Docker image versioning is decoupled from GAIA versioning — GAIA version is chosen at runtime
- No `latest` tag - all versions explicitly tagged

## Version Management

VERSION.json contains **Docker image versions only**. These versions track the base environment (Ubuntu + Python + Node.js + system deps), not the GAIA PyPI package.

### VERSION.json Format
```json
{
  "gaia-linux": "1.0.0",
  "gaia-dev": "1.2.0"
}
```

- **gaia-linux**: Docker image version (base environment). Bump when Dockerfile changes.
- **gaia-dev**: Docker image version (base environment + dev tools). Bump when Dockerfile changes.

GAIA version is specified at container runtime via `GAIA_VERSION` env var (or omitted for latest).

### Updating Version
1. Edit `VERSION.json` file — only bump when the Docker image itself changes
2. Commit and push to main branch
3. CI automatically:
   - Reads VERSION.json using jq
   - Skips build if the image tag already exists on Docker Hub
   - Builds and tags as `itomek/gaia-linux:<version>` and `itomek/gaia-dev:<version>`
   - Pushes to Docker Hub
   - Creates GitHub release

## CI/CD Pipeline

GitHub Actions workflow (.github/workflows/publish.yml):
1. **test** job: Runs pytest on all test files
2. **build-and-push** job: Builds and publishes gaia-linux (skips if tag exists)
3. **build-dev** job: Builds and publishes gaia-dev
4. **update-description** job: Updates Docker Hub README
5. **create-release** job: Creates GitHub release with version tag

Integration tests only run on pushes to main (not PRs) to save CI time.

## Environment Variables

### gaia-linux
- `LEMONADE_BASE_URL` (required): Lemonade server API endpoint
- `GAIA_VERSION` (optional): PyPI version to install. If omitted, installs latest from PyPI.
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
