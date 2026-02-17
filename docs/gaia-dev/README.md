# GAIA Dev Container

Docker container for [AMD GAIA](https://github.com/amd/gaia) - Development edition with Claude Code.

**Current Container Version**: 1.2.0

## Overview

The `itomek/gaia-dev` container provides a complete AMD GAIA development environment with Claude Code integration. GAIA is cloned from source and installed in editable mode, making it perfect for development and contributions.

**Key Features:**
- GAIA cloned from source and installed in editable mode
- Claude Code CLI pre-installed for AI-assisted development
- Ubuntu 24.04 LTS with Python 3.12 + Node.js 20
- Network isolation packages for sandboxing
- User `gaia` with passwordless sudo
- Fast installation with `uv` package manager
- GitHub CLI (gh) configured with your token
- No `latest` tag - all versions explicitly tagged

## Quick Start

### 1. Pull Image

```bash
docker pull itomek/gaia-dev:1.2.0
```

### 2. Run Container

```bash
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_REPO_URL=https://github.com/amd/gaia.git \
  -e GITHUB_TOKEN=ghp_your_token \
  -e ANTHROPIC_API_KEY=sk-ant-your_key \
  itomek/gaia-dev:1.2.0
```

**Note**: Using a named volume (`gaia-src:/home/gaia/gaia`) persists the GAIA source code between container restarts, avoiding re-cloning.

### 3. Connect

```bash
docker exec -it gaia-dev zsh
```

### 4. Use GAIA and Claude Code

```bash
# Check GAIA installation
gaia --version

# Start Claude Code for AI-assisted development
claude

# Work with GAIA source
cd ~/gaia
git status
```

For complete GAIA usage documentation, see [AMD GAIA](https://github.com/AMD/GAIA).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | Yes | - | Lemonade server API endpoint (e.g., `https://your-server.com/api/v1`) |
| `GAIA_REPO_URL` | Yes | - | Git repository URL to clone (e.g., `https://github.com/amd/gaia.git`) |
| `GITHUB_TOKEN` | Yes | - | GitHub token for authenticated cloning and gh CLI configuration |
| `ANTHROPIC_API_KEY` | No | - | Claude Code API key (if not provided, uses interactive login) |
| `SKIP_GAIA_CLONE` | No | `false` | Skip cloning GAIA repository (use if volume already contains source) |

## Architecture

The container follows this startup flow:

1. Base image: Ubuntu 24.04 LTS with uv-managed Python 3.12 + Node.js 20
2. System dependencies: git, gh CLI, jq, audio libraries, build tools, network isolation tools
3. User `gaia` created with passwordless sudo
4. `uv` (fast Python package installer) installed globally
5. Claude Code CLI installed via native installer (user-owned, auto-updates enabled)
6. **At runtime** (entrypoint.sh):
   - Validates `LEMONADE_BASE_URL` is set
   - Clones GAIA from `GAIA_REPO_URL` (if not present in volume)
   - Installs GAIA in editable mode with `uv pip install -e .`
   - Configures GitHub CLI if `GITHUB_TOKEN` provided
   - Sets up `ANTHROPIC_API_KEY` for Claude Code

## Development Workflow

### Making Changes to GAIA

Since GAIA is installed in editable mode, changes are immediately reflected:

```bash
# Enter container
docker exec -it gaia-dev zsh

# Navigate to GAIA source
cd ~/gaia

# Make changes
vim src/gaia/some_file.py

# Test immediately (no reinstall needed)
gaia --help
```

### Using Claude Code

Claude Code is pre-installed and ready to use:

```bash
# Start Claude Code
claude

# Claude can help you:
# - Understand the GAIA codebase
# - Write new features
# - Debug issues
# - Write tests
# - Improve documentation
```

### Working with Git

GitHub CLI is configured with your token:

```bash
# Check git status
git status

# Create a branch
git checkout -b feature/my-change

# Use gh CLI
gh pr create
gh issue list
```

## Using as Base Image

You can extend this image for your own development environment:

```dockerfile
FROM itomek/gaia-dev:1.2.0

# Install additional development tools
RUN apt-get update && \
    apt-get install -y vim emacs tmux && \
    apt-get clean

# Install additional Python packages
RUN uv pip install --system debugpy ipdb

# Add custom configurations
COPY .vimrc /home/gaia/
COPY .tmux.conf /home/gaia/

USER gaia
```

For more examples, see [Dockerfile usage guide](../dockerfile-usage.md).

## Versioning

The gaia-dev container uses independent versioning from the GAIA package:

- Container versions (e.g., `itomek/gaia-dev:1.2.0`) indicate development environment features
- The actual GAIA version installed depends on what you clone from `GAIA_REPO_URL`
- All versions are explicitly tagged (no `latest` tag for reproducibility)

Version history:
- `1.2.0` - Native Claude Code installer (user-owned, auto-updates enabled), DEVCONTAINER env
- `1.1.0` - Migrated to Ubuntu 24.04 LTS base image, uv-managed Python
- `1.0.0` - Development container with Claude Code, virtual environment, and editable GAIA install

## Volume Persistence

Using a named volume for the GAIA source code is recommended:

```bash
# First run - clones GAIA
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_REPO_URL=https://github.com/amd/gaia.git \
  -e GITHUB_TOKEN=ghp_your_token \
  itomek/gaia-dev:1.2.0

# Stop and remove container
docker stop gaia-dev && docker rm gaia-dev

# Restart with same volume - GAIA source persists
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_REPO_URL=https://github.com/amd/gaia.git \
  -e GITHUB_TOKEN=ghp_your_token \
  -e SKIP_GAIA_CLONE=true \
  itomek/gaia-dev:1.2.0
```

## Troubleshooting

### Container fails to start

Check that required environment variables are set:

```bash
docker logs gaia-dev
```

You should see validation and clone/installation progress.

### Claude Code authentication

If `ANTHROPIC_API_KEY` is not provided, Claude Code will prompt for interactive login on first use:

```bash
docker exec -it gaia-dev claude
# Follow prompts to authenticate
```

### Repository already cloned

If the volume already contains GAIA source, set `SKIP_GAIA_CLONE=true` to skip cloning:

```bash
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e SKIP_GAIA_CLONE=true \
  itomek/gaia-dev:1.2.0
```

## Support

- **GAIA Issues**: https://github.com/amd/gaia/issues
- **Docker Container Issues**: https://github.com/itomek/gaia-docker/issues
- **Claude Code Documentation**: https://claude.ai/code
- **Full Documentation**: https://github.com/itomek/gaia-docker

## Related Containers

- **[gaia-linux](../gaia-linux/README.md)** - Runtime container with GAIA from PyPI
- **[gaia-windows](../gaia-windows/README.md)** - Windows container (planned)

## License

MIT License - see [LICENSE](../../LICENSE) file
