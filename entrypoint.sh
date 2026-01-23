#!/bin/bash
set -e

# GAIA Development Container Entrypoint
# Clones GAIA repository and installs dependencies at runtime

echo "=== GAIA Development Container ==="

# Configuration from environment variables
GAIA_REPO="${GAIA_REPO:-https://github.com/amd/gaia.git}"
GAIA_BRANCH="${GAIA_BRANCH:-main}"
GAIA_DIR="/source/gaia"
SKIP_INSTALL="${SKIP_INSTALL:-false}"

echo "Repository: $GAIA_REPO"
echo "Branch: $GAIA_BRANCH"
echo "Target: $GAIA_DIR"

# Configure git credentials if GitHub token provided
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Configuring GitHub credentials..."
    git config --global credential.helper store
    echo "https://x-access-token:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
    chmod 600 ~/.git-credentials
fi

# Clone or update GAIA repository
if [ ! -d "$GAIA_DIR/.git" ]; then
    echo "Cloning GAIA from $GAIA_REPO (branch: $GAIA_BRANCH)..."
    git clone --depth 1 --branch "$GAIA_BRANCH" "$GAIA_REPO" "$GAIA_DIR"
    echo "Clone completed."
else
    echo "GAIA already cloned. Updating..."
    cd "$GAIA_DIR"
    git fetch origin "$GAIA_BRANCH" --depth 1
    git reset --hard "origin/$GAIA_BRANCH"
    echo "Update completed."
fi

cd "$GAIA_DIR"

# Install GAIA and dependencies
if [ "$SKIP_INSTALL" != "true" ]; then
    echo "Installing GAIA with dependencies (using uv for speed)..."
    echo "(First run: ~2-3 minutes, subsequent runs: ~30 seconds)"
    uv pip install --system -e ".[dev,mcp,eval,rag]"
    echo "Installation completed."
else
    echo "Skipping installation (SKIP_INSTALL=true)"
fi

echo ""
echo "=== Ready for development ==="
echo ""
echo "GAIA location: $GAIA_DIR"
echo "Claude Code: Run 'claude' to start (OAuth login on first use)"
echo "Access: docker exec -it <container> zsh"
echo ""

# Execute command passed to container
exec "$@"
