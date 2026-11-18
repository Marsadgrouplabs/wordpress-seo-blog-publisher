#!/usr/bin/env bash
# Installs this skill for Claude Code and/or Codex on this computer.
# Usage: bash install.sh [claude|codex|both]
set -euo pipefail

NAME="wordpress-seo-blog-publisher"
TARGET="${1:-both}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$HERE/skills/$NAME"

[ -f "$SOURCE/SKILL.md" ] || { echo "Skill files not found in $SOURCE" >&2; exit 1; }

case "$TARGET" in
  claude) ROOTS=("$HOME/.claude/skills") ;;
  codex)  ROOTS=("$HOME/.agents/skills") ;;
  both)   ROOTS=("$HOME/.claude/skills" "$HOME/.agents/skills") ;;
  *) echo "Usage: bash install.sh [claude|codex|both]" >&2; exit 1 ;;
esac

for ROOT in "${ROOTS[@]}"; do
  mkdir -p "$ROOT"
  DEST="$ROOT/$NAME"
  if [ -e "$DEST" ]; then
    BACKUP="$ROOT/.$NAME.backup-$(date +%Y%m%d-%H%M%S)"
    mv "$DEST" "$BACKUP"
    echo "Previous version kept at: $BACKUP"
  fi
  cp -R "$SOURCE" "$DEST"
  echo "Installed: $DEST"
done
echo "Done. Start a new session to use the skill."
