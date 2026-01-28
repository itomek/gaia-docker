# Docker Hub Image Description

Use this as the description when publishing the image to Docker Hub:

---

# GAIA Docker

Docker containers for [AMD GAIA](https://github.com/amd/gaia).

**Current GAIA Version**: 0.15.1

## Available Containers

- **`itomek/gaia-linux`** - Runtime container (GAIA from PyPI)
- **`itomek/gaia-dev`** - Development container (GAIA from source + Claude Code)

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

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | Yes | - | Lemonade server API endpoint |
| `GAIA_VERSION` | No | `0.15.1` | PyPI version to install |
| `SKIP_INSTALL` | No | `false` | Skip package installation |

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
| `GITHUB_TOKEN` | Yes | - | GitHub token for authenticated cloning |
| `GAIA_REPO_URL` | Yes | - | Git repository to clone |
| `ANTHROPIC_API_KEY` | No | - | Claude Code API key |
| `SKIP_GAIA_CLONE` | No | `false` | Skip cloning repository |

---

## Features

- ✅ Version-pinned to specific GAIA releases
- ✅ Fast installation with `uv` package manager
- ✅ Complete isolation
- ✅ Multi-instance support

## Documentation

Full documentation: https://github.com/itomek/gaia-docker

---
