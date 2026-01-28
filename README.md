# GAIA Docker

Docker containers for [AMD GAIA](https://github.com/amd/gaia) - the AI framework for building and deploying intelligent agents.

**Current GAIA Version**: 0.15.1

## Overview

This project provides production-ready Docker containers for AMD GAIA in multiple variants, each optimized for different use cases.

## Available Containers

| Container | Use Case | Installation Method | Documentation |
|-----------|----------|---------------------|---------------|
| **gaia-linux** | Production runtime | PyPI at startup | [View Docs](docs/gaia-linux/README.md) |
| **gaia-dev** | Development + Claude Code | Cloned from source | [View Docs](docs/gaia-dev/README.md) |
| **gaia-windows** | Windows environments | Planned | [View Docs](docs/gaia-windows/README.md) |

## Quick Start

Choose the container that matches your needs:

### For Production Use

Use `gaia-linux` for running GAIA applications:

```bash
docker pull itomek/gaia-linux:0.15.1
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

See [gaia-linux documentation](docs/gaia-linux/README.md) for complete usage.

### For Development

Use `gaia-dev` for developing GAIA or contributing to the project:

```bash
docker pull itomek/gaia-dev:0.15.1
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GAIA_REPO_URL=https://github.com/amd/gaia.git \
  -e GITHUB_TOKEN=ghp_your_token \
  itomek/gaia-dev:0.15.1
```

See [gaia-dev documentation](docs/gaia-dev/README.md) for complete usage.

## Key Features

- **Version-pinned**: All images tagged with specific GAIA versions (no `latest` tag)
- **Fast installation**: Uses `uv` package manager for 10-100x faster installs than pip
- **Complete isolation**: Each container is fully self-contained
- **Multi-instance support**: Run multiple GAIA instances on the same host
- **Production-ready**: Built on official Python images with security best practices

## Container Comparison

### gaia-linux
- **Best for**: Running GAIA applications, production deployments
- **GAIA source**: Installed from PyPI at startup
- **Includes**: Python 3.12, Node.js 20, system dependencies
- **Size**: Smaller (~1-2 GB)
- **Startup**: 2-3 minutes first run, 30 seconds cached

### gaia-dev
- **Best for**: GAIA development, contributions, experimentation
- **GAIA source**: Cloned from GitHub, editable install
- **Includes**: Everything in gaia-linux + Claude Code, network isolation tools
- **Size**: Larger (~2-3 GB)
- **Startup**: 3-5 minutes first run, 1 minute cached

### gaia-windows (Planned)
- **Best for**: Windows-specific workflows
- **Status**: Future feature, in planning phase
- **Alternative**: Use gaia-linux or gaia-dev with Docker Desktop on Windows

## Documentation

### Container-Specific Docs
- [gaia-linux Documentation](docs/gaia-linux/README.md) - Runtime container guide
- [gaia-dev Documentation](docs/gaia-dev/README.md) - Development container guide
- [gaia-windows Documentation](docs/gaia-windows/README.md) - Windows container (planned)

### Additional Guides
- [Using as Base Image](docs/dockerfile-usage.md) - Extend containers in your own Dockerfile
- [Building from Source](CLAUDE.md#development-commands) - Build containers locally

## Version Management

The GAIA version is managed in the `VERSION` file. All containers are tagged with explicit version numbers:

```bash
# Pull specific version
docker pull itomek/gaia-linux:0.15.1
docker pull itomek/gaia-dev:0.15.1

# No "latest" tag - ensures reproducibility
```

When a new GAIA version is released:
1. Update `VERSION` file
2. CI automatically builds and publishes new images
3. GitHub release created with version tag

## Development

### Running Tests

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest tests/ -v

# Run specific test suite
uv run pytest tests/test_dockerfile.py -v
```

### Building Locally

```bash
# Build gaia-linux
docker build -f gaia-linux/Dockerfile -t itomek/gaia-linux:0.15.1 .

# Build gaia-dev
docker build -f gaia-dev/Dockerfile -t itomek/gaia-dev:0.15.1 .
```

See [CLAUDE.md](CLAUDE.md) for complete development documentation.

## Support

- **GAIA Framework Issues**: https://github.com/amd/gaia/issues
- **Docker Container Issues**: https://github.com/itomek/gaia-docker/issues
- **GAIA Documentation**: https://github.com/amd/gaia

## Contributing

Contributions welcome! Please:
1. Read [CLAUDE.md](CLAUDE.md) for project structure and development workflow
2. Open an issue to discuss significant changes
3. Submit pull requests with tests

## License

MIT License - see [LICENSE](LICENSE) file

## Related Projects

- [AMD GAIA](https://github.com/amd/gaia) - The AI framework these containers package
- [Claude Code](https://claude.ai/code) - AI coding assistant included in gaia-dev

---

**Docker Hub**:
- https://hub.docker.com/r/itomek/gaia-linux
- https://hub.docker.com/r/itomek/gaia-dev
