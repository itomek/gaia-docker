"""Pytest fixtures for GAIA Docker tests."""

import pytest
import subprocess
import time
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
    subprocess.run(
        ["docker", "build", "-t", "gaia-dev:test", str(project_root)],
        check=True,
        capture_output=True,
        text=True,
        timeout=600
    )
    container = (
        DockerContainer("gaia-dev:test")
        .with_env("SKIP_INSTALL", "false")
        .with_command("sleep infinity")
    )

    with container:
        # Wait for entrypoint to complete
        start = time.time()
        while time.time() - start < 600:
            logs = container.get_wrapped_container().logs().decode("utf-8", errors="ignore")
            if "=== Ready ===" in logs:
                break
            time.sleep(1)
        else:
            raise TimeoutError("Container did not become ready within 600 seconds")
        yield container


@pytest.fixture
def container_exec(gaia_container):
    """Helper to execute commands in container."""
    def _exec(command, **kwargs):
        result = gaia_container.exec(command, **kwargs)
        return result
    return _exec
