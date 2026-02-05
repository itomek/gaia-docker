<sync-versions-skill>
# Sync Versions Skill

Sync all version references across the repository to match VERSION.json.

## Usage

```
/sync-versions
```

## Workflow

1. **Read VERSION.json** as the source of truth
2. **Scan files** for version references that need updating
3. **Show proposed changes** as a diff preview
4. **Apply changes** after user confirmation

## Instructions

When the user invokes `/sync-versions`:

### Step 1: Read Source of Truth

Read `VERSION.json`:
```bash
cat VERSION.json
```

### Step 2: Scan for Outdated Versions

Check these files for version references:

**For gaia-linux version:**
- `gaia-linux/Dockerfile` - ARG GAIA_VERSION default
- `gaia-linux/entrypoint.sh` - GAIA_VERSION fallback default
- `CLAUDE.md` - Version examples and defaults
- `dev.md` - VERSION.json examples and docker commands
- `docs/dockerfile-usage.md` - Usage examples
- `docs/gaia-linux/README.md` - Docker pull/run commands
- `README.md` - Current Versions section and examples

**For gaia-dev version:**
- `gaia-dev/Dockerfile` - ARG GAIA_VERSION default (if present)
- `gaia-dev/entrypoint.sh` - GAIA_VERSION fallback default (if present)
- `docs/gaia-dev/README.md` - Docker pull/run commands
- `README.md` - Current Versions section and examples

### Step 3: Report Discrepancies

List all files where versions don't match VERSION.json:
```
Version Audit Results:

VERSION.json (source of truth):
- gaia-linux: 0.15.3
- gaia-dev: 1.0.0

Files needing updates:
- gaia-linux/Dockerfile: ARG GAIA_VERSION=0.15.1 → 0.15.3
- CLAUDE.md: Multiple references to 0.15.1 → 0.15.3
- (none found for gaia-dev)
```

### Step 4: Apply Changes (with confirmation)

Use AskUserQuestion to confirm:
- "Apply these version updates?"
  - **Yes** - Update all listed files
  - **No** - Cancel

If confirmed, update all files and report what was changed.

## Files to Check

### Critical (build/runtime behavior)
- `gaia-linux/Dockerfile` - Line with `ARG GAIA_VERSION=`
- `gaia-linux/entrypoint.sh` - Line with `GAIA_VERSION="${GAIA_VERSION:-`
- `gaia-dev/Dockerfile` - Line with `ARG GAIA_VERSION=`
- `gaia-dev/entrypoint.sh` - Line with `GAIA_VERSION="${GAIA_VERSION:-`

### Documentation
- `README.md` - Version badges, "Current Versions", examples
- `CLAUDE.md` - VERSION.json format example, environment variable defaults
- `dev.md` - VERSION.json examples, docker run examples
- `docs/dockerfile-usage.md` - FROM and example commands
- `docs/gaia-linux/README.md` - Pull/run commands
- `docs/gaia-dev/README.md` - Pull/run commands

## Example Interaction

```
User: /sync-versions

Claude: Reading VERSION.json...

Source of truth:
- gaia-linux: 0.15.3
- gaia-dev: 1.0.0

Scanning files for outdated versions...

Found 3 files with outdated gaia-linux version (0.15.1 → 0.15.3):
1. gaia-linux/Dockerfile: ARG GAIA_VERSION=0.15.1
2. gaia-linux/entrypoint.sh: GAIA_VERSION="${GAIA_VERSION:-0.15.1}"
3. CLAUDE.md: 4 references to 0.15.1

gaia-dev version is consistent (1.0.0).

Apply these updates?
[Yes] [No]

User: Yes

Claude: Updated:
- gaia-linux/Dockerfile: ARG GAIA_VERSION=0.15.3
- gaia-linux/entrypoint.sh: GAIA_VERSION="${GAIA_VERSION:-0.15.3}"
- CLAUDE.md: 4 version references updated

All versions now match VERSION.json!
```

## Notes

- VERSION.json is always the source of truth
- Only updates version numbers, doesn't change other content
- Shows diff preview before making changes
- Does not commit changes (user should review and commit separately)
</sync-versions-skill>
