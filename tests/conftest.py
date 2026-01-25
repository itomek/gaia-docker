"""Pytest fixtures for GAIA Docker tests."""

import os
import pytest
from pathlib import Path
from testcontainers.core.container import DockerContainer


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def dockerfile_path(project_root):
    """Return path to Dockerfile."""
    return project_root / "Dockerfile"


@pytest.fixture(scope="session")
def entrypoint_path(project_root):
    """Return path to entrypoint.sh."""
    return project_root / "entrypoint.sh"


@pytest.fixture(scope="module")
def gaia_container(project_root):
    """Build and start GAIA container for integration tests."""
    container = (
        DockerContainer(str(project_root))
        .with_env("LEMONADE_URL", "http://localhost:5000/api/v1")
        .with_env("GAIA_BRANCH", "main")
        .with_env("SKIP_INSTALL", "false")
        .with_command("sleep infinity")
    )

    with container:
        # Wait for entrypoint to complete
        container.get_wrapped_container().wait(
            condition="Ready for development",
            timeout=300
        )
        yield container


@pytest.fixture
def container_exec(gaia_container):
    """Helper to execute commands in container."""
    def _exec(command, **kwargs):
        result = gaia_container.exec(command, **kwargs)
        return result
    return _exec
