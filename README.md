# GAIA Docker - Isolated Development Container

Fully isolated Docker container for [AMD GAIA](https://github.com/amd/gaia) development with Claude Code support.

**Current GAIA Version**: 0.15.1 (matches PyPI `amd-gaia` package)

## Features

- ✅ **Complete Isolation** - GAIA installed from PyPI inside container
- ✅ **Version Pinned** - Images tagged with GAIA version (currently 0.15.1)
- ✅ **YOLO Mode Safe** - Destroy and recreate containers freely
- ✅ **AI IDE Ready** - Configured for Claude Code and Cursor
- ✅ **Multi-Instance** - Spawn multiple containers from same image
- ✅ **Zero Security** - Optimized for development speed, not production
- ✅ **Simple Access** - `docker exec` for instant terminal access
- ✅ **Fast Installation** - Uses `uv` for 10-100x faster Python package installation
- ✅ **Docker Hub Ready** - Published as `itomek/gaia-dev:<version>` for easy deployment

## Quick Start

### Prerequisites

- Docker installed
- (Optional) Lemonade server URL (defaults to `http://localhost:5000/api/v1`)

### 1. Pull the Image

**Current version (GAIA 0.15.1):**
```bash
docker pull itomek/gaia-dev:0.15.1
```

**Other available versions:**
```bash
docker pull itomek/gaia-dev:0.15.2  # When available
```

**Note**: We only publish specific version tags (no `latest` tag). Images are tagged with the GAIA version they contain. The container installs GAIA from PyPI (`amd-gaia` package), so the version matches the PyPI package version.

### 2. Run the Container

**Option A: Using Default Settings**

The container works out of the box with default settings (LEMONADE_URL defaults to `http://localhost:5000/api/v1`):

```bash
docker run -d \
  --name gaia-dev \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
  itomek/gaia-dev:0.15.1
```

**Option B: With Custom Lemonade URL**

If you need to use a different Lemonade server, set the `LEMONADE_URL` environment variable using the `-e` flag:

```bash
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-lemonade-server.com/api/v1 \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
  itomek/gaia-dev:0.15.1
```

**Note**: You can set any environment variable using the `-e` flag. See the [Environment Variables](#environment-variables) section below for all available options.

**Option C: Using Docker Compose**

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gaia-dev:
    image: itomek/gaia-dev:0.15.1
    container_name: gaia-dev
    environment:
      - LEMONADE_URL=http://localhost:5000/api/v1  # Optional, this is the default
    ports:
      - "5000:5000"
      - "8000:8000"
      - "3000:3000"
    volumes:
      - gaia-claude-config:/home/gaia/.claude
    tty: true
    stdin_open: true

volumes:
  gaia-claude-config:
```

Then run:

```bash
docker compose up -d
```

### 3. Connect to Container

```bash
docker exec -it gaia-dev zsh
```

### 4. Start Using GAIA

```bash
# Test GAIA (already installed from PyPI)
gaia --version

# Use GAIA LLM (requires Lemonade server)
gaia llm "Hello, world!"

# Start GAIA chat
gaia chat
```

## Environment Variables

You can configure the container using environment variables. Set them using the `-e` flag with `docker run` or in your `docker-compose.yml`.

| Variable | Default | Description |
|----------|---------|-------------|
| `LEMONADE_URL` | `http://localhost:5000/api/v1` | Lemonade server URL for GAIA LLM features. Set this if your Lemonade server is running on a different host or port. |
| `GAIA_VERSION` | `0.15.1` | GAIA version to install from PyPI. Usually matches the image tag, but can be overridden. |
| `SKIP_INSTALL` | `false` | Skip package installation on startup (faster restarts). |

### Setting Environment Variables

**With docker run:**
```bash
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-server.com/api/v1 \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
  itomek/gaia-dev:0.15.1
```

**With docker-compose.yml:**
```yaml
services:
  gaia-dev:
    image: itomek/gaia-dev:0.15.1
    environment:
      - LEMONADE_URL=https://your-server.com/api/v1
    ports:
      - "5000:5000"
      - "8000:8000"
      - "3000:3000"
```

**Using .env file with docker-compose:**
```bash
# Create .env file
echo "LEMONADE_URL=https://your-server.com/api/v1" > .env

# docker-compose automatically reads .env
docker compose up -d
```

### Lemonade URL Examples

- **Default (Lemonade in container)**: `http://localhost:5000/api/v1`
- **Remote server**: `https://your-remote-server.com/api/v1`
- **Local server on host (macOS)**: `http://host.docker.internal:5000/api/v1`
- **Local server on host (Linux)**: `http://172.17.0.1:5000/api/v1`

## Versioning

This Docker image is versioned to match the GAIA version from PyPI:

- **Current version**: 0.15.1 (matches PyPI `amd-gaia==0.15.1`)
- **Image tags**: `itomek/gaia-dev:0.15.1` (current version), `itomek/gaia-dev:0.15.2` (future versions when available)

**Note**: We only publish specific version tags (no `latest` tag). Each version is explicitly tagged.

### Pulling Specific Versions

```bash
# Current version
docker pull itomek/gaia-dev:0.15.1

# Future versions (when available)
docker pull itomek/gaia-dev:0.15.2
```

The container installs GAIA from PyPI, so the version in the container matches the image tag. You can override the version using the `GAIA_VERSION` environment variable.

## Using in Your Dockerfile

You can use this image as a base in your own Dockerfile. See [docs/dockerfile-usage.md](docs/dockerfile-usage.md) for detailed examples.

**Quick example:**
```dockerfile
FROM itomek/gaia-dev:0.15.1

# Add your customizations
ENV LEMONADE_URL=https://your-server.com/api/v1
RUN your-custom-commands
```

## Building from Source

If you want to build the image yourself or modify it:

### 1. Clone This Repository

```bash
git clone https://github.com/itomek/gaia-docker.git
cd gaia-docker
```

### 2. Build the Image

```bash
docker build -t itomek/gaia-dev:0.15.1 .
```

### 3. Run the Container

Follow the same instructions as above, but use your locally built image.

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

Environment variables can be set in three ways (in order of precedence):
1. **`.env` file** (recommended) - Project-specific, gitignored, see `.env.example`
2. **OS environment variables** - `export VAR=value`
3. **Inline** - `VAR=value docker compose up`

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_URL` | No | `http://localhost:5000/api/v1` | Lemonade server URL |
| `GAIA_BRANCH` | No | `main` | Branch to clone |
| `GAIA_REPO` | No | `https://github.com/amd/gaia.git` | Repository URL |
| `CONTAINER_NAME` | No | `gaia-dev` | Container name |
| `LEMONADE_PORT` | No | `5000` | Lemonade server port |
| `GAIA_API_PORT` | No | `8000` | GAIA API port |
| `WEB_PORT` | No | `3000` | Web app port |
| `HOST_DIR` | No | - | Host directory to mount at `/host` |
| `SKIP_INSTALL` | No | `false` | Skip `pip install` on startup |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Hub                               │
│                  itomek/gaia-dev:0.15.1                     │
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
│  - Git (public repos, no token needed)                      │
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
# Restart container
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

# Check container logs
docker compose logs
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

### Configure Lemonade Server (Optional)

**LEMONADE_URL defaults to `http://localhost:5000/api/v1`** - you only need to set it if using a different Lemonade server.

**Option 1: Set in .env file (Recommended for local development)**

```bash
# Edit .env and set:
LEMONADE_URL=https://your-server.com/api/v1
```

**Option 2: Remote Lemonade Server**

```bash
# Set as environment variable
LEMONADE_URL=https://your-remote-server.com/api/v1 docker compose up -d
```

**Option 3: Local Lemonade Server (on host machine)**

If running Lemonade on your host machine:

```bash
# macOS - add to .env:
LEMONADE_URL=http://host.docker.internal:5000/api/v1

# Linux - get your Docker gateway IP first:
docker network inspect bridge | grep Gateway
# Then add to .env:
LEMONADE_URL=http://172.17.0.1:5000/api/v1
```

**For Docker Hub users**: Pass `LEMONADE_URL` as an environment variable when running the container. See [docker-hub.md](docs/docker-hub.md) for details.

**Note**: The interactive `./setup.sh` script can help you configure this automatically for local development.

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
docker build -t yourusername/gaia-dev:0.15.1 .

# Push
docker push yourusername/gaia-dev:0.15.1
```

## Development

See [dev.md](dev.md) for development setup, testing, and version management.

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
