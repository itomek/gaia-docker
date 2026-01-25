# Using GAIA Docker from Docker Hub

This image is published on Docker Hub as `itomek/gaia-dev:<version>`.

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

**LEMONADE_URL is optional** - defaults to `http://localhost:5000/api/v1` if not provided.

```bash
# With default Lemonade URL (localhost:5000)
docker run -d \
  --name gaia-dev \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
  itomek/gaia-dev:0.15.1

# Or with custom Lemonade URL
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-lemonade-server.com/api/v1 \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
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
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-remote-server.com/api/v1 \
  itomek/gaia-dev:0.15.1
```

### Option 2: Local Lemonade Server (on Host)

If you're running Lemonade on your host machine:

**macOS:**
```bash
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=http://host.docker.internal:5000/api/v1 \
  itomek/gaia-dev:0.15.1
```

**Linux:**
```bash
# First, find your Docker gateway IP
docker network inspect bridge | grep Gateway

# Then use it (example):
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=http://172.17.0.1:5000/api/v1 \
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
      - LEMONADE_URL=https://your-lemonade-server.com/api/v1
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

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_URL` | No | `http://localhost:5000/api/v1` | Lemonade server URL |
| `GAIA_VERSION` | No | `0.15.1` | GAIA version to install from PyPI (matches image tag) |
| `SKIP_INSTALL` | No | `false` | Skip package installation on startup |

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

# Use GAIA LLM (requires LEMONADE_URL)
gaia llm "Hello, world!"

# Start GAIA chat
gaia chat

## Troubleshooting

### Container exits immediately

Check logs:
```bash
docker logs gaia-dev
```

The container should start successfully with default settings. If it exits, check the logs for specific error messages.

### GAIA says "Lemonade server is not running"

Verify `LEMONADE_URL` is set correctly:
```bash
docker exec gaia-dev env | grep LEMONADE_URL
```

Make sure the URL is accessible from inside the container.

### Port conflicts

Use different ports:
```bash
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-server.com/api/v1 \
  -p 5001:5000 \
  -p 8001:8000 \
  -p 3001:3000 \
  itomek/gaia-dev:0.15.1
```
