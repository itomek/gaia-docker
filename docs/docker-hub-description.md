# Docker Hub Image Description

Use this as the description when publishing the image to Docker Hub:

---

# GAIA Docker - Isolated Development Container

Fully isolated Docker container for [AMD GAIA](https://github.com/amd/gaia) development with all dependencies pre-installed.

**GAIA Version**: 0.15.1 (matches PyPI `amd-gaia` package)

## Quick Start

### 1. Pull the Image

**Current version (0.15.1):**
```bash
docker pull itomek/gaia-dev:0.15.1
```

**Other available versions:**
```bash
docker pull itomek/gaia-dev:0.15.2  # When available
```

### 2. Run the Container
```bash
docker run -d --name gaia-dev -p 5000:5000 -p 8000:8000 -p 3000:3000 itomek/gaia-dev:0.15.1
```

**Optional:** Set `LEMONADE_URL` environment variable if using a custom Lemonade server:
```bash
docker run -d --name gaia-dev \
  -e LEMONADE_URL=https://your-server.com/api/v1 \
  -p 5000:5000 -p 8000:8000 -p 3000:3000 \
  itomek/gaia-dev:0.15.1
```

### 3. Access Container Terminal
```bash
docker exec -it gaia-dev zsh
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LEMONADE_URL` | `http://localhost:5000/api/v1` | Lemonade server URL for GAIA LLM features |

### Example: Custom Lemonade URL

```bash
docker run -d \
  --name gaia-dev \
  -e LEMONADE_URL=https://your-server.com/api/v1 \
  -p 5000:5000 \
  -p 8000:8000 \
  -p 3000:3000 \
  itomek/gaia-dev:0.15.1
```

## Usage

Once the container is running:

```bash
docker exec -it gaia-dev zsh
cd /source/gaia
gaia --version
gaia llm "Hello, world!"
```

## Versioning

Images are tagged with the GAIA version they contain. We only publish specific version tags (no `latest` tag):
- `itomek/gaia-dev:0.15.1` - Current version (matches PyPI `amd-gaia==0.15.1`)
- `itomek/gaia-dev:0.15.2` - Future versions (when available)

The container installs GAIA from PyPI, so the version matches the `amd-gaia` package version. To use a different version, pull the specific tag or set the `GAIA_VERSION` environment variable.

## Features

- ✅ Complete isolation - GAIA installed from PyPI
- ✅ Fast installation with `uv` package manager
- ✅ Pre-configured with Claude Code and Cursor support
- ✅ Ready to use out of the box
- ✅ Version-pinned to specific GAIA releases

## Documentation

Full documentation: https://github.com/itomek/gaia-docker

---
