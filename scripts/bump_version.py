#!/usr/bin/env python3
"""Version management utility for Spherepop.

Bumps version number, updates CHANGELOG.md, and prepares for release.

Usage:
    python scripts/bump_version.py patch    # 0.1.0 → 0.1.1
    python scripts/bump_version.py minor    # 0.1.0 → 0.2.0
    python scripts/bump_version.py major    # 0.1.0 → 1.0.0
    python scripts/bump_version.py 0.2.0    # Explicit version
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path


def get_current_version() -> str:
    """Extract current version from pyproject.toml."""
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        raise FileNotFoundError("pyproject.toml not found")

    content = pyproject.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("version not found in pyproject.toml")

    return match.group(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse semantic version string."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")

    return tuple(map(int, match.groups()))


def bump_version(current: str, bump_type: str) -> str:
    """Compute new version based on bump type.

    Args:
        current: Current version string (e.g., "0.1.0")
        bump_type: One of "major", "minor", "patch", or explicit version

    Returns:
        New version string
    """
    if bump_type not in ("major", "minor", "patch"):
        # Explicit version provided
        _ = parse_version(bump_type)  # Validate format
        return bump_type

    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()

    updated = re.sub(
        r'^(version\s*=\s*")[^"]+(")$', rf"\g<1>{new_version}\g<2>", content, flags=re.MULTILINE
    )

    pyproject.write_text(updated)
    print(f'✓ Updated pyproject.toml: version = "{new_version}"')


def update_changelog(new_version: str) -> None:
    """Move [Unreleased] section to versioned section in CHANGELOG.md."""
    changelog = Path("CHANGELOG.md")
    if not changelog.exists():
        print("⚠ CHANGELOG.md not found, skipping")
        return

    content = changelog.read_text()
    today = datetime.now().strftime("%Y-%m-%d")

    # Replace [Unreleased] with versioned section
    updated = re.sub(
        r"## \[Unreleased\]",
        f"## [Unreleased]\n\n(No unreleased changes yet)\n\n## [{new_version}] - {today}",
        content,
        count=1,
    )

    changelog.write_text(updated)
    print(f"✓ Updated CHANGELOG.md: [{new_version}] - {today}")


def main() -> int:
    """Main version bump workflow."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump_version.py [major|minor|patch|X.Y.Z]")
        return 1

    bump_type = sys.argv[1]

    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")

        new_version = bump_version(current_version, bump_type)
        print(f"New version: {new_version}")

        # Confirm
        response = input(f"\nBump {current_version} → {new_version}? [y/N] ")
        if response.lower() != "y":
            print("Cancelled")
            return 0

        # Update files
        update_pyproject(new_version)
        update_changelog(new_version)

        print("\n✓ Version bump complete")
        print("\nNext steps:")
        print(f"  1. Review CHANGELOG.md [{new_version}] section")
        print("  2. git add CHANGELOG.md pyproject.toml")
        print(f'  3. git commit -m "chore: Release v{new_version}"')
        print(f'  4. git tag -a v{new_version} -m "Release {new_version}"')
        print("  5. git push origin main")
        print(f"  6. git push origin v{new_version}")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
