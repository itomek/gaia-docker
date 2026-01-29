"""Tests for gaia-dev entrypoint.sh script functionality."""

import pytest
import subprocess


class TestEntrypointDevScript:
    """Test gaia-dev entrypoint.sh script exists and is executable."""

    def test_entrypoint_dev_exists(self, entrypoint_dev_path):
        """gaia-dev/entrypoint.sh must exist."""
        assert entrypoint_dev_path.exists(), "gaia-dev/entrypoint.sh not found"

    def test_entrypoint_dev_executable(self, entrypoint_dev_path):
        """gaia-dev/entrypoint.sh must be executable."""
        assert entrypoint_dev_path.stat().st_mode & 0o111, "gaia-dev/entrypoint.sh not executable"

    def test_entrypoint_dev_has_shebang(self, entrypoint_dev_path):
        """gaia-dev/entrypoint.sh must have proper shebang."""
        content = entrypoint_dev_path.read_text()
        assert content.startswith("#!/bin/bash")

    def test_entrypoint_dev_uses_set_e(self, entrypoint_dev_path):
        """gaia-dev/entrypoint.sh should fail fast on errors."""
        content = entrypoint_dev_path.read_text()
        assert "set -e" in content


class TestEnvironmentConfiguration:
    """Test environment variable handling in gaia-dev entrypoint.sh."""

    def test_requires_lemonade_base_url_env(self, entrypoint_dev_path):
        """Should require LEMONADE_BASE_URL environment variable."""
        content = entrypoint_dev_path.read_text()
        assert 'if [ -z "$LEMONADE_BASE_URL" ]' in content
        assert 'ERROR: LEMONADE_BASE_URL environment variable is required' in content

    def test_handles_github_token(self, entrypoint_dev_path):
        """Should handle GITHUB_TOKEN for GitHub CLI configuration."""
        content = entrypoint_dev_path.read_text()
        assert 'GITHUB_TOKEN' in content
        assert 'gh auth login' in content

    def test_handles_anthropic_api_key(self, entrypoint_dev_path):
        """Should handle ANTHROPIC_API_KEY for Claude Code."""
        content = entrypoint_dev_path.read_text()
        assert 'ANTHROPIC_API_KEY' in content

    def test_handles_gaia_repo_url(self, entrypoint_dev_path):
        """Should support custom GAIA_REPO_URL for forks."""
        content = entrypoint_dev_path.read_text()
        assert 'GAIA_REPO_URL' in content
        assert 'https://github.com/amd/gaia.git' in content  # default

    def test_uses_token_for_authenticated_clone(self, entrypoint_dev_path):
        """Should use GITHUB_TOKEN for authenticated cloning."""
        content = entrypoint_dev_path.read_text()
        assert 'GITHUB_TOKEN' in content
        assert 'git clone' in content

    def test_adds_upstream_remote_for_forks(self, entrypoint_dev_path):
        """Should add upstream remote pointing to main GAIA repo."""
        content = entrypoint_dev_path.read_text()
        assert 'git remote add upstream' in content
        assert 'https://github.com/amd/gaia.git' in content

    def test_handles_skip_gaia_clone(self, entrypoint_dev_path):
        """Should support SKIP_GAIA_CLONE to skip cloning."""
        content = entrypoint_dev_path.read_text()
        assert 'SKIP_GAIA_CLONE' in content
        assert 'Skipping GAIA clone' in content

    def test_entrypoint_activates_venv(self, entrypoint_dev_path):
        """Entrypoint should activate virtual environment."""
        content = entrypoint_dev_path.read_text()
        assert 'source /home/gaia/.venv/bin/activate' in content

    def test_shows_setup_instructions(self, entrypoint_dev_path):
        """Entrypoint should show first-time setup instructions."""
        content = entrypoint_dev_path.read_text()
        assert 'First-time setup' in content
        assert 'uv pip install' in content  # in instructions, not exec

    def test_no_auto_install(self, entrypoint_dev_path):
        """Should NOT auto-install GAIA packages (user does this manually)."""
        content = entrypoint_dev_path.read_text()
        # Should NOT have the old auto-install code
        assert 'echo "Installing GAIA dependencies..."' not in content
        # Instructions are okay, but not actual execution
        lines = content.split('\n')
        for line in lines:
            if 'uv pip install -e' in line:
                # If found, should be in echo statement (instructions), not actual command
                assert line.strip().startswith('echo')


class TestLemonadeBaseUrlValidation:
    """Test LEMONADE_BASE_URL validation at runtime."""

    @pytest.mark.integration
    def test_dev_container_fails_without_lemonade_url(self, project_root):
        """Dev container should fail to start without LEMONADE_BASE_URL."""
        result = subprocess.run(
            ["docker", "run", "--rm", "gaia-dev:test", "echo", "test"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode != 0
        assert "ERROR: LEMONADE_BASE_URL environment variable is required" in result.stderr or \
               "ERROR: LEMONADE_BASE_URL environment variable is required" in result.stdout

    @pytest.mark.integration
    def test_dev_container_starts_with_lemonade_url(self, project_root):
        """Dev container should start successfully with LEMONADE_BASE_URL."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://localhost:5000/api/v1",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "success"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0

    @pytest.mark.integration
    def test_skip_gaia_clone_actually_skips(self, project_root):
        """SKIP_GAIA_CLONE=true should skip cloning GAIA repository."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://localhost:5000/api/v1",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "done"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        assert result.returncode == 0
        assert "Skipping GAIA clone" in output
        assert "Cloning GAIA from:" not in output


class TestGitHubCLIConfiguration:
    """Test GitHub CLI configuration."""

    @pytest.mark.integration
    def test_github_cli_configured_with_token(self, project_root):
        """GitHub CLI should be configured when GITHUB_TOKEN is provided."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "GITHUB_TOKEN=ghp_test_token_invalid",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "started"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Container should start (token validation happens at gh usage time)
        assert result.returncode == 0

    @pytest.mark.integration
    def test_github_cli_message_without_token(self, project_root):
        """Should show message about GitHub CLI when no token provided."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "done"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        assert "gh auth login" in output


class TestClaudeCodeConfiguration:
    """Test Claude Code configuration."""

    @pytest.mark.integration
    def test_claude_code_message_with_api_key(self, project_root):
        """Should show message when ANTHROPIC_API_KEY is provided."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "ANTHROPIC_API_KEY=sk-ant-test",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "done"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        assert "ANTHROPIC_API_KEY detected" in output

    @pytest.mark.integration
    def test_claude_code_message_without_api_key(self, project_root):
        """Should show interactive login message when no API key provided."""
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test", "echo", "done"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        assert "authenticate interactively" in output or "ANTHROPIC_API_KEY not set" in output
