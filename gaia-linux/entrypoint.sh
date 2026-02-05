#!/bin/bash
set -e

# GAIA Linux Container Entrypoint
# Installs GAIA from PyPI at runtime

echo "=== GAIA Linux Container ==="

# Validate required LEMONADE_BASE_URL environment variable FIRST
# This ensures fast failure if the required environment variable is missing
if [ -z "$LEMONADE_BASE_URL" ]; then
    echo "ERROR: LEMONADE_BASE_URL environment variable is required."
    echo "Example: -e LEMONADE_BASE_URL=https://your-server.com/api/v1"
    exit 1
fi

# Configuration from environment variables
GAIA_VERSION="${GAIA_VERSION:-0.15.3}"
SKIP_INSTALL="${SKIP_INSTALL:-false}"

echo "GAIA Version: $GAIA_VERSION"

# Install GAIA from PyPI with specific version
if [ "$SKIP_INSTALL" != "true" ]; then
    echo "Installing GAIA version $GAIA_VERSION from PyPI (using uv for speed)..."
    echo "(First run: ~2-3 minutes, subsequent runs: ~30 seconds)"
    sudo "$HOME/.local/bin/uv" pip install --system --break-system-packages "amd-gaia[dev,mcp,eval,rag]==${GAIA_VERSION}"
    echo "Installation completed."
else
    echo "Skipping installation (SKIP_INSTALL=true)"
fi

export LEMONADE_BASE_URL
echo "Lemonade base URL: $LEMONADE_BASE_URL"

echo ""
echo "=== Ready ==="
echo ""
echo "GAIA version: $GAIA_VERSION"
echo "Access: docker exec -it <container> zsh"
echo ""

# Execute command passed to container
exec "$@"
