"""Tests for VERSION.json file format and parsing."""

import json
import subprocess
import pytest
from pathlib import Path


class TestVersionFileFormat:
    """Test VERSION.json file structure and content."""

    def test_version_file_exists(self, project_root):
        """VERSION.json must exist at repository root."""
        version_file = project_root / "VERSION.json"
        assert version_file.exists(), "VERSION.json file not found at repository root"

    def test_version_file_is_valid_json(self, project_root):
        """VERSION.json must contain valid JSON."""
        version_file = project_root / "VERSION.json"
        try:
            with open(version_file) as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"VERSION.json is not valid JSON: {e}")

    def test_version_file_has_gaia_linux_key(self, project_root):
        """VERSION.json must contain 'gaia-linux' key."""
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            data = json.load(f)
        assert "gaia-linux" in data, "VERSION.json missing 'gaia-linux' key"

    def test_version_file_has_gaia_dev_key(self, project_root):
        """VERSION.json must contain 'gaia-dev' key."""
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            data = json.load(f)
        assert "gaia-dev" in data, "VERSION.json missing 'gaia-dev' key"

    def test_gaia_linux_version_not_empty(self, project_root):
        """gaia-linux version must not be empty."""
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            data = json.load(f)
        version = data.get("gaia-linux")
        assert version, "gaia-linux version is empty"
        assert isinstance(version, str), "gaia-linux version must be a string"

    def test_gaia_dev_version_not_empty(self, project_root):
        """gaia-dev version must not be empty."""
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            data = json.load(f)
        version = data.get("gaia-dev")
        assert version, "gaia-dev version is empty"
        assert isinstance(version, str), "gaia-dev version must be a string"

    def test_versions_follow_semver_format(self, project_root):
        """Both versions should follow semantic versioning format (X.Y.Z)."""
        version_file = project_root / "VERSION.json"
        with open(version_file) as f:
            data = json.load(f)

        for key in ["gaia-linux", "gaia-dev"]:
            version = data[key]
            parts = version.split(".")
            assert len(parts) >= 3, f"{key} version '{version}' must have at least 3 parts (MAJOR.MINOR.PATCH[.HOTFIX])"
            for part in parts:
                assert part.isdigit(), f"{key} version '{version}' part '{part}' must be numeric"


class TestVersionFileJqParsing:
    """Test jq parsing of VERSION.json (as used in CI)."""

    def test_jq_can_read_gaia_linux_version(self, project_root):
        """jq should successfully read gaia-linux version."""
        version_file = project_root / "VERSION.json"
        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(version_file)],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        assert version, "jq returned empty version for gaia-linux"
        assert version != "null", "jq returned null for gaia-linux"

    def test_jq_can_read_gaia_dev_version(self, project_root):
        """jq should successfully read gaia-dev version."""
        version_file = project_root / "VERSION.json"
        result = subprocess.run(
            ["jq", "-r", '."gaia-dev"', str(version_file)],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        assert version, "jq returned empty version for gaia-dev"
        assert version != "null", "jq returned null for gaia-dev"

    def test_jq_returns_null_for_missing_key(self, project_root):
        """jq should return 'null' for non-existent keys."""
        version_file = project_root / "VERSION.json"
        result = subprocess.run(
            ["jq", "-r", '."non-existent-key"', str(version_file)],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert output == "null", f"jq should return 'null' for missing key, got: {output}"

    def test_ci_version_extraction_logic_gaia_linux(self, project_root):
        """Test the exact CI logic for extracting gaia-linux version."""
        version_file = project_root / "VERSION.json"

        # Simulate CI logic
        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(version_file)],
            capture_output=True,
            text=True
        )
        version = result.stdout.strip()

        # Verify CI validation logic
        assert result.returncode == 0, "jq command failed"
        assert version, "VERSION is empty"
        assert version != "null", "VERSION is null"

    def test_ci_version_extraction_logic_gaia_dev(self, project_root):
        """Test the exact CI logic for extracting gaia-dev version."""
        version_file = project_root / "VERSION.json"

        # Simulate CI logic
        result = subprocess.run(
            ["jq", "-r", '."gaia-dev"', str(version_file)],
            capture_output=True,
            text=True
        )
        version = result.stdout.strip()

        # Verify CI validation logic
        assert result.returncode == 0, "jq command failed"
        assert version, "VERSION is empty"
        assert version != "null", "VERSION is null"


class TestVersionFileMalformedHandling:
    """Test handling of malformed VERSION.json files."""

    def test_detect_invalid_json(self, tmp_path):
        """Should detect when VERSION.json contains invalid JSON."""
        invalid_json_file = tmp_path / "VERSION.json"
        invalid_json_file.write_text('{"gaia-linux": "1.0.0"')  # Missing closing brace

        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(invalid_json_file)],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0, "jq should fail on invalid JSON"

    def test_detect_missing_key(self, tmp_path):
        """Should detect when required key is missing."""
        missing_key_file = tmp_path / "VERSION.json"
        missing_key_file.write_text('{"other-key": "1.0.0"}')

        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(missing_key_file)],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        assert version == "null", "jq should return 'null' for missing key"

    def test_detect_empty_value(self, tmp_path):
        """Should detect when version value is empty string."""
        empty_value_file = tmp_path / "VERSION.json"
        empty_value_file.write_text('{"gaia-linux": ""}')

        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(empty_value_file)],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        # Empty string is valid JSON but should be caught by CI validation
        assert version == "", "jq should return empty string for empty value"


class TestVersionFileBackwardsCompatibility:
    """Test VERSION.json format is future-proof."""

    def test_can_add_new_container_types(self, tmp_path):
        """VERSION.json should support adding new container types."""
        extended_version_file = tmp_path / "VERSION.json"
        extended_version_file.write_text(json.dumps({
            "gaia-linux": "1.0.0",
            "gaia-dev": "1.1.0",
            "gaia-windows": "1.0.0",
            "gaia-arm": "1.0.0"
        }))

        # Should still be able to read existing keys
        result = subprocess.run(
            ["jq", "-r", '."gaia-linux"', str(extended_version_file)],
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "1.0.0"

        result = subprocess.run(
            ["jq", "-r", '."gaia-windows"', str(extended_version_file)],
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "1.0.0"
