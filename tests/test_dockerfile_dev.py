"""Tests for Dockerfile.dev build and development container requirements."""

import pytest
import subprocess


class TestDockerfileDevBuild:
    """Test that Dockerfile.dev builds successfully and contains required components."""

    def test_dockerfile_dev_exists(self, dockerfile_dev_path):
        """Dockerfile.dev must exist."""
        assert dockerfile_dev_path.exists(), "Dockerfile.dev not found"

    def test_dockerfile_dev_builds(self, project_root):
        """Dockerfile must build without errors."""
        result = subprocess.run(
            ["docker", "build", "-t", "gaia-dev:test", "-f", "gaia-dev/Dockerfile", str(project_root)],
            capture_output=True,
            text=True,
            timeout=900
        )
        assert result.returncode == 0, f"Docker build failed: {result.stderr}"

    def test_python_version(self, project_root):
        """Container must have Python 3.12."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "python", "--version"],
            capture_output=True,
            text=True
        )
        assert "Python 3.12" in result.stdout

    def test_nodejs_installed(self, project_root):
        """Container must have Node.js 20."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "node", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        last_line = result.stdout.strip().splitlines()[-1]
        assert last_line.startswith("v20.")

    def test_claude_code_installed(self, project_root):
        """Container must have Claude Code installed."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "claude", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_github_cli_installed(self, project_root):
        """Container must have GitHub CLI installed."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "gh", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "gh version" in result.stdout

    def test_uv_installed(self, project_root):
        """Container must have uv (fast Python package installer)."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "uv", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "uv" in result.stdout.lower()

    def test_git_installed(self, project_root):
        """Container must have git."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "git", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "git version" in result.stdout

    def test_zsh_installed(self, project_root):
        """Container must have zsh as shell."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "zsh", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "zsh" in result.stdout.lower()

    def test_gaia_user_exists(self, project_root):
        """Container must have 'gaia' user."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "whoami"],
            capture_output=True,
            text=True
        )
        last_line = result.stdout.strip().splitlines()[-1]
        assert last_line == "gaia"


class TestGaiaSourceCode:
    """Test GAIA source code cloning and dependencies."""

    def test_gaia_directory_exists(self, project_root):
        """GAIA directory must exist for volume mount."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "--entrypoint", "",
             "gaia-dev:test", "ls", "-d", "/home/gaia/gaia"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_entrypoint_clones_gaia(self, entrypoint_dev_path):
        """Entrypoint should clone GAIA if not present."""
        content = entrypoint_dev_path.read_text()
        assert "git clone" in content
        assert "github.com/amd/gaia" in content

    def test_entrypoint_shows_setup_instructions(self, entrypoint_dev_path):
        """Entrypoint should show setup instructions (not auto-install)."""
        content = entrypoint_dev_path.read_text()
        assert "First-time setup" in content
        assert "uv pip install" in content

    @pytest.mark.integration
    def test_gaia_cloned_on_first_run(self, project_root):
        """GAIA must be cloned on first run."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "gaia-dev:test", "ls", "-d", "/home/gaia/gaia/.git"],
            capture_output=True,
            text=True,
            timeout=600
        )
        assert result.returncode == 0


class TestDockerfileDevOptimization:
    """Test that Dockerfile.dev follows best practices."""

    def test_uses_ubuntu_base(self, dockerfile_dev_path):
        """Should use ubuntu:24.04 as base image."""
        content = dockerfile_dev_path.read_text()
        assert "ubuntu:24.04" in content

    def test_uses_uv_managed_python(self, dockerfile_dev_path):
        """Should use uv to install Python instead of system packages."""
        content = dockerfile_dev_path.read_text()
        assert "uv python install" in content

    def test_cleans_apt_cache(self, dockerfile_dev_path):
        """Should clean apt cache to reduce image size."""
        content = dockerfile_dev_path.read_text()
        assert "apt-get clean" in content
        assert "rm -rf /var/lib/apt/lists/*" in content

    def test_creates_gaia_directory(self, dockerfile_dev_path):
        """Should create gaia directory for volume mount."""
        content = dockerfile_dev_path.read_text()
        assert "mkdir -p /home/$USERNAME/gaia" in content

    def test_includes_sandbox_packages(self, dockerfile_dev_path):
        """Should include Claude Code sandbox requirements."""
        content = dockerfile_dev_path.read_text()
        assert "iptables" in content
        assert "ipset" in content
        assert "iproute2" in content

    def test_venv_activation_in_zshrc(self, dockerfile_dev_path):
        """Dockerfile should add venv activation to .zshrc."""
        content = dockerfile_dev_path.read_text()
        assert 'source /home/gaia/.venv/bin/activate' in content
        assert '.zshrc' in content
