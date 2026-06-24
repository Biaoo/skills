#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Link skills from this repository into a local agent skills directory.

Usage:
  scripts/link-skills.sh [--target codex|claude] [--bucket <bucket>] [--dry-run] [--force]

Options:
  --target <target>  Link into codex (~/.codex/skills) or claude (~/.claude/skills).
                     Default: codex.
  --bucket <bucket>  Only link skills from one bucket, such as engineering or personal.
  --dry-run          Print what would be linked without changing files.
  --force            Replace existing non-symlink skill directories at the target.
  -h, --help         Show this help.

Examples:
  scripts/link-skills.sh --target codex
  scripts/link-skills.sh --target claude --bucket engineering
  scripts/link-skills.sh --target codex --dry-run

Safety:
  Existing symlinks are replaced.
  Existing non-symlink files or directories are skipped unless --force is used.
EOF
}

repo="$(cd "$(dirname "$0")/.." && pwd)"
target_kind="codex"
bucket_filter=""
dry_run=0
force=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      if [ "$#" -lt 2 ]; then
        echo "error: --target expects codex or claude" >&2
        exit 2
      fi
      target_kind="$2"
      shift 2
      ;;
    --bucket)
      if [ "$#" -lt 2 ]; then
        echo "error: --bucket expects a bucket name" >&2
        exit 2
      fi
      bucket_filter="$2"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    --force)
      force=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$target_kind" in
  codex)
    dest="$HOME/.codex/skills"
    ;;
  claude)
    dest="$HOME/.claude/skills"
    ;;
  *)
    echo "error: --target expects codex or claude" >&2
    exit 2
    ;;
esac

resolve_symlink_target() {
  local link_path="$1"
  local link_target
  link_target="$(readlink "$link_path")"
  case "$link_target" in
    /*)
      printf "%s\n" "$link_target"
      ;;
    *)
      printf "%s/%s\n" "$(cd "$(dirname "$link_path")" && pwd -P)" "$link_target"
      ;;
  esac
}

if [ -L "$dest" ]; then
  resolved_dest="$(resolve_symlink_target "$dest")"
  case "$resolved_dest" in
    "$repo"|"$repo"/*)
      echo "error: $dest is a symlink into this repository: $resolved_dest" >&2
      echo "Remove it or choose another target before linking skills." >&2
      exit 1
      ;;
  esac
fi

if [ "$dry_run" -eq 0 ]; then
  mkdir -p "$dest"
fi

linked=0
skipped=0
failed=0

while IFS= read -r skill_md; do
  rel="${skill_md#"$repo/skills/"}"
  skill_dir_rel="$(dirname "$rel")"
  bucket="${skill_dir_rel%%/*}"
  name="$(basename "$skill_dir_rel")"
  src="$(dirname "$skill_md")"
  target="$dest/$name"

  if [ -n "$bucket_filter" ] && [ "$bucket" != "$bucket_filter" ]; then
    continue
  fi

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    if [ "$force" -eq 1 ]; then
      if [ "$dry_run" -eq 1 ]; then
        echo "would replace $target"
      else
        rm -rf "$target"
      fi
    else
      echo "skip $name: $target exists and is not a symlink; rerun with --force to replace it" >&2
      skipped=$((skipped + 1))
      failed=1
      continue
    fi
  fi

  if [ "$dry_run" -eq 1 ]; then
    echo "would link $name -> $src"
  else
    rm -f "$target"
    ln -s "$src" "$target"
    echo "linked $name -> $src"
  fi
  linked=$((linked + 1))
done < <(find "$repo/skills" -name SKILL.md -type f -not -path '*/node_modules/*' | sort)

if [ "$dry_run" -eq 1 ]; then
  title="Skills link dry run"
else
  title="Skills linked"
fi

printf "\n%s\n\n" "$title"
printf "Summary:\n"
printf -- "- target: %s (%s)\n" "$target_kind" "$dest"
printf -- "- linked: %s\n" "$linked"
printf -- "- skipped: %s\n" "$skipped"

if [ "$failed" -ne 0 ]; then
  printf "\nNext:\n"
  printf -- "- Resolve skipped targets or rerun with --force if replacement is intended.\n"
  exit 1
fi

printf "\nNext:\n"
printf -- "- Run scripts/list-skills.sh --format table to inspect available skills.\n"
