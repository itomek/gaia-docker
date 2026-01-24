# GAIA Docker - Isolated Development Container

Fully isolated Docker container for [AMD GAIA](https://github.com/amd/gaia) development with Claude Code support.

## Features

- ✅ **Complete Isolation** - GAIA cloned inside container, not bind-mounted
- ✅ **YOLO Mode Safe** - Destroy and recreate containers freely
- ✅ **AI IDE Ready** - Configured for Claude Code and Cursor
- ✅ **Multi-Instance** - Spawn multiple containers from same image
- ✅ **Zero Security** - Optimized for development speed, not production
- ✅ **Simple Access** - `docker exec` for instant terminal access
- ✅ **Fast Installation** - Uses `uv` for 10-100x faster Python package installation

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- GitHub personal access token (for cloning GAIA)
- (Optional) Claude Code or Cursor for AI-assisted development

### 1. Clone This Repository

```bash
git clone https://github.com/itomek/gaia-docker.git
cd gaia-docker
```

### 2. Set GitHub Token

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### 3. Start Container

```bash
docker compose up -d
```

First startup takes ~2-3 minutes (downloads image, clones GAIA, installs dependencies with uv).

### 4. Connect to Container

```bash
docker exec -it gaia-dev zsh
```

### 5. Using AI IDEs (Optional)

#### Claude Code

```bash
claude
# Follow OAuth login in browser
# Credentials persist in Docker volume
```

#### Cursor

The project includes `.cursorrules` for Cursor AI configuration. Simply open the project in Cursor to use AI features with project-specific context.

### 6. Start Using GAIA

```bash
cd /source/gaia

# Test LLM (requires Lemonade server)
gaia llm "Hello"

# Start chat
gaia chat

# Use Claude Code
claude -p "Show me the GAIA architecture"
```

## Usage

### Spawn Multiple Containers

```bash
# Default container
docker compose up -d

# Second container (different name/ports)
CONTAINER_NAME=gaia-feature \
LEMONADE_PORT=5001 \
GAIA_API_PORT=8001 \
GAIA_BRANCH=feature/new-agent \
  docker compose up -d

# Third container (your fork)
CONTAINER_NAME=gaia-myfork \
LEMONADE_PORT=5002 \
GAIA_API_PORT=8002 \
GAIA_REPO=https://github.com/yourname/gaia.git \
  docker compose up -d
```

### Connect to Specific Container

```bash
docker exec -it gaia-feature zsh
```

### Destroy and Recreate (YOLO Reset)

```bash
# Stop and remove
docker compose down

# Recreate fresh (fast with uv: ~2-3 minutes)
docker compose up -d
```

### Mount Host Directory for File Exchange

```bash
# Mount ~/Public to /host in container
HOST_DIR=/Users/yourname/Public docker compose up -d

# Inside container
ls /host
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | **Yes** | - | GitHub PAT for cloning GAIA |
| `GAIA_BRANCH` | No | `main` | Branch to clone |
| `GAIA_REPO` | No | `https://github.com/amd/gaia.git` | Repository URL |
| `CONTAINER_NAME` | No | `gaia-dev` | Container name |
| `LEMONADE_PORT` | No | `5000` | Lemonade server port |
| `GAIA_API_PORT` | No | `8000` | GAIA API port |
| `WEB_PORT` | No | `3000` | Web app port |
| `HOST_DIR` | No | - | Host directory to mount at `/host` |
| `SKIP_INSTALL` | No | `false` | Skip `pip install` on startup |
| `LEMONADE_URL` | No | - | Remote Lemonade server URL |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Hub                               │
│                  itomek/gaia-dev:latest                     │
│      (Python 3.12 + Node.js + tools + Claude Code)          │
│      Configured for: Claude Code, Cursor                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ docker compose up
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Container Start                            │
│  1. entrypoint.sh runs                                      │
│  2. git clone gaia (configurable branch)                    │
│  3. uv pip install -e ".[dev,mcp,eval,rag]" (fast!)        │
│  4. Ready for development                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ docker exec -it gaia-dev zsh
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Development                                │
│  - Claude Code with OAuth credentials                       │
│  - Git with GITHUB_TOKEN                                    │
│  - Full GAIA environment                                    │
│  - YOLO mode safe (container is disposable)                 │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

Inside container:

```
/source/gaia/           # GAIA repository (cloned at runtime)
/home/gaia/.claude/     # Claude Code config (persisted in volume)
/host/                  # Optional host directory mount
```

In workspace root:

```
.cursor/
  rules/
    index.mdc          # Main project rules (always applied)
    testing.mdc        # Testing-specific rules (auto-applied to test files)
    docker.mdc         # Docker/container rules (auto-applied to Docker files)
    python.mdc         # Python development rules (auto-applied to .py files)
.cursorignore          # Files to exclude from Cursor analysis
```

## Development Workflow

### Typical Session

```bash
# Start container
docker compose up -d

# Connect
docker exec -it gaia-dev zsh

# Work with GAIA
cd /source/gaia
git checkout -b my-feature
# ... make changes ...
git commit -am "Add feature"

# Test with Claude Code
claude
# ... interactive session ...

# When done, exit
exit

# Stop container (keeps volumes)
docker compose stop

# Or destroy completely
docker compose down
```

### Update GAIA Source

```bash
# Restart container to pull latest
docker compose restart

# Or manually inside container
cd /source/gaia
git pull origin main
pip install -e ".[dev]"
```

### Fast Restarts (Skip Install)

```bash
# Skip pip install on restart (faster)
SKIP_INSTALL=true docker compose up -d
```

## Testing

### Run Tests Locally

```bash
# Install test dependencies
uv sync

# Run all tests
uv run pytest tests/ -v

# Run specific test suite
uv run pytest tests/test_dockerfile.py -v
uv run pytest tests/test_entrypoint.py -v
uv run pytest tests/test_container.py -v -m integration
```

### Run Tests in CI

Tests run automatically on pull requests via GitHub Actions.

## Performance

The container uses **uv** for Python package installation, which is 10-100x faster than pip:

- **First install**: ~2-3 minutes (including git clone)
- **Reinstall with cache**: ~30 seconds
- **YOLO reset**: ~2-3 minutes (fresh clone + install)

This makes the YOLO workflow practical for daily use.

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs

# Check if GITHUB_TOKEN is set
echo $GITHUB_TOKEN
```

### Claude Code Not Working

```bash
# Re-login to Claude
docker exec -it gaia-dev claude

# Check config persists
docker exec -it gaia-dev ls -la /home/gaia/.claude
```

### GAIA Install Fails

```bash
# Check Python version
docker exec -it gaia-dev python --version  # Should be 3.12

# Manually install
docker exec -it gaia-dev bash -c "cd /source/gaia && pip install -e '.[dev]'"
```

### Port Conflicts

```bash
# Use different ports
LEMONADE_PORT=5001 GAIA_API_PORT=8001 docker compose up -d
```

## Advanced Usage

### Connect to Remote Lemonade Server

```bash
# Set Lemonade URL
LEMONADE_URL=http://your-server:5000 docker compose up -d

# Inside container
export LEMONADE_URL=http://your-server:5000
gaia llm "Hello"
```

### Build Image Locally

```bash
# Build from Dockerfile
docker compose build

# Or with docker directly
docker build -t gaia-dev:local .
```

### Push to Your Own Docker Hub

```bash
# Login
docker login

# Build and tag
docker build -t yourusername/gaia-dev:latest .

# Push
docker push yourusername/gaia-dev:latest
```

## Contributing

Contributions welcome! Please:

1. Fork this repository
2. Create a feature branch
3. Run tests: `pytest tests/ -v`
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file

## AI IDE Configuration

### Cursor

This project uses the modern `.cursor/rules/` structure with multiple `.mdc` files:

- **`index.mdc`**: Main project rules (always applied) - project overview, architecture, environment variables
- **`testing.mdc`**: Auto-applies to test files - pytest guidelines, test commands
- **`docker.mdc`**: Auto-applies to Docker files - container best practices, image architecture
- **`python.mdc`**: Auto-applies to Python files - uv usage, dependency management, code style

The `.cursorignore` file excludes unnecessary files from AI analysis (git objects, cache, etc.).

**Note**: The old `.cursorrules` single-file format is deprecated in favor of the modular `.cursor/rules/*.mdc` approach.

### Claude Code

Claude Code is pre-installed in the Docker container. OAuth credentials persist in the Docker volume at `/home/gaia/.claude/`.

## Related Projects

- [AMD GAIA](https://github.com/amd/gaia) - Main GAIA framework
- [Claude Code](https://claude.ai/code) - Anthropic's CLI tool
- [Cursor](https://cursor.sh) - AI-powered code editor

## Support

- **GAIA Issues**: https://github.com/amd/gaia/issues
- **Docker Issues**: https://github.com/itomek/gaia-docker/issues
- **Claude Code Help**: https://claude.ai/help
