# Using This Image in Your Dockerfile

You can use this image as a base in your own Dockerfile to extend or customize it.

## Basic Usage

```dockerfile
FROM itomek/gaia-dev:0.15.1

# Your customizations here
RUN echo "Custom setup"

# The entrypoint will automatically install GAIA version 0.15.1
```

## Using a Specific GAIA Version

```dockerfile
FROM itomek/gaia-dev:0.15.1

# This image already has GAIA 0.15.1 pre-configured
# Add your customizations
```

## Overriding GAIA Version

You can override the GAIA version by setting the `GAIA_VERSION` environment variable:

```dockerfile
FROM itomek/gaia-dev:0.15.1

# Override to use a different GAIA version
ENV GAIA_VERSION=0.15.1

# The entrypoint will install the specified version from PyPI
```

## Custom Environment Variables

```dockerfile
FROM itomek/gaia-dev:0.15.1

# Set custom Lemonade base URL
ENV LEMONADE_BASE_URL=https://your-server.com/api/v1

# Add your custom setup
RUN your-custom-commands
```

## Example: Custom Development Setup

```dockerfile
FROM itomek/gaia-dev:0.15.1

# Install additional tools
RUN apt-get update && \
    apt-get install -y your-tools && \
    apt-get clean

# Set up custom configuration
ENV LEMONADE_BASE_URL=https://your-lemonade-server.com/api/v1
ENV CUSTOM_VAR=value

# Copy your scripts
COPY scripts/ /usr/local/bin/

# The base image's entrypoint will handle GAIA installation
```

## Building Your Custom Image

```bash
docker build -t my-gaia-dev:latest .
docker run -d --name my-gaia-dev my-gaia-dev:latest
docker exec -it my-gaia-dev zsh
```

## Notes

- The base image's entrypoint automatically installs GAIA from PyPI
- GAIA version is determined by the image tag or `GAIA_VERSION` environment variable
- All environment variables from the base image are available
- The container runs as user `gaia` with passwordless sudo
