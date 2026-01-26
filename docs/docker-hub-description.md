# Docker Hub Image Description

Use this as the description when publishing the image to Docker Hub:

---

# GAIA Docker - Linux Container

GAIA Linux container for [AMD GAIA](https://github.com/amd/gaia). GAIA is installed from PyPI at startup.

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
docker run -dit --name gaia-dev itomek/gaia-dev:0.15.1
```

**Optional:** Set `LEMONADE_BASE_URL` environment variable if using a custom Lemonade server:
```bash
docker run -dit --name gaia-dev \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-dev:0.15.1
```

### 3. Access Container Terminal
```bash
docker exec -it gaia-dev zsh
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LEMONADE_BASE_URL` | `http://localhost:5000/api/v1` | Lemonade server base URL for GAIA LLM features |

### Example: Custom Lemonade URL

```bash
docker run -dit \
  --name gaia-dev \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-dev:0.15.1
```

## Usage

Once the container is running:

```bash
docker exec -it gaia-dev zsh
gaia --version
```

For the rest of GAIA usage, see https://github.com/AMD/GAIA

## Versioning

Images are tagged with the GAIA version they contain. We only publish specific version tags (no `latest` tag):
- `itomek/gaia-dev:0.15.1` - Current version (matches PyPI `amd-gaia==0.15.1`)
- `itomek/gaia-dev:0.15.2` - Future versions (when available)

The container installs GAIA from PyPI, so the version matches the `amd-gaia` package version. To use a different version, pull the specific tag or set the `GAIA_VERSION` environment variable.

## Features

- ✅ Complete isolation - GAIA installed from PyPI
- ✅ Fast installation with `uv` package manager
- ✅ Linux container for GAIA
- ✅ Ready to use out of the box
- ✅ Version-pinned to specific GAIA releases

## Documentation

Full documentation: https://github.com/itomek/gaia-docker

---
