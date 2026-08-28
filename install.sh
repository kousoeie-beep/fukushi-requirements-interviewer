#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./install.sh <hermes|codex|both> [--force]"
}

target="${1:-}"
force="${2:-}"
if [[ "$target" != "hermes" && "$target" != "codex" && "$target" != "both" ]]; then
  usage
  exit 2
fi
if [[ -n "$force" && "$force" != "--force" ]]; then
  usage
  exit 2
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_dir="$script_dir/skills/fukushi-requirements-interviewer"
if [[ ! -f "$source_dir/SKILL.md" ]]; then
  echo "ERROR: Skill本体が見つかりません: $source_dir"
  exit 1
fi

install_one() {
  local product="$1"
  local root_dir
  if [[ "$product" == "hermes" ]]; then
    root_dir="${HERMES_HOME:-$HOME/.hermes}/skills"
  else
    root_dir="${CODEX_HOME:-$HOME/.codex}/skills"
  fi

  local destination="$root_dir/fukushi-requirements-interviewer"
  mkdir -p "$root_dir"
  if [[ -e "$destination" && "$force" != "--force" ]]; then
    echo "ERROR: $destination は既にあります。確認後に --force を付けてください。"
    return 1
  fi
  if [[ -e "$destination" ]]; then
    local backup="${destination}.backup.$(date +%Y%m%d%H%M%S)"
    mv "$destination" "$backup"
    echo "既存版を退避しました: $backup"
  fi
  cp -R "$source_dir" "$destination"
  echo "Installed for $product: $destination"
}

if [[ "$target" == "hermes" || "$target" == "both" ]]; then
  install_one hermes
fi
if [[ "$target" == "codex" || "$target" == "both" ]]; then
  install_one codex
fi

echo "完了しました。新しい会話を開き、『ヒアリングスタート』と入力してください。"
