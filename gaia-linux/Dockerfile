# GAIA Linux Container
# Provides isolated Python 3.12 environment for GAIA
# GAIA is installed from PyPI at runtime based on version

FROM ubuntu:24.04

# GAIA version - optional, if not set the entrypoint installs latest from PyPI
ARG GAIA_VERSION
ENV GAIA_VERSION="${GAIA_VERSION}"

# Timezone configuration
ARG TZ=America/Los_Angeles
ENV TZ="$TZ"

# Prevent apt prompts during build
ARG DEBIAN_FRONTEND=noninteractive

# Install Python 3.12 (required for system-wide pip install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-dev \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf /usr/bin/pip3 /usr/bin/pip \
    && rm -rf /var/lib/apt/lists/*

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core runtime
    ca-certificates curl sudo procps file \
    # Shell (needed for entrypoint and user interaction)
    zsh \
    # Git (required for oh-my-zsh installation)
    git \
    # Build tools (for Python packages with C extensions)
    build-essential \
    # Audio processing for GAIA voice features
    libportaudio2 portaudio19-dev ffmpeg \
    # Editor
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 (required for GAIA Electron apps)
ARG NODE_MAJOR=20
RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg && \
    mkdir -p /etc/apt/keyrings && \
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
COPY gaia-linux/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to gaia user
USER $USERNAME
WORKDIR /source

# Install Homebrew
ENV HOMEBREW_NO_ANALYTICS=1
ENV HOMEBREW_NO_AUTO_UPDATE=1
ENV HOMEBREW_NO_INSTALL_CLEANUP=1
RUN NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/6d5e2670d07961e7985d2079a2f0a484420f3c38/install.sh)"

# Configure Vim
COPY --chown=gaia:gaia .vimrc /home/gaia/.vimrc

# Install oh-my-zsh with useful plugins
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(curl -fsSL https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git -p fzf -p python -x

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure environment
ENV SHELL=/bin/zsh
ENV TERM=xterm-256color
ENV COLORTERM=truecolor
ENV EDITOR=vim
ENV VISUAL=vim
ENV PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:/home/gaia/.cargo/bin:/home/gaia/.local/bin:$PATH"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["zsh"]
