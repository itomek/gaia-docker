"""Tests for entrypoint.sh script functionality."""

import pytest


class TestEntrypointScript:
    """Test entrypoint script exists and is executable."""

    def test_entrypoint_exists(self, entrypoint_path):
        """entrypoint.sh must exist."""
        assert entrypoint_path.exists(), "entrypoint.sh not found"

    def test_entrypoint_executable(self, entrypoint_path):
        """entrypoint.sh must be executable."""
        assert entrypoint_path.stat().st_mode & 0o111, "entrypoint.sh not executable"

    def test_entrypoint_has_shebang(self, entrypoint_path):
        """entrypoint.sh must have proper shebang."""
        content = entrypoint_path.read_text()
        assert content.startswith("#!/bin/bash")

    def test_entrypoint_uses_set_e(self, entrypoint_path):
        """entrypoint.sh should fail fast on errors."""
        content = entrypoint_path.read_text()
        assert "set -e" in content


class TestDependencyInstallation:
    """Test GAIA dependency installation."""

    @pytest.mark.integration
    def test_gaia_installed(self, container_exec):
        """Should install GAIA package."""
        result = container_exec("python -c 'import gaia'")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_dev_dependencies_installed(self, container_exec):
        """Should install dev dependencies."""
        result = container_exec("python -c 'import pytest'")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_mcp_dependencies_installed(self, container_exec):
        """Should install MCP dependencies."""
        result = container_exec("python -c 'import mcp'")
        assert result.exit_code == 0


class TestEnvironmentConfiguration:
    """Test environment variable handling."""

    def test_respects_gaia_version_env(self, entrypoint_path):
        """Should respect GAIA_VERSION environment variable."""
        content = entrypoint_path.read_text()
        assert 'GAIA_VERSION="${GAIA_VERSION:-' in content

    def test_requires_lemonade_base_url_env(self, entrypoint_path):
        """Should require LEMONADE_BASE_URL environment variable."""
        content = entrypoint_path.read_text()
        assert 'if [ -z "$LEMONADE_BASE_URL" ]' in content
        assert 'ERROR: LEMONADE_BASE_URL environment variable is required' in content

    def test_respects_skip_install_env(self, entrypoint_path):
        """Should respect SKIP_INSTALL environment variable."""
        content = entrypoint_path.read_text()
        assert 'SKIP_INSTALL' in content

class TestLemonadeBaseUrlValidation:
    """Test LEMONADE_BASE_URL validation at runtime."""

    @pytest.mark.integration
    def test_container_fails_without_lemonade_url(self, project_root):
        """Container should fail to start without LEMONADE_BASE_URL."""
        import subprocess
        import time

        # Try to run container without LEMONADE_BASE_URL
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "sleep", "1"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should fail with error message
        assert result.returncode != 0
        assert "ERROR: LEMONADE_BASE_URL environment variable is required" in result.stderr or \
               "ERROR: LEMONADE_BASE_URL environment variable is required" in result.stdout

    @pytest.mark.integration
    def test_container_starts_with_lemonade_url(self, project_root):
        """Container should start successfully with LEMONADE_BASE_URL."""
        import subprocess

        # Run container with LEMONADE_BASE_URL
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://localhost:5000/api/v1",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test", "echo", "success"],
            capture_output=True,
            text=True,
            timeout=30
        )

        # Should succeed
        assert result.returncode == 0


class TestHostDirectoryMount:
    """Test optional host directory mounting."""

    @pytest.mark.integration
    def test_host_directory_exists(self, project_root):
        """Container should have /host directory for optional mounting."""
        import subprocess
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://localhost:5000/api/v1",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test", "ls", "-ld", "/host"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "drwxr" in result.stdout or "drwx" in result.stdout

    @pytest.mark.integration
    def test_host_directory_writable_by_gaia_user(self, project_root):
        """The /host directory should be writable by gaia user."""
        import subprocess
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://localhost:5000/api/v1",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test", "sh", "-c", "touch /host/test_file && rm /host/test_file && echo success"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "success" in result.stdout
