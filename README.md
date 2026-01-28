# GAIA Docker

Docker containers for [AMD GAIA](https://github.com/amd/gaia).

**Current GAIA Version**: 0.15.1

## Available Containers

| Container | Description | GAIA Source |
|-----------|-------------|-------------|
| `itomek/gaia-linux` | Runtime container | Installed from PyPI at startup |
| `itomek/gaia-dev` | Development container with Claude Code | Cloned from source, pre-installed |

---

# GAIA Linux (`itomek/gaia-linux`)

Runtime container - GAIA installed from PyPI at startup.

## 1. Pull Image

```bash
docker pull itomek/gaia-linux:0.15.1
```

## 2. Run Container

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

## 3. Connect

```bash
docker exec -it gaia-linux zsh
```

## 4. Use GAIA

```bash
gaia --version
```

For the rest of GAIA usage, see https://github.com/AMD/GAIA

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | Yes | - | Lemonade server API endpoint |
| `GAIA_VERSION` | No | `0.15.1` | PyPI version to install |
| `SKIP_INSTALL` | No | `false` | Skip package installation for faster restarts |

---

# GAIA Dev (`itomek/gaia-dev`)

Development container with Claude Code and dev tools.

## 1. Pull Image

```bash
docker pull itomek/gaia-dev:0.15.1
```

## 2. Run Container

```bash
docker run -dit \
  --name gaia-dev \
  -v gaia-src:/home/gaia/gaia \
  -e LEMONADE_BASE_URL=https://your-server.com/api/v1 \
  -e GITHUB_TOKEN=ghp_your_token \
  -e GAIA_REPO_URL=https://github.com/amd/gaia.git \
  itomek/gaia-dev:0.15.1
```

## 3. Connect

```bash
docker exec -it gaia-dev zsh
```

## 4. Use GAIA

```bash
gaia --version
claude  # Start Claude Code
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | Yes | - | Lemonade server API endpoint |
| `GITHUB_TOKEN` | Yes | - | GitHub token for authenticated cloning and CLI |
| `GAIA_REPO_URL` | Yes | - | Git repository to clone |
| `ANTHROPIC_API_KEY` | No | - | Claude Code API key (fallback: interactive login) |
| `SKIP_GAIA_CLONE` | No | `false` | Skip cloning GAIA repository |

---

## Additional Documentation

- [Using as Base Image](docs/dockerfile-usage.md)
- [Building from Source](docs/building.md)

## Testing

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest tests/ -v
```

## License

MIT License - see [LICENSE](LICENSE) file

## Related Projects

- [AMD GAIA](https://github.com/amd/gaia) - Main GAIA framework

## Support

- **GAIA Issues**: https://github.com/amd/gaia/issues
- **Docker Issues**: https://github.com/itomek/gaia-docker/issues
