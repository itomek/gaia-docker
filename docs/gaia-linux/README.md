# GAIA Linux Container

Docker container for [AMD GAIA](https://github.com/amd/gaia) - Runtime edition.

**Current Image Version**: 1.0.0

## Overview

The `itomek/gaia-linux` container provides a ready-to-run AMD GAIA environment. GAIA is installed from PyPI at container startup — either the latest version or a specific version you choose.

**Key Features:**
- GAIA installed from PyPI at startup (latest or pinned version)
- Ubuntu 24.04 LTS with Python 3.12 + Node.js 20
- User `gaia` with passwordless sudo
- Fast installation with `uv` package manager (~2-3 minutes first run, ~30 seconds cached)
- No `latest` tag - all versions explicitly tagged

## Quick Start

### 1. Pull Image

```bash
docker pull itomek/gaia-linux:1.0.0
```

### 2. Run Container

```bash
# Installs latest GAIA from PyPI
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:1.0.0

# Or pin a specific GAIA version
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_VERSION=0.15.3.2 \
  itomek/gaia-linux:1.0.0
```

### 3. Connect

```bash
docker exec -it gaia-linux zsh
```

### 4. Use GAIA

```bash
gaia --version
```

For complete GAIA usage documentation, see [AMD GAIA](https://github.com/AMD/GAIA).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | Yes | - | Lemonade server API endpoint (e.g., `https://your-server.com/api/v1`) |
| `GAIA_VERSION` | No | *(latest)* | PyPI version to install. If omitted, installs latest from PyPI. |
| `SKIP_INSTALL` | No | `false` | Skip package installation for faster restarts (use with care) |

## Architecture

The container follows this startup flow:

1. Base image: Ubuntu 24.04 LTS with Python 3.12 + Node.js 20
2. System dependencies: git, audio libraries, build tools
3. User `gaia` created with passwordless sudo
4. `uv` (fast Python package installer) installed globally
5. **At runtime** (entrypoint.sh):
   - Validates `LEMONADE_BASE_URL` is set
   - If `GAIA_VERSION` is set: installs `amd-gaia[dev,mcp,eval,rag]==<version>` from PyPI
   - If `GAIA_VERSION` is not set: installs latest `amd-gaia[dev,mcp,eval,rag]` from PyPI
   - First run: ~2-3 minutes for download and installation
   - Subsequent runs: ~30 seconds (cached dependencies)

## Using as Base Image

You can extend this image in your own Dockerfile:

```dockerfile
FROM itomek/gaia-linux:1.0.0

# Install additional tools
RUN apt-get update && \
    apt-get install -y your-tools && \
    apt-get clean

# Set custom environment
ENV LEMONADE_BASE_URL=https://your-server.com/api/v1

# Add your customizations
COPY scripts/ /usr/local/bin/
```

For more examples, see [Dockerfile usage guide](../dockerfile-usage.md).

## Versioning

Image versions track the **base environment** (Ubuntu + Python + Node.js + system deps), not the GAIA PyPI package. A new GAIA release does not require a new Docker image — just set `GAIA_VERSION` at runtime:

```bash
# Use latest GAIA (default)
docker run -dit -e LEMONADE_BASE_URL=... itomek/gaia-linux:1.0.0

# Pin specific GAIA version
docker run -dit -e LEMONADE_BASE_URL=... -e GAIA_VERSION=0.16.0 itomek/gaia-linux:1.0.0
```

We do not publish a `latest` tag to ensure reproducibility.

## Troubleshooting

### Container fails to start

Check that `LEMONADE_BASE_URL` is set:

```bash
docker logs gaia-linux
```

You should see validation and installation progress.

### Slow installation

First run downloads all dependencies. Subsequent runs use Docker layer caching and are much faster. To skip installation entirely (if dependencies are already cached), set `SKIP_INSTALL=true`.

### Pin a specific GAIA version

If you need a specific GAIA version for compatibility, set it at runtime:

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_VERSION=0.15.3.1 \
  itomek/gaia-linux:1.0.0
```

## Support

- **GAIA Issues**: https://github.com/amd/gaia/issues
- **Docker Container Issues**: https://github.com/itomek/gaia-docker/issues
- **Full Documentation**: https://github.com/itomek/gaia-docker

## Related Containers

- **[gaia-dev](../gaia-dev/README.md)** - Development container with Claude Code and GAIA source code
- **[gaia-windows](../gaia-windows/README.md)** - Windows container (planned)

## License

MIT License - see [LICENSE](../../LICENSE) file
