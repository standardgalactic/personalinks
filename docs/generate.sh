#!/bin/bash
# Generate API documentation for Spherepop core modules using pdoc3.
#
# This script generates HTML documentation from docstrings for the stable
# public API surface. It documents only the established library interface,
# excluding experimental modules and research directories.
#
# Usage:
#   ./docs/generate.sh              # Generate docs locally
#   ./docs/generate.sh --serve      # Generate and serve at localhost:8080

set -e

cd "$(dirname "$0")/.."

# Core stable modules (see THEORY_STATUS.md for established vs provisional)
MODULES=(
    spherepop.model
    spherepop.semantics
    spherepop.observers
    spherepop.views
    spherepop.grammar
    spherepop.predicates
    spherepop.path_utils
    spherepop.validation
)

echo "Generating API documentation for Spherepop stable core..."

if [ "$1" = "--serve" ]; then
    echo "Starting documentation server at http://localhost:8080"
    python3 -m pdoc --html --http localhost:8080 "${MODULES[@]}"
else
    # Generate HTML to docs/api/
    python3 -m pdoc --html --output-dir docs/api --force "${MODULES[@]}"
    
    echo "✓ Documentation generated in docs/api/"
    echo ""
    echo "To view locally:"
    echo "  Open docs/api/spherepop/index.html in a browser"
    echo ""
    echo "To serve with live reload:"
    echo "  ./docs/generate.sh --serve"
fi
