# GAIA Docker - Linux Container

GAIA Linux container for [AMD GAIA](https://github.com/amd/gaia). GAIA is installed from PyPI at startup.

**Current GAIA Version**: 0.15.1 (matches PyPI `amd-gaia` package)

## Features

- ✅ **Complete Isolation** - GAIA installed from PyPI inside container
- ✅ **Version Pinned** - Images tagged with GAIA version (currently 0.15.1)
- ✅ **Multi-Instance** - Spawn multiple containers from same image
- ✅ **Simple Access** - `docker exec` for instant terminal access
- ✅ **Fast Installation** - Uses `uv` for 10-100x faster Python package installation
- ✅ **Docker Hub Ready** - Published as `itomek/gaia-linux:<version>` for easy deployment

## Quick Start

### Prerequisites

- Docker installed
- Lemonade server base URL

### 1. Pull the Image

**Current version (GAIA 0.15.1):**
```bash
docker pull itomek/gaia-linux:0.15.1
```

**Other available versions:**
```bash
docker pull itomek/gaia-linux:0.15.2  # When available
```

**Note**: We only publish specific version tags (no `latest` tag). Images are tagged with the GAIA version they contain. The container installs GAIA from PyPI (`amd-gaia` package), so the version matches the PyPI package version.

### 2. Run the Container

Set the `LEMONADE_BASE_URL` environment variable to your Lemonade server:

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

You can set any environment variable using the `-e` flag. See the [Environment Variables](#environment-variables) section below for all available options.

### 3. Connect to Container

```bash
docker exec -it gaia-linux zsh
```

### 4. Start Using GAIA

```bash
gaia --version
```

For the rest of GAIA usage, see https://github.com/AMD/GAIA

## Environment Variables

You can configure the container using environment variables. Set them using the `-e` flag with `docker run`.

| Variable | Default | Description |
|----------|---------|-------------|
| `LEMONADE_BASE_URL` | **(required)** | Lemonade server base URL for GAIA LLM features. |
| `GAIA_VERSION` | `0.15.1` | GAIA version to install from PyPI. Usually matches the image tag, but can be overridden. |
| `SKIP_INSTALL` | `false` | Skip package installation on startup (faster restarts). |

### Setting Environment Variables

Use the `-e` flag with `docker run`:
```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

### Lemonade URL Examples

Start your Lemonade server separately, then set `LEMONADE_BASE_URL` to its API endpoint:

- **Local server**: `http://localhost:5000/api/v1`
- **Remote server**: `https://your-remote-server.com/api/v1`

### External Lemonade

If you want to use an external Lemonade, add this environment variable.

```bash
export LEMONADE_BASE_URL="https://your-server.com/api/v1"
source .cshrc
```

## Versioning

This Docker image is versioned to match the GAIA version from PyPI:

- **Current version**: 0.15.1 (matches PyPI `amd-gaia==0.15.1`)
- **Image tags**: `itomek/gaia-linux:0.15.1` (current version), `itomek/gaia-linux:0.15.2` (future versions when available)

**Note**: We only publish specific version tags (no `latest` tag). Each version is explicitly tagged.

### Pulling Specific Versions

```bash
# Current version
docker pull itomek/gaia-linux:0.15.1

# Future versions (when available)
docker pull itomek/gaia-linux:0.15.2
```

The container installs GAIA from PyPI, so the version in the container matches the image tag. You can override the version using the `GAIA_VERSION` environment variable.

## Using in Your Dockerfile

You can use this image as a base in your own Dockerfile. See [docs/dockerfile-usage.md](docs/dockerfile-usage.md) for detailed examples.

**Quick example:**
```dockerfile
FROM itomek/gaia-linux:0.15.1

# Add your customizations
ENV LEMONADE_BASE_URL=https://your-server.com/api/v1
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
docker build -t itomek/gaia-linux:0.15.1 .
```

### 3. Run the Container

Follow the same instructions as above, but use your locally built image.

## Usage

### Spawn Multiple Containers

```bash
# First container
docker run -dit \
  --name gaia-linux-main \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1

# Second container
docker run -dit \
  --name gaia-linux-feature \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

### Connect to Specific Container

```bash
docker exec -it gaia-linux-feature zsh
```

### Destroy and Recreate

```bash
# Stop and remove
docker stop gaia-linux-main && docker rm gaia-linux-main

# Recreate fresh
docker run -dit \
  --name gaia-linux-main \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

### Mount Host Directory for File Exchange

```bash
# Mount ~/Public to /host in container
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -v /Users/yourname/Public:/host \
  itomek/gaia-linux:0.15.1

# Inside container
ls /host
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Hub                               │
│                  itomek/gaia-linux:0.15.1                   │
│      (Python 3.12 + Node.js + tools)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ docker run
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Container Start                            │
│  1. entrypoint.sh runs                                      │
│  2. uv pip install "amd-gaia[dev,mcp,eval,rag]==<version>"  │
│  3. Ready                                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ docker exec -it gaia-linux zsh
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   GAIA Container                             │
│  - GAIA installed from PyPI                                 │
│  - Lemonade URL via env var                                 │
│  - Isolated Linux environment                               │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

Inside container:

```
/source/                # Working directory
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

- **First install**: ~2-3 minutes
- **Reinstall with cache**: ~30 seconds

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs gaia-linux
```

### GAIA Install Fails

```bash
# Check Python version
docker exec -it gaia-linux python --version  # Should be 3.12

# Manually install
docker exec -it gaia-linux bash -c "uv pip install --system 'amd-gaia[dev,mcp,eval,rag]==${GAIA_VERSION}'"
```

## Advanced Usage

### Build Image Locally

```bash
docker build -t gaia-linux:local .
```

### Push to Your Own Docker Hub

```bash
# Login
docker login

# Build and tag
docker build -t yourusername/gaia-linux:0.15.1 .

# Push
docker push yourusername/gaia-linux:0.15.1
```

## Development

See [dev.md](dev.md) for development setup, testing, and version management.

## License

MIT License - see [LICENSE](LICENSE) file

## Related Projects

- [AMD GAIA](https://github.com/amd/gaia) - Main GAIA framework

## Support

- **GAIA Issues**: https://github.com/amd/gaia/issues
- **Docker Issues**: https://github.com/itomek/gaia-docker/issues
