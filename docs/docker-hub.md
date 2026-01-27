# Using GAIA Docker from Docker Hub

This image is published on Docker Hub as `itomek/gaia-linux:<version>`. This is a Linux container.

**Current GAIA Version**: 0.15.1 (matches PyPI `amd-gaia` package)

## Versioning

Images are tagged with the GAIA version they contain. We only publish specific version tags (no `latest` tag). The container installs GAIA from PyPI, so the version matches the `amd-gaia` package version.

- `itomek/gaia-linux:0.15.1` - Current version
- `itomek/gaia-linux:0.15.2` - Future versions (when available)

## Quick Start

### 1. Pull the Image

**Current version:**
```bash
docker pull itomek/gaia-linux:0.15.1
```

**Other versions:**
```bash
docker pull itomek/gaia-linux:0.15.2  # When available
```

### 2. Run the Container

**LEMONADE_BASE_URL is required** - set it to your Lemonade server's API endpoint.

```bash
docker run -dit \
  --name gaia-linux \
  -e LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1 \
  itomek/gaia-linux:0.15.1
```

### 3. Connect to Container

```bash
docker exec -it gaia-linux zsh
```


## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LEMONADE_BASE_URL` | **Yes** | N/A | Lemonade server base URL |
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
docker exec -it gaia-linux zsh

# Test GAIA (already installed)
gaia --version
```

For the rest of GAIA usage, see https://github.com/AMD/GAIA

## Troubleshooting

### Container exits immediately

Check logs:
```bash
docker logs gaia-linux
```

If the container exits, check the logs for specific error messages. Make sure you provided the required LEMONADE_BASE_URL environment variable.

### GAIA says "Lemonade server is not running"

Verify `LEMONADE_BASE_URL` is set correctly:
```bash
docker exec gaia-linux env | grep LEMONADE_BASE_URL
```

Make sure the URL is accessible from inside the container.

