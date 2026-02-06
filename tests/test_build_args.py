"""Tests for GAIA_VERSION build argument handling."""

import pytest
import subprocess
import re


class TestDockerfileBuildArgs:
    """Test GAIA_VERSION build argument in Dockerfiles."""

    def test_gaia_linux_dockerfile_declares_gaia_version_arg(self, dockerfile_path):
        """gaia-linux Dockerfile must declare GAIA_VERSION build arg."""
        content = dockerfile_path.read_text()
        assert 'ARG GAIA_VERSION' in content, "Dockerfile missing 'ARG GAIA_VERSION'"

    def test_gaia_linux_dockerfile_has_no_default_version(self, dockerfile_path):
        """gaia-linux Dockerfile should NOT have a default GAIA_VERSION (decoupled)."""
        content = dockerfile_path.read_text()
        # ARG GAIA_VERSION should exist but without a default value
        assert not re.search(r'ARG GAIA_VERSION=\d', content), \
            "Dockerfile should not have a default GAIA_VERSION (image versioning is decoupled from GAIA)"

    def test_gaia_linux_dockerfile_exports_version_as_env(self, dockerfile_path):
        """gaia-linux Dockerfile should export GAIA_VERSION as environment variable."""
        content = dockerfile_path.read_text()
        assert 'ENV GAIA_VERSION' in content, "Dockerfile doesn't export GAIA_VERSION as ENV"


class TestEntrypointVersionUsage:
    """Test entrypoint scripts use GAIA_VERSION."""

    def test_gaia_linux_entrypoint_uses_version_variable(self, entrypoint_path):
        """gaia-linux entrypoint should reference GAIA_VERSION variable."""
        content = entrypoint_path.read_text()
        assert 'GAIA_VERSION' in content, "Entrypoint doesn't reference GAIA_VERSION"

    def test_gaia_linux_entrypoint_handles_missing_version(self, entrypoint_path):
        """gaia-linux entrypoint should handle missing GAIA_VERSION (installs latest)."""
        content = entrypoint_path.read_text()
        assert 'installing latest from PyPI' in content.lower() or 'No GAIA_VERSION specified' in content, \
            "Entrypoint doesn't handle missing GAIA_VERSION"

    def test_gaia_linux_entrypoint_handles_specific_version(self, entrypoint_path):
        """gaia-linux entrypoint should install specific version when GAIA_VERSION is set."""
        content = entrypoint_path.read_text()
        assert '==${GAIA_VERSION}' in content, \
            "Entrypoint doesn't pin to specific GAIA_VERSION when set"


class TestVersionEnvironmentVariable:
    """Test GAIA_VERSION is accessible inside running containers."""

    @pytest.mark.integration
    def test_can_override_version_env_at_runtime(self, project_root):
        """Should be able to override GAIA_VERSION at container runtime."""
        # Build container
        subprocess.run(
            ["docker", "build", "-f", "gaia-linux/Dockerfile",
             "-t", "gaia-linux:test-override", str(project_root)],
            check=True,
            capture_output=True,
            timeout=600
        )

        # Override at runtime (use --entrypoint to bypass entrypoint output)
        result = subprocess.run(
            ["docker", "run", "--rm",
             "--entrypoint", "bash",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_INSTALL=true",
             "-e", "GAIA_VERSION=88.88.88",
             "gaia-linux:test-override",
             "-c", "echo $GAIA_VERSION"],
            capture_output=True,
            text=True,
            timeout=30
        )

        version = result.stdout.strip()
        assert version == "88.88.88", \
            f"Runtime GAIA_VERSION override failed, got: {version}"

    @pytest.mark.integration
    def test_gaia_version_empty_when_not_set(self, project_root):
        """GAIA_VERSION should be empty when not set at build or runtime."""
        # Build container without GAIA_VERSION build arg
        subprocess.run(
            ["docker", "build", "-f", "gaia-linux/Dockerfile",
             "-t", "gaia-linux:test-no-ver", str(project_root)],
            check=True,
            capture_output=True,
            timeout=600
        )

        result = subprocess.run(
            ["docker", "run", "--rm",
             "--entrypoint", "bash",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test-no-ver",
             "-c", "echo \"GAIA_VERSION=${GAIA_VERSION}\""],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip()
        assert output == "GAIA_VERSION=", \
            f"GAIA_VERSION should be empty when not set, got: {output}"


class TestVersionConsistency:
    """Test version consistency between Dockerfile, entrypoint, and VERSION.json."""

    def test_gaia_dev_default_matches_version_json(self, project_root, dockerfile_dev_path):
        """gaia-dev Dockerfile default should match VERSION.json."""
        import json

        # Read VERSION.json
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            versions = json.load(f)
        expected_version = versions["gaia-dev"]

        # Read Dockerfile default
        content = dockerfile_dev_path.read_text()
        match = re.search(r'ARG GAIA_VERSION=(\d+\.\d+\.\d+(?:\.\d+)?)', content)
        assert match, "Could not find GAIA_VERSION default in gaia-dev Dockerfile"
        dockerfile_version = match.group(1)

        assert dockerfile_version == expected_version, \
            f"gaia-dev Dockerfile default ({dockerfile_version}) doesn't match VERSION.json ({expected_version})"
