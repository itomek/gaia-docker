#!/bin/bash
# Interactive setup script for GAIA Docker container (local development)
# Prompts for LEMONADE_URL configuration
# Note: For Docker Hub users, see docs/docker-hub.md for instructions

set -e

ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

echo "=== GAIA Docker Setup (Local Development) ==="
echo ""
echo "This script helps configure your local .env file for docker-compose."
echo "For Docker Hub usage, see docs/docker-hub.md"
echo ""

# Check if .env exists, if not copy from example
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        echo "Creating .env file from .env.example..."
        cp "$ENV_EXAMPLE" "$ENV_FILE"
    else
        echo "Error: .env.example not found!"
        exit 1
    fi
fi

# Function to update or add a variable in .env file
update_env() {
    local key=$1
    local value=$2
    local comment=$3
    
    if grep -q "^${key}=" "$ENV_FILE"; then
        # Update existing value
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
        else
            # Linux
            sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
        fi
    else
        # Add new value
        if [ -n "$comment" ]; then
            echo "" >> "$ENV_FILE"
            echo "# $comment" >> "$ENV_FILE"
        fi
        echo "${key}=${value}" >> "$ENV_FILE"
    fi
}

# LEMONADE_URL is optional (defaults to localhost:5000)
current_lemonade=$(grep "^LEMONADE_URL=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || echo "")
if [ -z "$current_lemonade" ] || [ "$current_lemonade" = "" ]; then
    echo "🍋 Lemonade Server URL (Optional)"
    echo "   Default: http://localhost:5000/api/v1 (for Lemonade running in container)"
    echo ""
    echo "   Options:"
    echo "   1. Press Enter to use default (localhost:5000)"
    echo "   2. Remote server: https://your-server.com/api/v1"
    echo "   3. Local server on host (macOS): http://host.docker.internal:5000/api/v1"
    echo "   4. Local server on host (Linux): http://172.17.0.1:5000/api/v1"
    echo ""
    read -p "Enter Lemonade URL [default: http://localhost:5000/api/v1]: " lemonade_url
    
    # Use default if empty
    if [ -z "$lemonade_url" ]; then
        lemonade_url="http://localhost:5000/api/v1"
        echo "   Using default: $lemonade_url"
    fi
    
    # Auto-detect 'local' keyword
    if [ "$lemonade_url" = "local" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            lemonade_url="http://host.docker.internal:5000/api/v1"
        else
            gateway_ip=$(docker network inspect bridge 2>/dev/null | grep -oP '"Gateway": "\K[^"]+' | head -1 || echo "172.17.0.1")
            lemonade_url="http://${gateway_ip}:5000/api/v1"
        fi
        echo "   Using local Lemonade at: $lemonade_url"
    fi
    
    update_env "LEMONADE_URL" "$lemonade_url" "Lemonade server URL (defaults to http://localhost:5000/api/v1)"
    echo "✅ Lemonade URL saved"
    echo ""
else
    echo "✅ Lemonade URL already configured: $current_lemonade"
    echo ""
fi

# Optional: Ask about port conflicts
echo "🔌 Port Configuration (Optional)"
read -p "Do you want to customize ports? (y/N): " customize_ports
if [[ "$customize_ports" =~ ^[Yy]$ ]]; then
    current_lemonade_port=$(grep "^LEMONADE_PORT=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || echo "5001")
    read -p "Lemonade port [default: 5001]: " lemonade_port
    lemonade_port=${lemonade_port:-5001}
    update_env "LEMONADE_PORT" "$lemonade_port" "Lemonade server port"
    
    current_api_port=$(grep "^GAIA_API_PORT=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || echo "8000")
    read -p "GAIA API port [default: 8000]: " api_port
    api_port=${api_port:-8000}
    update_env "GAIA_API_PORT" "$api_port" "GAIA API port"
    
    current_web_port=$(grep "^WEB_PORT=" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || echo "3000")
    read -p "Web app port [default: 3000]: " web_port
    web_port=${web_port:-3000}
    update_env "WEB_PORT" "$web_port" "Web app port"
    
    echo "✅ Ports configured"
    echo ""
fi

echo "=== Setup Complete ==="
echo ""
echo "Configuration saved to: $ENV_FILE"
echo ""
echo "Next steps:"
echo "  1. Review your .env file if needed"
echo "  2. Start the container: docker compose up -d"
echo "  3. Connect: docker exec -it gaia-dev zsh"
echo ""
