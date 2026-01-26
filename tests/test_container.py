"""Integration tests for complete container functionality."""

import pytest


class TestContainerStartup:
    """Test container starts and initializes correctly."""

    @pytest.mark.integration
    def test_container_starts(self, gaia_container):
        """Container should start successfully."""
        container = gaia_container.get_wrapped_container()
        container.reload()
        assert container.status == "running"

    @pytest.mark.integration
    def test_entrypoint_completes(self, container_exec):
        """Entrypoint should complete without errors."""
        # If we got here, entrypoint succeeded (waited in fixture)
        result = container_exec("echo 'success'")
        assert result.exit_code == 0


class TestGAIAFunctionality:
    """Test GAIA commands work inside container."""

    @pytest.mark.integration
    def test_gaia_cli_available(self, container_exec):
        """GAIA CLI should be available."""
        result = container_exec("gaia --version")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_gaia_help_works(self, container_exec):
        """GAIA help should work."""
        result = container_exec("gaia --help")
        assert result.exit_code == 0
        assert b"GAIA" in result.output


class TestDockerExecAccess:
    """Test docker exec access works correctly."""

    @pytest.mark.integration
    def test_exec_as_gaia_user(self, container_exec):
        """Docker exec should run as gaia user."""
        result = container_exec("whoami")
        assert result.output.decode().strip() == "gaia"

    @pytest.mark.integration
    def test_exec_with_zsh(self, container_exec):
        """Docker exec should use zsh shell."""
        result = container_exec("sh -c 'echo $SHELL'")
        assert b"/bin/zsh" in result.output

    @pytest.mark.integration
    def test_sudo_works(self, container_exec):
        """User should have passwordless sudo."""
        result = container_exec("sudo whoami")
        assert result.output.decode().strip() == "root"


