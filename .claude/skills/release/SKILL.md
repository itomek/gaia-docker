<release-skill>
# Release Skill

Manage releases for GAIA Docker containers.

## Usage

```
/release
```

## Workflow

1. **Read current versions** from `VERSION.json`
2. **Ask user for action**:
   - **New Release**: Bump version for gaia-linux, gaia-dev, or both
   - **Re-trigger Workflow**: Re-publish current versions to Docker Hub
3. **For New Release**:
   - Ask which container(s) to release
   - Ask for new version number(s)
   - Update `VERSION.json`
   - Update hardcoded versions in README files
   - Commit and push changes
4. **For Re-trigger**:
   - Run `gh workflow run` to re-publish

## Instructions

When the user invokes `/release`:

### Step 1: Read Current State

Read `VERSION.json` to get current versions:
```bash
cat VERSION.json
```

### Step 2: Ask User Intent

Use AskUserQuestion to ask:
- "What would you like to do?"
  - **New gaia-linux release** - Bump gaia-linux version
  - **New gaia-dev release** - Bump gaia-dev version
  - **Re-trigger workflow** - Re-publish current versions

### Step 3a: For New Release

If user chose new release:

1. Ask for the new version number
2. Update `VERSION.json` with the new version
3. Update version references in these files:
   - `docs/gaia-linux/README.md` - Update all occurrences of the old version
   - `docs/gaia-dev/README.md` - Update all occurrences of the old version
   - `README.md` - Update version in "Current Versions" line and examples
4. Commit changes with message: `Release <container> v<version>`
5. Push to main branch

### Step 3b: For Re-trigger

If user chose re-trigger:

```bash
gh workflow run "Test, Publish, Release" --ref main
```

Then inform user that the workflow has been triggered and they can check progress at the Actions tab.

## Files to Update on New Release

### For gaia-linux release:
- `VERSION.json` - Update `"gaia-linux"` value
- `docs/gaia-linux/README.md` - Replace all `gaia-linux:<old>` with `gaia-linux:<new>`
- `README.md` - Update "Current Versions" line and docker examples

### For gaia-dev release:
- `VERSION.json` - Update `"gaia-dev"` value
- `docs/gaia-dev/README.md` - Replace all `gaia-dev:<old>` with `gaia-dev:<new>`
- `README.md` - Update "Current Versions" line and docker examples

## Example Interaction

```
User: /release

Claude: Current versions:
- gaia-linux: 0.15.3
- gaia-dev: 1.0.0

What would you like to do?
[New gaia-linux release] [New gaia-dev release] [Re-trigger workflow]

User: New gaia-linux release

Claude: What version should gaia-linux be released as?
Current: 0.15.3

User: 0.15.4

Claude: I'll update the following:
- VERSION.json: gaia-linux → 0.15.4
- docs/gaia-linux/README.md: Update version references
- README.md: Update version references

[Makes changes, commits, and pushes]

Done! Release v0.15.4 has been pushed. The CI workflow will:
1. Run tests
2. Build and push Docker images
3. Update Docker Hub README
4. Create GitHub release

Check progress: https://github.com/<repo>/actions
```
</release-skill>
