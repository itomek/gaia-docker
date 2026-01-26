# GAIA Linux Container
# Provides isolated Python 3.12 environment for GAIA
# GAIA is installed from PyPI at runtime based on version

FROM python:3.12-slim

# GAIA version (set via build arg, defaults to 0.15.1)
ARG GAIA_VERSION=0.15.1
ENV GAIA_VERSION="${GAIA_VERSION}"

# Timezone configuration
ARG TZ=America/Los_Angeles
ENV TZ="$TZ"

# Install system dependencies
# Combined into single layer for efficiency
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to gaia user
USER $USERNAME
WORKDIR /source

# Install oh-my-zsh with useful plugins
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git -p fzf -p python -x

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure environment
ENV SHELL=/bin/zsh
ENV PATH="/home/gaia/.cargo/bin:/home/gaia/.local/bin:$PATH"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["zsh"]
