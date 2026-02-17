# GAIA Development Container
# Includes GAIA source code, Claude Code, and development tools pre-installed
# GAIA runs from source at /home/gaia/gaia

FROM ubuntu:24.04

# GAIA version for reference (source is cloned from main branch)
ARG GAIA_VERSION=1.1.0
ENV GAIA_VERSION="${GAIA_VERSION}"

# Timezone configuration
ARG TZ=America/Los_Angeles
ENV TZ="$TZ"

# Prevent apt prompts during build
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies (NO Python - will be managed by uv)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core tools
    ca-certificates curl gnupg git procps sudo \
    # Shell and utilities
    fzf zsh man-db unzip nano vim wget less \
    # JSON processor
    jq \
    # Build tools (for Python packages with C extensions)
    build-essential \
    # Audio processing for GAIA voice features
    libportaudio2 portaudio19-dev ffmpeg \
    # Claude Code sandbox requirements (network isolation)
    iptables ipset iproute2 bind9-dnsutils aggregate \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI from official repository
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    gpg --dearmor -o /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (required for GAIA Electron apps)
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

# Install Claude Code using native installer (user-owned, supports auto-updates)
RUN curl -fsSL https://claude.ai/install.sh | bash

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.12 via uv (no system Python needed)
RUN /home/gaia/.local/bin/uv python install 3.12

# Create virtual environment using uv-managed Python
RUN /home/gaia/.local/bin/uv venv --python 3.12 /home/gaia/.venv

# Create python symlink for CLI convenience
RUN ln -sf /home/gaia/.venv/bin/python /home/gaia/.local/bin/python

# Configure environment
ENV SHELL=/bin/zsh
ENV VIRTUAL_ENV=/home/gaia/.venv
ENV PATH="/home/gaia/.venv/bin:/home/gaia/.cargo/bin:/home/gaia/.local/bin:$PATH"

ENV DEVCONTAINER=true

# Copy mode for mounted volumes
ENV UV_LINK_MODE=copy

# Create gaia directory for volume mount
RUN mkdir -p /home/$USERNAME/gaia

# Set working directory to gaia source
WORKDIR /home/$USERNAME/gaia

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["zsh"]
