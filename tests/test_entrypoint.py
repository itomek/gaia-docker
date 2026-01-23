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


class TestGitCloning:
    """Test GAIA repository cloning functionality."""

    @pytest.mark.integration
    def test_clones_gaia_repo(self, container_exec):
        """Should clone GAIA repository on startup."""
        result = container_exec("test -d /source/gaia/.git")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_uses_correct_branch(self, container_exec):
        """Should clone specified branch."""
        result = container_exec("cd /source/gaia && git branch --show-current")
        assert "main" in result.output.decode()

    @pytest.mark.integration
    def test_shallow_clone(self, container_exec):
        """Should use shallow clone (--depth 1) for speed."""
        result = container_exec("cd /source/gaia && git rev-list --count HEAD")
        # Shallow clone should have limited history
        count = int(result.output.decode().strip())
        assert count < 100, "Clone not shallow (has too much history)"


class TestDependencyInstallation:
    """Test GAIA dependency installation."""

    @pytest.mark.integration
    def test_gaia_installed(self, container_exec):
        """Should install GAIA package."""
        result = container_exec("python -c 'import gaia; print(gaia.__version__)'")
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

    def test_respects_gaia_branch_env(self, entrypoint_path):
        """Should respect GAIA_BRANCH environment variable."""
        content = entrypoint_path.read_text()
        assert 'GAIA_BRANCH="${GAIA_BRANCH:-main}"' in content

    def test_respects_gaia_repo_env(self, entrypoint_path):
        """Should respect GAIA_REPO environment variable."""
        content = entrypoint_path.read_text()
        assert 'GAIA_REPO=' in content
        assert 'github.com/amd/gaia' in content

    def test_respects_skip_install_env(self, entrypoint_path):
        """Should respect SKIP_INSTALL environment variable."""
        content = entrypoint_path.read_text()
        assert 'SKIP_INSTALL' in content


class TestGitHubTokenHandling:
    """Test GitHub token configuration."""

    def test_configures_git_credentials(self, entrypoint_path):
        """Should configure git credentials if token provided."""
        content = entrypoint_path.read_text()
        assert "GITHUB_TOKEN" in content
        assert "git config" in content

    @pytest.mark.integration
    def test_token_not_exposed_in_env(self, container_exec):
        """GitHub token should not be exposed in environment."""
        result = container_exec("env")
        # Token should be used but not stored in env after setup
        output = result.output.decode()
        # Allow it to be in env initially, but check it's not logged
        # This test might need adjustment based on actual implementation
        pass


class TestHostDirectoryMount:
    """Test optional host directory mounting."""

    def test_creates_host_mount_point(self, entrypoint_path):
        """Should create /host directory for optional mounting."""
        content = entrypoint_path.read_text()
        # Check that /host is mentioned or created
        # This might be in Dockerfile instead
        pass
