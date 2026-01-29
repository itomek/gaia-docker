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

    def test_gaia_dev_dockerfile_declares_gaia_version_arg(self, dockerfile_dev_path):
        """gaia-dev Dockerfile must declare GAIA_VERSION build arg."""
        content = dockerfile_dev_path.read_text()
        assert 'ARG GAIA_VERSION' in content, "gaia-dev Dockerfile missing 'ARG GAIA_VERSION'"

    def test_gaia_dev_dockerfile_has_default_version(self, dockerfile_dev_path):
        """gaia-dev Dockerfile should have default GAIA_VERSION."""
        content = dockerfile_dev_path.read_text()
        # Look for ARG GAIA_VERSION=X.Y.Z
        assert re.search(r'ARG GAIA_VERSION=\d+\.\d+\.\d+', content), \
            "gaia-dev Dockerfile missing default version for GAIA_VERSION"

    def test_gaia_dev_dockerfile_exports_version_as_env(self, dockerfile_dev_path):
        """gaia-dev Dockerfile should export GAIA_VERSION as environment variable."""
        content = dockerfile_dev_path.read_text()
        assert 'ENV GAIA_VERSION' in content, "gaia-dev Dockerfile doesn't export GAIA_VERSION as ENV"


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

    def test_gaia_dev_entrypoint_uses_version_variable(self, entrypoint_dev_path):
        """gaia-dev entrypoint should reference GAIA_VERSION variable."""
        content = entrypoint_dev_path.read_text()
        assert 'GAIA_VERSION' in content, "gaia-dev entrypoint doesn't reference GAIA_VERSION"


class TestBuildArgPassing:
    """Test GAIA_VERSION can be passed at build time."""

    @pytest.mark.integration
    def test_can_override_gaia_linux_version_at_build_time(self, project_root):
        """Should be able to override GAIA_VERSION for gaia-linux via --build-arg."""
        # Try building with custom version
        result = subprocess.run(
            [
                "docker", "build",
                "-f", "gaia-linux/Dockerfile",
                "--build-arg", "GAIA_VERSION=99.99.99",
                "-t", "gaia-linux:test-version",
                "--target", "base",  # Build minimal stage to speed up test
                str(project_root)
            ],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Build should succeed (even though 99.99.99 doesn't exist on PyPI)
        # because we're only testing the build arg is accepted
        assert result.returncode == 0, f"Build failed: {result.stderr}"

    @pytest.mark.integration
    def test_can_override_gaia_dev_version_at_build_time(self, project_root):
        """Should be able to override GAIA_VERSION for gaia-dev via --build-arg."""
        # Try building with custom version
        result = subprocess.run(
            [
                "docker", "build",
                "-f", "gaia-dev/Dockerfile",
                "--build-arg", "GAIA_VERSION=99.99.99",
                "-t", "gaia-dev:test-version",
                str(project_root)
            ],
            capture_output=True,
            text=True,
            timeout=600
        )

        # Build should succeed
        assert result.returncode == 0, f"Build failed: {result.stderr}"


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

        # Check environment variable
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_INSTALL=true",
             "gaia-linux:test-env",
             "bash", "-c", "echo $GAIA_VERSION"],
            capture_output=True,
            text=True,
            timeout=30
        )

        version = result.stdout.strip()
        assert version, "GAIA_VERSION environment variable is empty"
        assert re.match(r'\d+\.\d+\.\d+', version), \
            f"GAIA_VERSION '{version}' doesn't match semver format"

    @pytest.mark.integration
    def test_gaia_dev_container_has_version_env_var(self, project_root):
        """gaia-dev container should have GAIA_VERSION environment variable."""
        # Build container
        subprocess.run(
            ["docker", "build", "-f", "gaia-dev/Dockerfile",
             "-t", "gaia-dev:test-env", str(project_root)],
            check=True,
            capture_output=True,
            timeout=900
        )

        # Check environment variable
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_GAIA_CLONE=true",
             "gaia-dev:test-env",
             "bash", "-c", "echo $GAIA_VERSION"],
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

        # Override at runtime
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-e", "LEMONADE_BASE_URL=http://test",
             "-e", "SKIP_INSTALL=true",
             "-e", "GAIA_VERSION=88.88.88",
             "gaia-linux:test-override",
             "bash", "-c", "echo $GAIA_VERSION"],
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


class TestBuildArgDocumentation:
    """Test build arguments are documented."""

    def test_gaia_linux_dockerfile_documents_version_arg(self, dockerfile_path):
        """gaia-linux Dockerfile should document GAIA_VERSION arg purpose."""
        content = dockerfile_path.read_text()
        lines = content.split('\n')

        # Find ARG GAIA_VERSION line
        arg_line_idx = None
        for i, line in enumerate(lines):
            if 'ARG GAIA_VERSION' in line:
                arg_line_idx = i
                break

        assert arg_line_idx is not None, "Could not find ARG GAIA_VERSION"

        # Check for comment near the ARG (within 2 lines before)
        has_comment = False
        for i in range(max(0, arg_line_idx - 2), arg_line_idx + 1):
            if lines[i].strip().startswith('#'):
                has_comment = True
                break

        assert has_comment, "GAIA_VERSION arg should have a comment explaining its purpose"

    def test_gaia_dev_dockerfile_documents_version_arg(self, dockerfile_dev_path):
        """gaia-dev Dockerfile should document GAIA_VERSION arg purpose."""
        content = dockerfile_dev_path.read_text()
        lines = content.split('\n')

        # Find ARG GAIA_VERSION line
        arg_line_idx = None
        for i, line in enumerate(lines):
            if 'ARG GAIA_VERSION' in line:
                arg_line_idx = i
                break

        assert arg_line_idx is not None, "Could not find ARG GAIA_VERSION"

        # Check for comment near the ARG (within 2 lines before)
        has_comment = False
        for i in range(max(0, arg_line_idx - 2), arg_line_idx + 1):
            if lines[i].strip().startswith('#'):
                has_comment = True
                break

        assert has_comment, "GAIA_VERSION arg should have a comment explaining its purpose"
