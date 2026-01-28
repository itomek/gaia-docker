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
    """Return path to gaia-linux Dockerfile."""
    return project_root / "gaia-linux" / "Dockerfile"


@pytest.fixture(scope="session")
def entrypoint_path(project_root):
    """Return path to gaia-linux entrypoint.sh."""
    return project_root / "gaia-linux" / "entrypoint.sh"


@pytest.fixture(scope="session")
def dockerfile_dev_path(project_root):
    """Return path to gaia-dev Dockerfile."""
    return project_root / "gaia-dev" / "Dockerfile"


@pytest.fixture(scope="session")
def entrypoint_dev_path(project_root):
    """Return path to gaia-dev entrypoint.sh."""
    return project_root / "gaia-dev" / "entrypoint.sh"


@pytest.fixture(scope="module")
def gaia_container(project_root):
    """Build and start GAIA container for integration tests."""
    subprocess.run(
        ["docker", "build", "-t", "gaia-linux:test", "-f", "gaia-linux/Dockerfile", str(project_root)],
        check=True,
        capture_output=True,
        text=True,
        timeout=600
    )
    container = (
        DockerContainer("gaia-linux:test")
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


@pytest.fixture(scope="module")
def gaia_dev_container(project_root):
    """Build and start GAIA dev container for integration tests."""
    subprocess.run(
        ["docker", "build", "-t", "gaia-dev:test", "-f", "gaia-dev/Dockerfile", str(project_root)],
        check=True,
        capture_output=True,
        text=True,
        timeout=900
    )
    container = (
        DockerContainer("gaia-dev:test")
        .with_env("LEMONADE_BASE_URL", "http://localhost:5000/api/v1")
        .with_command("sleep infinity")
    )

    with container:
        # Wait for entrypoint to complete
        start = time.time()
        while time.time() - start < 120:
            logs = container.get_wrapped_container().logs().decode("utf-8", errors="ignore")
            if "=== Ready ===" in logs:
                break
            time.sleep(1)
        else:
            raise TimeoutError("Dev container did not become ready within 120 seconds")
        yield container


@pytest.fixture
def dev_container_exec(gaia_dev_container):
    """Helper to execute commands in dev container."""
    def _exec(command, **kwargs):
        result = gaia_dev_container.exec(command, **kwargs)
        return result
    return _exec
