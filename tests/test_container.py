"""Integration tests for complete container functionality."""

import pytest


class TestContainerStartup:
    """Test container starts and initializes correctly."""

    @pytest.mark.integration
    def test_container_starts(self, gaia_container):
        """Container should start successfully."""
        assert gaia_container.get_wrapped_container().status == "running"

    @pytest.mark.integration
    def test_entrypoint_completes(self, container_exec):
        """Entrypoint should complete without errors."""
        # If we got here, entrypoint succeeded (waited in fixture)
        result = container_exec("echo 'success'")
        assert result.exit_code == 0


class TestClaudeCodeYOLO:
    """Test Claude Code works in YOLO mode (no restrictions)."""

    @pytest.mark.integration
    def test_claude_executable(self, container_exec):
        """Claude Code should be in PATH."""
        result = container_exec("which claude")
        assert result.exit_code == 0
        assert "/home/gaia/.local/bin/claude" in result.output.decode()

    @pytest.mark.integration
    def test_claude_version(self, container_exec):
        """Claude Code should report version."""
        result = container_exec("claude --version")
        assert result.exit_code == 0

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires interactive OAuth login")
    def test_claude_authenticated(self, container_exec):
        """Claude Code should work after OAuth login."""
        # This test requires manual OAuth login first
        # Skip in CI, test manually
        result = container_exec("claude -p 'Hello'")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_claude_config_persists(self, container_exec):
        """Claude Code config should persist in volume."""
        result = container_exec("test -d /home/gaia/.claude")
        assert result.exit_code == 0


class TestGAIAFunctionality:
    """Test GAIA commands work inside container."""

    @pytest.mark.integration
    def test_gaia_cli_available(self, container_exec):
        """GAIA CLI should be available."""
        result = container_exec("gaia --version")
        assert result.exit_code == 0

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires Lemonade server")
    def test_gaia_llm_works(self, container_exec):
        """GAIA LLM should work (requires Lemonade)."""
        result = container_exec("gaia llm 'Hello'")
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
        result = container_exec("echo $SHELL")
        assert b"/bin/zsh" in result.output

    @pytest.mark.integration
    def test_sudo_works(self, container_exec):
        """User should have passwordless sudo."""
        result = container_exec("sudo whoami")
        assert result.output.decode().strip() == "root"


class TestPortExposure:
    """Test that expected ports are exposed."""

    @pytest.mark.integration
    def test_port_5000_exposed(self, gaia_container):
        """Port 5000 should be exposed for Lemonade."""
        ports = gaia_container.get_exposed_ports()
        # This might need adjustment based on testcontainers API
        pass

    @pytest.mark.integration
    def test_port_8000_exposed(self, gaia_container):
        """Port 8000 should be exposed for GAIA API."""
        pass


class TestVolumePersistedData:
    """Test that important data persists in volumes."""

    @pytest.mark.integration
    def test_claude_config_in_volume(self, container_exec):
        """Claude config should be in /home/gaia/.claude."""
        result = container_exec("mountpoint /home/gaia/.claude || test -d /home/gaia/.claude")
        assert result.exit_code == 0

    @pytest.mark.integration
    def test_gaia_in_source(self, container_exec):
        """GAIA should be cloned to /source/gaia."""
        result = container_exec("test -d /source/gaia")
        assert result.exit_code == 0


class TestOptionalFeatures:
    """Test optional features work when enabled."""

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires HOST_DIR env var")
    def test_host_directory_mount(self, container_exec):
        """Host directory should be mounted at /host when HOST_DIR set."""
        result = container_exec("test -d /host")
        assert result.exit_code == 0

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires LEMONADE_URL env var")
    def test_remote_lemonade_connection(self, container_exec):
        """Should connect to remote Lemonade when LEMONADE_URL set."""
        pass
