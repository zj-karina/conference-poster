#!/usr/bin/env bash
# Install the conference-poster skill into Claude Code.
#
# Symlinks (default) or copies this repo into ~/.claude/skills/conference-poster
# so Claude Code discovers it. Symlinking means `git pull` keeps the skill current.
#
# Usage:
#   ./install.sh           # symlink (recommended)
#   ./install.sh --copy    # copy files instead of symlinking
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
DEST="$SKILLS_DIR/conference-poster"
MODE="symlink"
[ "${1:-}" = "--copy" ] && MODE="copy"

if [ ! -f "$REPO_DIR/SKILL.md" ]; then
  echo "ERROR: SKILL.md not found in $REPO_DIR — run this from the repo root." >&2
  exit 1
fi

mkdir -p "$SKILLS_DIR"

# Back up / clear any existing install.
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  if [ -L "$DEST" ]; then
    rm "$DEST"
  else
    BAK="$DEST.bak.$$"
    echo "existing install found -> backing up to $BAK"
    mv "$DEST" "$BAK"
  fi
fi

if [ "$MODE" = "symlink" ]; then
  ln -s "$REPO_DIR" "$DEST"
  echo "OK: symlinked $DEST -> $REPO_DIR"
else
  mkdir -p "$DEST"
  cp -r "$REPO_DIR"/SKILL.md "$REPO_DIR"/scripts "$REPO_DIR"/assets "$REPO_DIR"/reference "$DEST"/
  echo "OK: copied skill to $DEST"
fi

echo
echo "Done. Restart Claude Code (or start a new session), then ask it to"
echo "\"make a conference poster\" to confirm the skill is loaded."
