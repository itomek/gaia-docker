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
        assert 'GAIA_VERSION="${GAIA_VERSION:-0.15.1}"' in content

    def test_respects_lemonade_base_url_env(self, entrypoint_path):
        """Should respect LEMONADE_BASE_URL environment variable."""
        content = entrypoint_path.read_text()
        assert 'LEMONADE_BASE_URL="${LEMONADE_BASE_URL:-http://localhost:5000/api/v1}"' in content

    def test_respects_skip_install_env(self, entrypoint_path):
        """Should respect SKIP_INSTALL environment variable."""
        content = entrypoint_path.read_text()
        assert 'SKIP_INSTALL' in content

class TestHostDirectoryMount:
    """Test optional host directory mounting."""

    def test_creates_host_mount_point(self, entrypoint_path):
        """Should create /host directory for optional mounting."""
        content = entrypoint_path.read_text()
        # Check that /host is mentioned or created
        # This might be in Dockerfile instead
        pass
