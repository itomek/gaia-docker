# GAIA Linux Container

Docker container for [AMD GAIA](https://github.com/amd/gaia) - Runtime edition.

**Current GAIA Version**: 0.15.3.2

## Overview

The `itomek/gaia-linux` container provides a ready-to-run AMD GAIA environment. GAIA is installed from PyPI at container startup, ensuring you always get a known version.

**Key Features:**
- GAIA installed from PyPI at startup
- Ubuntu 24.04 LTS with Python 3.12 + Node.js 20
- User `gaia` with passwordless sudo
- Fast installation with `uv` package manager (~2-3 minutes first run, ~30 seconds cached)
- No `latest` tag - all versions explicitly tagged

## Quick Start

### 1. Pull Image

```bash
docker pull itomek/gaia-linux:0.15.3.2
```

### 2. Run Container

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.3.2
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
| `GAIA_VERSION` | No | `0.15.3.2` | PyPI version to install (override image default) |
| `SKIP_INSTALL` | No | `false` | Skip package installation for faster restarts (use with care) |

## Architecture

The container follows this startup flow:

1. Base image: Ubuntu 24.04 LTS with Python 3.12 + Node.js 20
2. System dependencies: git, audio libraries, build tools
3. User `gaia` created with passwordless sudo
4. `uv` (fast Python package installer) installed globally
5. **At runtime** (entrypoint.sh):
   - Validates `LEMONADE_BASE_URL` is set
   - Installs `amd-gaia[dev,mcp,eval,rag]==<version>` from PyPI using uv
   - First run: ~2-3 minutes for download and installation
   - Subsequent runs: ~30 seconds (cached dependencies)

## Using as Base Image

You can extend this image in your own Dockerfile:

```dockerfile
FROM itomek/gaia-linux:0.15.3.2

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

Images are tagged with the GAIA version they install from PyPI:

- `itomek/gaia-linux:0.15.3.2` - Installs GAIA 0.15.3.2
- `itomek/gaia-linux:0.15.4` - Installs GAIA 0.15.4 (when released)
- etc.

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

### Version mismatch

To install a different GAIA version than the image default:

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_VERSION=0.15.2 \
  itomek/gaia-linux:0.15.3.2
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
