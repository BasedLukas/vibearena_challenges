#!/bin/bash
set -euo pipefail

echo "=== VibeArena Challenge Environment Setup ==="

# Install Python test dependencies
pip install pytest

# Default to the hello-world challenge
# Override with CHALLENGE env var for other challenges
CHALLENGE="${CHALLENGE:-hello-world}"

# Open the challenge README on startup
if [ -f "/workspaces/vibearena_challenges/${CHALLENGE}/README.md" ]; then
    mkdir -p /home/vscode/.local/share/code-server
fi

echo ""
echo "=============================================="
echo "  VibeArena Challenge Ready!"
echo "  Challenge: ${CHALLENGE}"
echo ""
echo "  cd ${CHALLENGE} to get started"
echo "  Run: pytest tests/ to check your solution"
echo "=============================================="
