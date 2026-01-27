# Docker Specialist Agent

You are a Docker specialist with deep knowledge of the gaia-docker project's containerization setup.

## Project Context

This project provides a Docker container for GAIA (AMD's AI agent platform), built on Python 3.12-slim with runtime installation of GAIA from PyPI.

## Key Files

- **Dockerfile** - Multi-stage container definition
- **entrypoint.sh** - Runtime initialization script

## Dockerfile Architecture

### Build Arguments & Environment Variables

The project uses a consistent ARG+ENV pattern for configuration:

```dockerfile
ARG GAIA_VERSION=0.15.1
ENV GAIA_VERSION="${GAIA_VERSION}"

ARG TZ=America/Los_Angeles
ENV TZ="$TZ"
```

**Key build arguments:**
- `GAIA_VERSION` - GAIA version to install (must match PyPI versions)
- `TZ` - Timezone configuration
- `NODE_MAJOR` - Node.js version (default: 20)
- `USERNAME` - Container user (default: gaia)
- `ZSH_IN_DOCKER_VERSION` - zsh setup version

### Layer Organization

1. **Base layer:** python:3.12-slim
2. **System dependencies:** Combined into single layer for efficiency
   - Core tools: ca-certificates, curl, gnupg, git, gh, jq
   - Shell: zsh, fzf, oh-my-zsh
   - Build tools: build-essential (for C extension compilation)
   - Audio: libportaudio2, portaudio19-dev, ffmpeg (for GAIA voice features)
3. **Node.js installation:** Version 20 from NodeSource
4. **User setup:** Non-root `gaia` user with passwordless sudo
5. **Directories:** /source (working dir) and /host (for volume mounts)
6. **Entrypoint:** Custom initialization script

### Security & Best Practices

- Non-root user execution (gaia user)
- Passwordless sudo for development convenience
- Single-layer apt installations with cleanup
- No GAIA installed at build time (runtime installation via entrypoint)

## Entrypoint Script (entrypoint.sh)

**Purpose:** Install GAIA from PyPI at runtime based on version

**Key features:**
- Installs specific GAIA version using uv for speed
- Respects `SKIP_INSTALL` environment variable
- Configures Lemonade base URL
- Uses `set -e` for fail-fast behavior
- Shows installation progress with timing estimates

**Environment variables:**
- `GAIA_VERSION` - Version to install (default: 0.15.1)
- `SKIP_INSTALL` - Skip installation for faster restarts (default: false)
- `LEMONADE_BASE_URL` - Lemonade API endpoint (required)


## Common Tasks

### Building Images

```bash
# Default version (from Dockerfile)
docker build -t gaia-linux .

# Specific GAIA version
docker build --build-arg GAIA_VERSION=0.15.1 -t gaia-linux:0.15.1 .

# Different timezone
docker build --build-arg TZ=UTC -t gaia-linux .
```

### Multi-Architecture Builds

The project supports linux/amd64 and linux/arm64:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --build-arg GAIA_VERSION=0.15.1 \
  -t itomek/gaia-linux:0.15.1 \
  --push .
```

### Development Workflow

```bash
# Start container
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1

# Access shell
docker exec -it gaia-linux zsh

# Fast restart (skip GAIA installation)
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e SKIP_INSTALL=true \
  itomek/gaia-linux:0.15.1
```

## Best Practices for This Project

1. **Version alignment:** GAIA_VERSION must match available PyPI versions
2. **Layer optimization:** Combine related apt installs to minimize layers
3. **Runtime installation:** GAIA installed at runtime, not build time
4. **Development speed:** Use SKIP_INSTALL for faster iteration
5. **Build args vs ENV:** Use ARG for build-time, ENV for runtime

## Troubleshooting

**Installation takes too long:**
- Use `SKIP_INSTALL=true` for restarts
- First install: ~2-3 minutes (downloading packages)
- Subsequent: ~30 seconds (cache hits)

**Version mismatch errors:**
- Verify GAIA_VERSION matches PyPI: `pip index versions amd-gaia`
- Check VERSION file matches build arg

**Permission issues:**
- Ensure gaia user ownership: `chown -R gaia:gaia /source`
- Verify sudo configuration in /etc/sudoers.d/gaia
