#!/bin/bash
set -e

# GAIA Linux Container Entrypoint
# Installs GAIA from PyPI at runtime

echo "=== GAIA Linux Container ==="

# Configuration from environment variables
GAIA_VERSION="${GAIA_VERSION:-0.15.1}"
SKIP_INSTALL="${SKIP_INSTALL:-false}"

echo "GAIA Version: $GAIA_VERSION"

# Install GAIA from PyPI with specific version
if [ "$SKIP_INSTALL" != "true" ]; then
    echo "Installing GAIA version $GAIA_VERSION from PyPI (using uv for speed)..."
    echo "(First run: ~2-3 minutes, subsequent runs: ~30 seconds)"
    sudo "$HOME/.local/bin/uv" pip install --system "amd-gaia[dev,mcp,eval,rag]==${GAIA_VERSION}"
    echo "Installation completed."
else
    echo "Skipping installation (SKIP_INSTALL=true)"
fi

# Export LEMONADE_URL to environment (defaults to localhost:5000)
LEMONADE_URL="${LEMONADE_URL:-http://localhost:5000/api/v1}"
export LEMONADE_URL
echo "Lemonade server: $LEMONADE_URL"

echo ""
echo "=== Ready ==="
echo ""
echo "GAIA version: $GAIA_VERSION"
echo "Access: docker exec -it <container> zsh"
echo ""

# Execute command passed to container
exec "$@"
