# Using This Image in Your Dockerfile

You can use the `gaia-linux` image as a base in your own Dockerfile to extend or customize it.

## Basic Usage

```dockerfile
FROM itomek/gaia-linux:0.15.3.1

# Your customizations here
RUN echo "Custom setup"

# The entrypoint will automatically install GAIA from PyPI at runtime
```

## How It Works

The `gaia-linux` image installs GAIA from PyPI at container startup (not build time). This means:
- First container start takes ~2-3 minutes for installation
- Subsequent starts with cached packages are faster (~30 seconds)
- The version is determined by the `GAIA_VERSION` environment variable

## Overriding GAIA Version

You can override the GAIA version by setting the `GAIA_VERSION` environment variable:

```dockerfile
FROM itomek/gaia-linux:0.15.3.1

# Override to use a different GAIA version
ENV GAIA_VERSION=0.15.2

# The entrypoint will install the specified version from PyPI
```

Or at runtime:
```bash
docker run -e GAIA_VERSION=0.15.2 itomek/gaia-linux:0.15.3.1
```

## Required Environment Variables

The container requires `LEMONADE_BASE_URL` to be set:

```dockerfile
FROM itomek/gaia-linux:0.15.3.1

# Required: Set Lemonade server URL
ENV LEMONADE_BASE_URL=https://your-server.com/api/v1

# Add your custom setup
RUN your-custom-commands
```

## Example: Custom Production Setup

```dockerfile
FROM itomek/gaia-linux:0.15.3.1

# Install additional tools
RUN apt-get update && \
    apt-get install -y your-tools && \
    apt-get clean

# Set up configuration
ENV LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1
ENV CUSTOM_VAR=value

# Copy your scripts
COPY scripts/ /usr/local/bin/

# The base image's entrypoint will handle GAIA installation from PyPI
```

## Building Your Custom Image

```bash
docker build -t my-gaia-app:latest .
docker run -d --name my-gaia-app my-gaia-app:latest
docker exec -it my-gaia-app zsh
```

## Skipping Installation

For faster restarts when GAIA is already installed (e.g., in a volume), set `SKIP_INSTALL=true`:

```bash
docker run -e SKIP_INSTALL=true -e LEMONADE_BASE_URL=... itomek/gaia-linux:0.15.3.1
```

## Notes

- The base image's entrypoint automatically installs GAIA from PyPI using `uv` (fast Python installer)
- GAIA version defaults to the image tag version, can be overridden via `GAIA_VERSION`
- All environment variables from the base image are available
- The container runs as user `gaia` with passwordless sudo

## Development Container

For development work (cloning GAIA from source, using Claude Code), use the `gaia-dev` image instead:

```bash
docker run -dit \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GITHUB_TOKEN=ghp_... \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  itomek/gaia-dev:1.0.0
```
