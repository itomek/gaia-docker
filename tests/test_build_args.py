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

    def test_gaia_linux_dockerfile_has_default_version(self, dockerfile_path):
        """gaia-linux Dockerfile should have default GAIA_VERSION."""
        content = dockerfile_path.read_text()
        # Look for ARG GAIA_VERSION=X.Y.Z
        assert re.search(r'ARG GAIA_VERSION=\d+\.\d+\.\d+', content), \
            "Dockerfile missing default version for GAIA_VERSION"

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

    def test_gaia_linux_entrypoint_has_version_default(self, entrypoint_path):
        """gaia-linux entrypoint should provide default for GAIA_VERSION."""
        content = entrypoint_path.read_text()
        # Look for ${GAIA_VERSION:-default}
        assert 'GAIA_VERSION="${GAIA_VERSION:-' in content, \
            "Entrypoint doesn't provide default for GAIA_VERSION"


class TestVersionEnvironmentVariable:
    """Test GAIA_VERSION is accessible inside running containers."""

    @pytest.mark.integration
    def test_gaia_linux_container_has_version_env_var(self, project_root):
        """gaia-linux container should have GAIA_VERSION environment variable."""
        # Build container
        subprocess.run(
            ["docker", "build", "-f", "gaia-linux/Dockerfile",
             "-t", "gaia-linux:test-env", str(project_root)],
            check=True,
            capture_output=True,
            timeout=600
        )

        # Check environment variable (use --entrypoint to bypass entrypoint output)
        result = subprocess.run(
            ["docker", "run", "--rm",
             "--entrypoint", "bash",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test-env",
             "-c", "echo $GAIA_VERSION"],
            capture_output=True,
            text=True,
            timeout=30
        )

        version = result.stdout.strip()
        assert version, "GAIA_VERSION environment variable is empty"
        assert re.match(r'\d+\.\d+\.\d+', version), \
            f"GAIA_VERSION '{version}' doesn't match semver format"

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


class TestVersionConsistency:
    """Test version consistency between Dockerfile, entrypoint, and VERSION.json."""

    def test_gaia_linux_default_matches_version_json(self, project_root, dockerfile_path):
        """gaia-linux Dockerfile default should match VERSION.json."""
        import json

        # Read VERSION.json
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            versions = json.load(f)
        expected_version = versions["gaia-linux"]

        # Read Dockerfile default
        content = dockerfile_path.read_text()
        match = re.search(r'ARG GAIA_VERSION=(\d+\.\d+\.\d+)', content)
        assert match, "Could not find GAIA_VERSION default in Dockerfile"
        dockerfile_version = match.group(1)

        assert dockerfile_version == expected_version, \
            f"Dockerfile default ({dockerfile_version}) doesn't match VERSION.json ({expected_version})"

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
        match = re.search(r'ARG GAIA_VERSION=(\d+\.\d+\.\d+)', content)
        assert match, "Could not find GAIA_VERSION default in gaia-dev Dockerfile"
        dockerfile_version = match.group(1)

        assert dockerfile_version == expected_version, \
            f"gaia-dev Dockerfile default ({dockerfile_version}) doesn't match VERSION.json ({expected_version})"
