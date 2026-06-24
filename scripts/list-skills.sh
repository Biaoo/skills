#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
List skills in this repository.

Usage:
  scripts/list-skills.sh [--format path|name|table] [--bucket <bucket>]

Options:
  --format <format>  Output format: path, name, or table. Default: path.
  --bucket <bucket>  Only list skills from one bucket, such as engineering or personal.
  -h, --help         Show this help.

Examples:
  scripts/list-skills.sh
  scripts/list-skills.sh --format table
  scripts/list-skills.sh --bucket engineering --format name
EOF
}

repo="$(cd "$(dirname "$0")/.." && pwd)"
format="path"
bucket_filter=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --format)
      if [ "$#" -lt 2 ]; then
        echo "error: --format expects path, name, or table" >&2
        exit 2
      fi
      format="$2"
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

case "$format" in
  path|name|table) ;;
  *)
    echo "error: --format expects path, name, or table" >&2
    exit 2
    ;;
esac

extract_summary() {
  awk '
    /^[[:space:]]+short-description:[[:space:]]*/ {
      sub(/^[[:space:]]+short-description:[[:space:]]*/, "")
      gsub(/^"|"$/, "")
      print
      found = 1
      exit
    }
    /^description:[[:space:]]*/ {
      sub(/^description:[[:space:]]*/, "")
      gsub(/^"|"$/, "")
      description = $0
    }
    END {
      if (!found && description != "") {
        print description
      }
    }
  ' "$1"
}

if [ "$format" = "table" ]; then
  printf "%-14s %-32s %s\n" "BUCKET" "NAME" "DESCRIPTION"
fi

find "$repo/skills" -name SKILL.md -type f -not -path '*/node_modules/*' | sort |
while IFS= read -r skill_md; do
  rel="${skill_md#"$repo/skills/"}"
  skill_dir="$(dirname "$rel")"
  bucket="${skill_dir%%/*}"
  name="$(basename "$skill_dir")"

  if [ -n "$bucket_filter" ] && [ "$bucket" != "$bucket_filter" ]; then
    continue
  fi

  case "$format" in
    path)
      printf "%s\n" "$skill_dir"
      ;;
    name)
      printf "%s\n" "$name"
      ;;
    table)
      description="$(extract_summary "$skill_md")"
      printf "%-14s %-32s %s\n" "$bucket" "$name" "$description"
      ;;
  esac
done
