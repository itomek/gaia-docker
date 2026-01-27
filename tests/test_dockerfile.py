"""Tests for Dockerfile build and base image requirements."""

import pytest
import subprocess


class TestDockerfileBuild:
    """Test that Dockerfile builds successfully and contains required components."""

    def test_dockerfile_exists(self, dockerfile_path):
        """Dockerfile must exist."""
        assert dockerfile_path.exists(), "Dockerfile not found"

    def test_dockerfile_builds(self, project_root):
        """Dockerfile must build without errors."""
        result = subprocess.run(
            ["docker", "build", "-t", "gaia-linux:test", str(project_root)],
            capture_output=True,
            text=True,
            timeout=600
        )
        assert result.returncode == 0, f"Docker build failed: {result.stderr}"

    def test_python_version(self, project_root):
        """Container must have Python 3.12."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "python", "--version"],
            capture_output=True,
            text=True
        )
        assert "Python 3.12" in result.stdout

    def test_nodejs_installed(self, project_root):
        """Container must have Node.js 20."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "node", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        last_line = result.stdout.strip().splitlines()[-1]
        assert last_line.startswith("v20.")

    def test_git_installed(self, project_root):
        """Container must have git."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "git", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "git version" in result.stdout

    def test_zsh_installed(self, project_root):
        """Container must have zsh as shell."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "zsh", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "zsh" in result.stdout.lower()

    def test_uv_installed(self, project_root):
        """Container must have uv (fast Python package installer)."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "uv", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "uv" in result.stdout.lower()

    def test_gaia_user_exists(self, project_root):
        """Container must have 'gaia' user."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "whoami"],
            capture_output=True,
            text=True
        )
        last_line = result.stdout.strip().splitlines()[-1]
        assert last_line == "gaia"

    def test_workspace_directory(self, project_root):
        """Container must have /source directory."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "ls", "-d", "/source"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0

    def test_ffmpeg_installed(self, project_root):
        """Container must have ffmpeg for audio processing."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-linux:test", "ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "ffmpeg version" in result.stdout


class TestDockerfileOptimization:
    """Test that Dockerfile follows best practices."""

    def test_uses_slim_base(self, dockerfile_path):
        """Should use python:3.12-slim for smaller image."""
        content = dockerfile_path.read_text()
        assert "python:3.12-slim" in content

    def test_cleans_apt_cache(self, dockerfile_path):
        """Should clean apt cache to reduce image size."""
        content = dockerfile_path.read_text()
        assert "apt-get clean" in content
        assert "rm -rf /var/lib/apt/lists/*" in content

    def test_combines_run_commands(self, dockerfile_path):
        """Should combine RUN commands to reduce layers."""
        content = dockerfile_path.read_text()
        lines = content.split('\n')
        run_lines = [l for l in lines if l.strip().startswith('RUN')]
        # Should have fewer than 10 RUN commands (combined efficiently)
        assert len(run_lines) < 10
