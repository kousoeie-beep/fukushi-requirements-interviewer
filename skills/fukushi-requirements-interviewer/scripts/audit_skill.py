#!/usr/bin/env python3
"""Deterministic structural audit for the interview Skill."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_DIR = SKILL_DIR.parents[1]


@dataclass(frozen=True)
class Finding:
    check: str
    detail: str


def read(relative: str) -> str:
    return (SKILL_DIR / relative).read_text(encoding="utf-8")


def quoted_question_blocks(markdown: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in markdown.splitlines():
        if line.startswith(">"):
            current.append(line[1:].lstrip())
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return ["\n".join(block) for block in blocks if "?" in "\n".join(block) or "？" in "\n".join(block)]


def main() -> int:
    findings: list[Finding] = []
    required = [
        "SKILL.md",
        "agents/openai.yaml",
        "references/interview-engine.md",
        "references/question-bank.md",
        "references/requirements-output.md",
        "references/development-materials.md",
    ]
    for relative in required:
        if not (SKILL_DIR / relative).is_file():
            findings.append(Finding("required-file", relative))

    if findings:
        for finding in findings:
            print(f"FAIL {finding.check}: {finding.detail}")
        return 1

    skill = read("SKILL.md")
    questions = read("references/question-bank.md")
    engine = read("references/interview-engine.md")
    output = read("references/requirements-output.md")
    materials = read("references/development-materials.md")
    openai = read("agents/openai.yaml")
    readme = (REPO_DIR / "README.md").read_text(encoding="utf-8")

    if not skill.startswith("---\n") or "name: fukushi-requirements-interviewer" not in skill:
        findings.append(Finding("frontmatter", "missing valid name frontmatter"))

    for phrase in ["ヒアリングスタート", "1メッセージにつき必ず1問", "ヒアリング再開", "ヒアリング終了"]:
        if phrase not in skill:
            findings.append(Finding("trigger-contract", phrase))

    for phrase in ["確認済み", "仮説", "資料待ち", "判断待ち", "READY"]:
        if phrase not in skill + engine + output:
            findings.append(Finding("state-contract", phrase))

    for phrase in ["匿名化", "パスワード", "1回1件", "優先度A"]:
        if phrase not in skill + materials:
            findings.append(Finding("material-safety", phrase))

    match = re.search(r'short_description: "([^"]+)"', openai)
    if not match or not 25 <= len(match.group(1)) <= 64:
        findings.append(Finding("openai-metadata", "short_description must be 25-64 characters"))
    if "$fukushi-requirements-interviewer" not in openai:
        findings.append(Finding("openai-metadata", "default_prompt must mention $skill-name"))

    blocks = quoted_question_blocks(skill + "\n" + questions)
    banned = ["API", "CSV", "データベース", "権限設計", "認証", "MVP", "PoC", "SLA"]
    for index, block in enumerate(blocks, start=1):
        question_count = block.count("?") + block.count("？")
        if question_count != 1:
            findings.append(Finding("one-question", f"block {index} has {question_count} questions"))
        choices = re.findall(r"(?m)^[A-H]\. ", block)
        if choices and not 3 <= len(choices) <= 8:
            findings.append(Finding("choice-count", f"block {index} has {len(choices)} choices"))
        for term in banned:
            if term in block:
                findings.append(Finding("plain-language", f"block {index} contains {term}"))

    for phrase in [
        "hermes skills install kousoeie-beep/fukushi-requirements-interviewer/skills/fukushi-requirements-interviewer",
        "$fukushi-requirements-interviewer",
        "ヒアリングスタート",
    ]:
        if phrase not in readme:
            findings.append(Finding("install-doc", phrase))

    if findings:
        for finding in findings:
            print(f"FAIL {finding.check}: {finding.detail}")
        print(f"RESULT: FAIL ({len(findings)} findings)")
        return 1

    print(f"quoted_question_blocks={len(blocks)}")
    print("RESULT: PASS (0 findings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
