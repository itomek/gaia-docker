"""Tests for GitHub Actions workflow structure and logic."""

import yaml
import pytest
import re
from pathlib import Path


class TestWorkflowFileStructure:
    """Test GitHub Actions workflow file exists and is valid."""

    def test_workflow_file_exists(self, project_root):
        """Workflow file must exist at .github/workflows/publish.yml."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        assert workflow_file.exists(), "publish.yml workflow file not found"

    def test_workflow_is_valid_yaml(self, project_root):
        """Workflow file must contain valid YAML."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        try:
            with open(workflow_file) as f:
                yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"publish.yml is not valid YAML: {e}")

    def test_workflow_has_name(self, project_root):
        """Workflow must have a name."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)
        assert "name" in workflow, "Workflow missing 'name' field"
        assert workflow["name"], "Workflow name is empty"


class TestWorkflowTriggers:
    """Test workflow trigger configuration."""

    def test_triggers_on_push_to_main(self, project_root):
        """Workflow should trigger on push to main branch."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        # YAML parses 'on' as True (boolean)
        triggers = workflow.get("on") or workflow.get(True)
        assert triggers, "Workflow missing triggers"
        assert "push" in triggers, "Workflow missing 'push' trigger"
        assert "branches" in triggers["push"], "Push trigger missing 'branches'"
        assert "main" in triggers["push"]["branches"], "Workflow not configured for main branch"

    def test_triggers_on_pull_request(self, project_root):
        """Workflow should trigger on pull requests to main."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        triggers = workflow.get("on") or workflow.get(True)
        assert "pull_request" in triggers, "Workflow missing 'pull_request' trigger"

    def test_has_manual_trigger(self, project_root):
        """Workflow should support manual triggering."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        triggers = workflow.get("on") or workflow.get(True)
        assert "workflow_dispatch" in triggers, "Workflow missing 'workflow_dispatch' for manual triggering"


class TestWorkflowJobs:
    """Test workflow job structure and dependencies."""

    def test_has_test_job(self, project_root):
        """Workflow must have a test job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "jobs" in workflow, "Workflow missing 'jobs'"
        assert "test" in workflow["jobs"], "Workflow missing 'test' job"

    def test_has_build_and_push_job(self, project_root):
        """Workflow must have a build-and-push job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "build-and-push" in workflow["jobs"], "Workflow missing 'build-and-push' job"

    def test_has_build_dev_job(self, project_root):
        """Workflow must have a build-dev job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "build-dev" in workflow["jobs"], "Workflow missing 'build-dev' job"

    def test_build_and_push_depends_on_test(self, project_root):
        """build-and-push job should depend on test job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_job = workflow["jobs"]["build-and-push"]
        assert "needs" in build_job, "build-and-push missing 'needs' dependency"
        assert "test" in build_job["needs"], "build-and-push should depend on test"

    def test_build_dev_depends_on_test(self, project_root):
        """build-dev job should depend on test job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_dev_job = workflow["jobs"]["build-dev"]
        assert "needs" in build_dev_job, "build-dev missing 'needs' dependency"
        assert "test" in build_dev_job["needs"], "build-dev should depend on test"

    def test_build_jobs_only_run_on_main(self, project_root):
        """Build jobs should only run on main branch pushes."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        for job_name in ["build-and-push", "build-dev"]:
            job = workflow["jobs"][job_name]
            assert "if" in job, f"{job_name} missing conditional execution"
            assert "github.ref == 'refs/heads/main'" in job["if"], \
                f"{job_name} should only run on main branch"


class TestVersionReading:
    """Test VERSION.json reading logic in workflow."""

    def test_build_and_push_reads_version_file(self, project_root):
        """build-and-push job should read VERSION.json file."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        # Check for VERSION.json reading in build-and-push job
        assert 'VERSION.json' in content, "Workflow doesn't reference VERSION.json"
        assert 'jq -r' in content, "Workflow doesn't use jq to parse VERSION.json"

    def test_build_and_push_reads_gaia_linux_version(self, project_root):
        """build-and-push should extract gaia-linux version."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert '"gaia-linux"' in content, "Workflow doesn't read gaia-linux version"

    def test_build_dev_reads_gaia_dev_version(self, project_root):
        """build-dev should extract gaia-dev version."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert '"gaia-dev"' in content, "Workflow doesn't read gaia-dev version"

    def test_version_reading_has_error_handling(self, project_root):
        """Version reading should have error handling for null/empty values."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        # Should check for empty or null version
        assert '"null"' in content or 'null' in content, "Workflow doesn't check for null version"
        assert 'ERROR' in content or 'error' in content or 'exit 1' in content, \
            "Workflow doesn't handle version read errors"

    def test_version_output_set_for_build_and_push(self, project_root):
        """build-and-push should output version for downstream jobs."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_job = workflow["jobs"]["build-and-push"]
        assert "outputs" in build_job, "build-and-push missing outputs"
        assert "version" in build_job["outputs"], "build-and-push not outputting version"

    def test_version_output_set_for_build_dev(self, project_root):
        """build-dev should output version for downstream jobs."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_dev_job = workflow["jobs"]["build-dev"]
        assert "outputs" in build_dev_job, "build-dev missing outputs"
        assert "version" in build_dev_job["outputs"], "build-dev not outputting version"


class TestBuildArguments:
    """Test GAIA_VERSION build argument passing."""

    def test_build_and_push_does_not_pass_gaia_version_arg(self, project_root):
        """build-and-push should NOT pass GAIA_VERSION build argument (decoupled)."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_job = workflow["jobs"]["build-and-push"]
        steps = build_job.get("steps", [])
        for step in steps:
            if step.get("uses", "").startswith("docker/build-push-action"):
                build_args = step.get("with", {}).get("build-args", "")
                assert "GAIA_VERSION" not in build_args, \
                    "build-and-push should not pass GAIA_VERSION (image versioning is decoupled)"
                break

    def test_build_dev_passes_gaia_version_arg(self, project_root):
        """build-dev should still pass GAIA_VERSION build argument."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_dev_job = workflow["jobs"]["build-dev"]
        steps = build_dev_job.get("steps", [])
        found = False
        for step in steps:
            if step.get("uses", "").startswith("docker/build-push-action"):
                build_args = step.get("with", {}).get("build-args", "")
                if "GAIA_VERSION" in build_args:
                    found = True
                break
        assert found, "build-dev should pass GAIA_VERSION build arg"


class TestDockerOperations:
    """Test Docker build and push configuration."""

    def test_uses_docker_buildx(self, project_root):
        """Workflow should use Docker Buildx for multi-arch builds."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'docker/setup-buildx-action' in content, "Workflow doesn't setup Docker Buildx"

    def test_supports_multi_arch_builds(self, project_root):
        """Workflow should build for multiple architectures."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'linux/amd64' in content, "Workflow missing amd64 platform"
        assert 'linux/arm64' in content, "Workflow missing arm64 platform"

    def test_uses_github_actions_cache(self, project_root):
        """Workflow should use GitHub Actions cache for Docker layers."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'cache-from: type=gha' in content, "Workflow missing cache-from configuration"
        assert 'cache-to: type=gha' in content, "Workflow missing cache-to configuration"

    def test_build_and_push_has_skip_if_exists(self, project_root):
        """build-and-push should skip building if the tag already exists on Docker Hub."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'docker manifest inspect' in content, \
            "Workflow should check if image tag already exists before building"

    def test_build_dev_has_skip_if_exists(self, project_root):
        """build-dev should skip building if the tag already exists on Docker Hub."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        build_dev_job = workflow["jobs"]["build-dev"]
        steps = build_dev_job.get("steps", [])

        # Find the check_exists step
        has_manifest_check = any(
            "docker manifest inspect" in step.get("run", "")
            for step in steps
        )
        assert has_manifest_check, \
            "build-dev should check if image tag already exists before building"

        # Verify build step is conditional on check_exists
        has_conditional_build = any(
            "check_exists" in step.get("if", "")
            for step in steps
            if step.get("uses", "").startswith("docker/build-push-action")
        )
        assert has_conditional_build, \
            "build-dev build step should be conditional on check_exists"


class TestReleaseCreation:
    """Test GitHub release creation logic."""

    def test_has_create_release_job(self, project_root):
        """Workflow should have create-release job."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "create-release" in workflow["jobs"], "Workflow missing 'create-release' job"

    def test_create_release_depends_on_builds(self, project_root):
        """create-release should depend on both build jobs."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        release_job = workflow["jobs"]["create-release"]
        assert "needs" in release_job, "create-release missing dependencies"
        needs = release_job["needs"]
        assert "build-and-push" in needs, "create-release should depend on build-and-push"
        assert "build-dev" in needs, "create-release should depend on build-dev"

    def test_release_uses_gh_cli(self, project_root):
        """Release creation should use GitHub CLI."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'gh release create' in content, "Workflow doesn't use 'gh release create'"

    def test_release_tag_has_v_prefix(self, project_root):
        """Release tags should have 'v' prefix (e.g., v1.0.0)."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        # Look for version tag pattern with v prefix
        assert re.search(r'v\$\{?\{?.*version', content), \
            "Release tag should have 'v' prefix"


class TestWorkflowPermissions:
    """Test workflow permissions configuration."""

    def test_has_contents_write_permission(self, project_root):
        """Workflow needs contents:write permission for releases."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "permissions" in workflow, "Workflow missing permissions"
        assert "contents" in workflow["permissions"], "Workflow missing contents permission"
        assert workflow["permissions"]["contents"] == "write", \
            "Workflow needs contents:write permission for creating releases"


class TestWorkflowSecrets:
    """Test required secrets are documented/used."""

    def test_uses_dockerhub_username_secret(self, project_root):
        """Workflow should use DOCKERHUB_USERNAME secret."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'DOCKERHUB_USERNAME' in content, "Workflow doesn't use DOCKERHUB_USERNAME secret"

    def test_uses_dockerhub_token_secret(self, project_root):
        """Workflow should use DOCKERHUB_TOKEN secret."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'DOCKERHUB_TOKEN' in content, "Workflow doesn't use DOCKERHUB_TOKEN secret"

    def test_uses_github_token(self, project_root):
        """Workflow should use GITHUB_TOKEN for releases."""
        workflow_file = project_root / ".github" / "workflows" / "publish.yml"
        content = workflow_file.read_text()

        assert 'GITHUB_TOKEN' in content or 'github.token' in content, \
            "Workflow doesn't use GITHUB_TOKEN for releases"
