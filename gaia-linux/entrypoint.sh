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
SKIP_INSTALL="${SKIP_INSTALL:-false}"

# Install GAIA from PyPI
if [ "$SKIP_INSTALL" != "true" ]; then
    if [ -n "$GAIA_VERSION" ]; then
        echo "Installing GAIA version $GAIA_VERSION from PyPI..."
        if ! sudo "$HOME/.local/bin/uv" pip install --system --break-system-packages "amd-gaia[dev,mcp,eval,rag]==${GAIA_VERSION}"; then
            echo ""
            echo "ERROR: Failed to install amd-gaia==${GAIA_VERSION}"
            echo "Possible causes:"
            echo "  - Version '${GAIA_VERSION}' does not exist on PyPI"
            echo "  - PyPI is unreachable (check network connectivity)"
            echo "  - Package index is temporarily unavailable"
            echo "Check available versions: pip index versions amd-gaia"
            exit 1
        fi
    else
        echo "No GAIA_VERSION specified, installing latest from PyPI..."
        if ! sudo "$HOME/.local/bin/uv" pip install --system --break-system-packages "amd-gaia[dev,mcp,eval,rag]"; then
            echo ""
            echo "ERROR: Failed to install amd-gaia from PyPI"
            echo "Possible causes:"
            echo "  - PyPI is unreachable (check network connectivity)"
            echo "  - Package index is temporarily unavailable"
            exit 1
        fi
    fi

    # Log the actual installed version
    INSTALLED_VERSION=$(sudo "$HOME/.local/bin/uv" pip show amd-gaia 2>/dev/null | grep "^Version:" | awk '{print $2}')
    if [ -n "$INSTALLED_VERSION" ]; then
        echo "Installed GAIA version: $INSTALLED_VERSION"
    fi
else
    echo "Skipping installation (SKIP_INSTALL=true)"
fi

export LEMONADE_BASE_URL
echo "Lemonade base URL: $LEMONADE_BASE_URL"

echo ""
echo "=== Ready ==="
echo ""
echo "GAIA version: ${GAIA_VERSION:-latest}"
echo "Access: docker exec -it <container> zsh"
echo ""

# Execute command passed to container
exec "$@"
