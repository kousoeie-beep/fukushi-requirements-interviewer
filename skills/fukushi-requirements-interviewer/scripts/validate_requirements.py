#!/usr/bin/env python3
"""Validate an engineer-handoff requirements document before delivery."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys


REQUIRED_SECTIONS = [
    "引き渡し判定",
    "背景・目的・成功指標",
    "スコープ",
    "現在の業務",
    "改善後の業務",
    "機能要件",
    "画面・帳票・通知",
    "データ要件",
    "既存システム・外部との情報受け渡し",
    "AI利用要件",
    "情報管理・プライバシー",
    "品質要件",
    "運用・サポート",
    "受入条件・テスト",
    "未解決事項・決定事項",
    "トレーサビリティ",
    "開発見積もり・技術設計への引き渡し情報",
    "承認",
]

UNRESOLVED_MARKERS = ["未確認", "TBD", "TODO", "資料待ち", "判断待ち", "仮説のまま"]


@dataclass(frozen=True)
class Finding:
    code: str
    detail: str


def status_of(text: str) -> str | None:
    statuses = re.findall(r"\b(?:ENGINEERING_READY|CONDITIONALLY_READY|DRAFT_NOT_READY)\b", text)
    return statuses[0] if statuses else None


def validate(text: str) -> tuple[str | None, list[Finding]]:
    findings: list[Finding] = []
    status = status_of(text)
    if status is None:
        findings.append(Finding("STATUS", "引き渡し状態がありません"))

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"(?m)^#+\s+.*{re.escape(section)}", text):
            findings.append(Finding("SECTION", section))

    if re.search(r"\b(?:FR|AC|DATA|INT|OI)-xxx\b", text, re.IGNORECASE):
        findings.append(Finding("PLACEHOLDER_ID", "xxx形式のIDが残っています"))

    fr_ids = set(re.findall(r"\bFR-\d{3}\b", text))
    ac_rows = [line for line in text.splitlines() if re.search(r"\bAC-\d{3}\b", line)]
    covered_fr = {identifier for line in ac_rows for identifier in re.findall(r"\bFR-\d{3}\b", line)}
    if not fr_ids:
        findings.append(Finding("FUNCTIONAL_REQUIREMENT", "FRがありません"))
    for identifier in sorted(fr_ids - covered_fr):
        findings.append(Finding("AC_COVERAGE", f"{identifier} に結び付くACがありません"))

    if not re.search(r"\bSRC-\d{3}\b", text):
        findings.append(Finding("EVIDENCE", "SRCがありません"))
    if not re.search(r"\b(?:P|G|NEED)-\d{3}\b", text):
        findings.append(Finding("TRACEABILITY", "問題・目標・ニーズのIDがありません"))

    if status == "ENGINEERING_READY":
        for marker in UNRESOLVED_MARKERS:
            if marker in text:
                findings.append(Finding("UNRESOLVED", marker))
        if re.search(r"(?im)\b(?:Yes|あり)\b.*(?:ブロッカー)|(?:ブロッカー).*\b(?:Yes|あり)\b", text):
            findings.append(Finding("BLOCKER", "ENGINEERING_READYにブロッカーがあります"))
        if "合意済み" in text and not re.search(r"(?m)^\|\s*最終承認\s*\|.*\b承認\b", text):
            findings.append(Finding("APPROVAL", "合意済みですが最終承認が確認できません"))

    return status, findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    args = parser.parse_args()

    if not args.document.is_file():
        print(f"FAIL FILE: {args.document}")
        return 2

    status, findings = validate(args.document.read_text(encoding="utf-8"))
    for finding in findings:
        print(f"FAIL {finding.code}: {finding.detail}")
    print(f"status={status or 'MISSING'}")
    print(f"RESULT: {'PASS' if not findings else 'FAIL'} ({len(findings)} findings)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
