# GAIA Development Container
# Includes GAIA source code, Claude Code, and development tools pre-installed
# GAIA runs from source at /home/gaia/gaia

FROM python:3.12-slim

# GAIA version for reference (source is cloned from main branch)
ARG GAIA_VERSION=1.0.0
ENV GAIA_VERSION="${GAIA_VERSION}"

# Timezone configuration
ARG TZ=America/Los_Angeles
ENV TZ="$TZ"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core tools
    ca-certificates curl gnupg git procps sudo \
    # Shell and utilities
    fzf zsh man-db unzip nano vim wget less \
    # GitHub CLI
    gh \
    # JSON processor
    jq \
    # Build tools (for Python packages with C extensions)
    build-essential \
    # Audio processing for GAIA voice features
    libportaudio2 portaudio19-dev ffmpeg \
    # Claude Code sandbox requirements (network isolation)
    iptables ipset iproute2 dnsutils aggregate \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (required for GAIA Electron apps and Claude Code)
ARG NODE_MAJOR=20
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | \
    gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" \
    > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Claude Code globally via npm
RUN npm install -g @anthropic-ai/claude-code

# Create gaia user with passwordless sudo
ARG USERNAME=gaia
RUN useradd -m -s /bin/zsh $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Create working directories
RUN mkdir -p /source /host && \
    chown -R $USERNAME:$USERNAME /source /host

# Copy entrypoint script
COPY gaia-dev/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to gaia user
USER $USERNAME
WORKDIR /home/$USERNAME

# Install oh-my-zsh with useful plugins
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git -p fzf -p python -x

# Ensure virtual environment is activated in interactive shells
RUN echo 'source /home/gaia/.venv/bin/activate' >> /home/gaia/.zshrc

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment owned by gaia user
RUN /home/gaia/.local/bin/uv venv /home/gaia/.venv

# Configure environment
ENV SHELL=/bin/zsh
ENV VIRTUAL_ENV=/home/gaia/.venv
ENV PATH="/home/gaia/.venv/bin:/home/gaia/.cargo/bin:/home/gaia/.local/bin:$PATH"

# Copy mode for mounted volumes
ENV UV_LINK_MODE=copy

# Create gaia directory for volume mount
RUN mkdir -p /home/$USERNAME/gaia

# Set working directory to gaia source
WORKDIR /home/$USERNAME/gaia

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["zsh"]
