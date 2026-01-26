# Using GAIA Docker from Docker Hub

This image is published on Docker Hub as `itomek/gaia-dev:<version>`. This is a Linux container.

**Current GAIA Version**: 0.15.1 (matches PyPI `amd-gaia` package)

## Versioning

Images are tagged with the GAIA version they contain. We only publish specific version tags (no `latest` tag). The container installs GAIA from PyPI, so the version matches the `amd-gaia` package version.

- `itomek/gaia-dev:0.15.1` - Current version
- `itomek/gaia-dev:0.15.2` - Future versions (when available)

## Quick Start

### 1. Pull the Image

**Current version:**
```bash
docker pull itomek/gaia-dev:0.15.1
```

**Other versions:**
```bash
docker pull itomek/gaia-dev:0.15.2  # When available
```

### 2. Run the Container

**LEMONADE_BASE_URL is optional** - defaults to `http://localhost:5000/api/v1` if not provided.

```bash
# With default Lemonade URL (localhost:5000)
docker run -dit \
  --name gaia-dev \
  itomek/gaia-dev:0.15.1

# Or with custom Lemonade URL
docker run -dit \
  --name gaia-dev \
  -e LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1 \
  itomek/gaia-dev:0.15.1
```

### 3. Connect to Container

```bash
docker exec -it gaia-dev zsh
```

## Lemonade Server Options

### Option 1: Remote Lemonade Server

If you have a remote Lemonade server:

```bash
docker run -dit \
  --name gaia-dev \
  -e LEMONADE_BASE_URL=https://your-remote-server.com/api/v1 \
  itomek/gaia-dev:0.15.1
```

## Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gaia-dev:
    image: itomek/gaia-dev:0.15.1
    container_name: gaia-dev
    environment:
      - LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1
    tty: true
    stdin_open: true
```

Then run:

```bash
docker compose up -d
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | No | `http://localhost:5000/api/v1` | Lemonade server base URL |
| `GAIA_VERSION` | No | `0.15.1` | GAIA version to install from PyPI (matches image tag) |
| `SKIP_INSTALL` | No | `false` | Skip package installation on startup |

**Note**: `LEMONADE_URL` is accepted as a legacy alias and mapped to `LEMONADE_BASE_URL`.

## First Run

On first run, the container will:
1. Install GAIA version from PyPI (~2-3 minutes)
2. Install all dependencies
3. Be ready for use

Subsequent starts are much faster (~30 seconds) if `SKIP_INSTALL=true`.

**Note**: GAIA is installed from PyPI (`amd-gaia` package), not cloned from git. The version matches the Docker image tag.

## Usage

Once the container is running:

```bash
# Connect to container
docker exec -it gaia-dev zsh

# Test GAIA (already installed)
gaia --version
```

For the rest of GAIA usage, see https://github.com/AMD/GAIA

## Troubleshooting

### Container exits immediately

Check logs:
```bash
docker logs gaia-dev
```

The container should start successfully with default settings. If it exits, check the logs for specific error messages.

### GAIA says "Lemonade server is not running"

Verify `LEMONADE_BASE_URL` is set correctly (or `LEMONADE_URL` as a legacy alias):
```bash
docker exec gaia-dev env | grep LEMONADE_BASE_URL
```

Make sure the URL is accessible from inside the container.

