#!/bin/bash
set -e

# GAIA Development Container Entrypoint
# Clones GAIA on first run, configures GitHub CLI and Claude Code

echo "=== GAIA Development Container ==="

# Validate required LEMONADE_BASE_URL environment variable
if [ -z "$LEMONADE_BASE_URL" ]; then
    echo "ERROR: LEMONADE_BASE_URL environment variable is required."
    echo "Example: -e LEMONADE_BASE_URL=https://your-server.com/api/v1"
    exit 1
fi

export LEMONADE_BASE_URL
echo "Lemonade base URL: $LEMONADE_BASE_URL"

# Clone GAIA source if not present (first run with empty volume)
GAIA_DIR="/home/gaia/gaia"
GAIA_REPO_URL="${GAIA_REPO_URL:-https://github.com/amd/gaia.git}"

UPSTREAM_URL="https://github.com/amd/gaia.git"

if [ ! -d "$GAIA_DIR/.git" ]; then
    echo "Cloning GAIA from: $GAIA_REPO_URL"

    # Use token authentication if GITHUB_TOKEN is set
    if [ -n "$GITHUB_TOKEN" ]; then
        # Insert token into URL for authentication
        AUTH_URL=$(echo "$GAIA_REPO_URL" | sed "s|https://|https://${GITHUB_TOKEN}@|")
        git clone "$AUTH_URL" "$GAIA_DIR"
    else
        git clone "$GAIA_REPO_URL" "$GAIA_DIR"
    fi

    # Add upstream remote pointing to main GAIA repo
    cd "$GAIA_DIR"
    if [ "$GAIA_REPO_URL" != "$UPSTREAM_URL" ]; then
        echo "Adding upstream remote: $UPSTREAM_URL"
        git remote add upstream "$UPSTREAM_URL"
    fi

    echo "Installing GAIA dependencies..."
    sudo /home/gaia/.local/bin/uv pip install --system -e ".[dev,mcp,eval,rag]"
    if [ -f package.json ]; then
        npm install
    fi
    echo "GAIA installation complete."
else
    echo "GAIA source found at $GAIA_DIR"
fi

# Configure GitHub CLI if GITHUB_TOKEN is provided
if [ -n "$GITHUB_TOKEN" ]; then
    echo "Configuring GitHub CLI with provided token..."
    echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null && \
        echo "GitHub CLI configured successfully." || \
        echo "Warning: GitHub CLI configuration failed."
else
    echo "GITHUB_TOKEN not set. Run 'gh auth login' to authenticate GitHub CLI."
fi

# Configure Claude Code
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "ANTHROPIC_API_KEY detected. Claude Code will use this API key."
    export ANTHROPIC_API_KEY
else
    echo "ANTHROPIC_API_KEY not set. Run 'claude' to authenticate interactively."
fi

echo ""
echo "=== Ready ==="
echo ""
echo "GAIA source: ~/gaia"
echo "GAIA version: $GAIA_VERSION"
echo ""
echo "Available commands:"
echo "  claude        - Start Claude Code"
echo "  gh            - GitHub CLI"
echo "  gaia --version - Verify GAIA installation"
echo ""
echo "Access: docker exec -it <container> zsh"
echo ""

# Execute command passed to container
exec "$@"
