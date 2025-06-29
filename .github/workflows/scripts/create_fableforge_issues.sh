#!/bin/bash

REPO="Coding-for-Weeks/FableForge"

echo "🚀 Creating GitHub Issues in $REPO..."

gh issue create -R "$REPO" -t "Fix menu recursion crash" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Set up init_db.py or DB schema script" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Add character creation system" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Implement quest flow system" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Combat loop logic" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Save/load player progress" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Write unit tests with pytest" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Fix GitHub Action PR requirement" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Expand README with usage and features" \
  -F templates/issue-template.md

gh issue create -R "$REPO" -t "Add CLI color polish with rich" \
  -F templates/issue-template.md

echo "✅ All issues created! You can now manually track or automate more."
