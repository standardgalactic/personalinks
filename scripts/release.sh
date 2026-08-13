#!/usr/bin/env bash
# Release workflow script
# Usage: ./scripts/release.sh [version]
#
# Examples:
#   ./scripts/release.sh 0.2.0
#   ./scripts/release.sh patch    # Auto-bump patch version
#   ./scripts/release.sh minor    # Auto-bump minor version

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

info() {
    echo -e "${GREEN}$1${NC}"
}

warn() {
    echo -e "${YELLOW}$1${NC}"
}

# Check we're on main branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" != "main" ]; then
    error "Must be on main branch (currently on: $BRANCH)"
fi

# Check working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    error "Working directory not clean. Commit or stash changes first."
fi

# Check all tests pass
info "Running tests..."
python3 -m pytest tests/ -q || error "Tests failed"

# Check coverage
info "Checking coverage..."
COVERAGE=$(python3 -m pytest --cov=spherepop --cov-report=term-missing tests/ -q 2>/dev/null | grep "^TOTAL" | awk '{print $4}' | tr -d '%')
if [ -z "$COVERAGE" ]; then
    warn "Could not determine coverage"
else
    info "Coverage: ${COVERAGE}%"
    if (( $(echo "$COVERAGE < 85" | bc -l) )); then
        warn "Coverage below target (85%): ${COVERAGE}%"
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Get version argument
VERSION_ARG="${1:-}"
if [ -z "$VERSION_ARG" ]; then
    error "Usage: $0 [version|major|minor|patch]"
fi

# Bump version
info "Bumping version to: $VERSION_ARG"
python3 scripts/bump_version.py "$VERSION_ARG" <<< "y" || error "Version bump failed"

# Get new version from pyproject.toml
NEW_VERSION=$(grep -Po '(?<=version = ")[^"]*' pyproject.toml)
info "New version: $NEW_VERSION"

# Verify CHANGELOG was updated
if ! grep -q "\[$NEW_VERSION\]" CHANGELOG.md; then
    error "CHANGELOG.md not updated with [$NEW_VERSION]"
fi

# Commit release
info "Committing release..."
git add CHANGELOG.md pyproject.toml
git commit -m "chore: Release v$NEW_VERSION" || error "Commit failed"

# Create tag
info "Creating tag v$NEW_VERSION..."
git tag -a "v$NEW_VERSION" -m "Release $NEW_VERSION" || error "Tag creation failed"

# Show summary
echo
info "Release prepared:"
info "  Version: $NEW_VERSION"
info "  Tag: v$NEW_VERSION"
info "  Commit: $(git rev-parse HEAD)"
echo
info "Next steps:"
echo "  1. Review: git show"
echo "  2. Push: git push origin main"
echo "  3. Push tag: git push origin v$NEW_VERSION"
echo "  4. GitHub Actions will create release automatically"
echo
warn "If something is wrong:"
echo "  Undo commit: git reset --hard HEAD~1"
echo "  Delete tag: git tag -d v$NEW_VERSION"
