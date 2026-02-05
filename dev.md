# Development Guide

Developer documentation for GAIA Docker project.

## Development Setup

### Prerequisites

- Docker and Docker Compose installed
- Python 3.12+ and uv installed (for running tests)

### Running Tests

**Quick test:**
```bash
uv sync
uv run pytest tests/ -v
```

**Full testing guide:**

1. **Unit Tests** (no container required):
   ```bash
   uv run pytest tests/test_dockerfile.py tests/test_entrypoint.py -v
   ```

2. **Integration Tests** (requires container):
   ```bash
   uv run pytest tests/test_container.py -v -m integration
   ```

3. **All Tests**:
   ```bash
   uv run pytest tests/ -v
   ```

## Publishing New Versions

### Version Management

Container versions are defined in the `VERSION.json` file in the repository root. This JSON file contains independent version numbers for each container type.

### Updating the Version

1. **Update `VERSION.json` file** with the new version(s):
   ```json
   {
     "gaia-linux": "0.15.3",
     "gaia-dev": "1.0.0"
   }
   ```
2. **Create a pull request** with the version change
3. **CI will automatically**:
   - Read versions from `VERSION.json` using jq
   - Build Docker images with their respective GAIA versions
   - Tag images with versions (e.g., `itomek/gaia-linux:0.15.2`, `itomek/gaia-dev:1.0.0`)
   - Publish to Docker Hub

### Version File Format

The `VERSION.json` file should contain a JSON object with version numbers for each container:
```json
{
  "gaia-linux": "0.15.3",
  "gaia-dev": "1.0.0"
}
```

- **gaia-linux**: Should match the PyPI `amd-gaia` package version
- **gaia-dev**: Independent versioning for development container features

**Important**: We only publish specific version tags (no `latest` tag). Each version is explicitly tagged.

## Docker Hub Publishing Setup

### Required GitHub Secrets

1. **DOCKERHUB_USERNAME** - Your Docker Hub username
2. **DOCKERHUB_TOKEN** - Docker Hub access token (create at https://hub.docker.com/settings/security)

### Publishing Workflow

The image publishes automatically when:
- You push to `main` branch (if `VERSION` file changed)
- You create a pull request that updates `VERSION`

The CI workflow:
1. Reads `VERSION.json` file using jq
2. Builds images with `GAIA_VERSION` build args set to their respective versions
3. Tags images as `itomek/gaia-linux:<version>` and `itomek/gaia-dev:<version>`
4. Pushes to Docker Hub

**Note**: We only publish specific version tags (no `latest` tag). Each version is explicitly tagged.

## Testing Guide

### Prerequisites

1. **Docker and Docker Compose** installed and running
2. **Python 3.12+** and **uv** installed
3. **Test dependencies** installed: `uv sync`

### Quick Manual Test

```bash
docker run -dit \
  --name gaia-linux-test \
  -e LEMONADE_BASE_URL=http://localhost:5000/api/v1 \
  itomek/gaia-linux:0.15.3

docker logs -f gaia-linux-test
# Wait for "Ready for development"
docker exec -it gaia-linux-test zsh -c "gaia --version"
docker stop gaia-linux-test && docker rm gaia-linux-test
```

### Automated Testing

**Unit Tests** (no container required):
```bash
uv run pytest tests/test_dockerfile.py tests/test_entrypoint.py -v
```

**Integration Tests** (requires container):
```bash
uv run pytest tests/test_container.py -v -m integration
```

**All Tests**:
```bash
uv run pytest tests/ -v
```

### CI/CD Testing

Tests run automatically in GitHub Actions on pull requests and pushes to `main`.

## Code Style

- Follow existing code style
- Run tests before submitting PRs
- Update documentation if needed
