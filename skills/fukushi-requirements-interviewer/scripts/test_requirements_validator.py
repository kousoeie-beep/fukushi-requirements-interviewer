#!/usr/bin/env python3
"""Focused tests for validate_requirements.py."""

from __future__ import annotations

from validate_requirements import REQUIRED_SECTIONS, validate


def complete_document(status: str = "ENGINEERING_READY") -> str:
    headings = "\n".join(f"## {index}. {name}\n内容あり" for index, name in enumerate(REQUIRED_SECTIONS, start=1))
    return f"""# 要件定義書

| 引き渡し状態 | {status} |
| ブロッカー件数 | 0 |

{headings}

| P-001 | 問題 |
| G-001 | 目標 |
| NEED-001 | 必要性 |
| FR-001 | 必須 | 記録を保存する |
| DATA-001 | 記録内容 |
| INT-001 | 対象外 |
| SRC-001 | 業務責任者回答 |
| AC-001 | FR-001 | 通常 | 保存される |
| 最終承認 | 業務責任者 | 承認 | 2026-08-28 |
"""


def main() -> int:
    cases = [
        ("complete_ready", complete_document(), 0),
        ("missing_ac", complete_document().replace("| AC-001 | FR-001 | 通常 | 保存される |", ""), 1),
        ("ready_with_unknown", complete_document() + "\n未確認\n", 1),
        ("draft_can_have_unknown", complete_document("DRAFT_NOT_READY") + "\n未確認\n", 0),
    ]

    failed = 0
    for name, document, minimum_findings in cases:
        _, findings = validate(document)
        passed = len(findings) >= minimum_findings if minimum_findings else not findings
        print(f"{'PASS' if passed else 'FAIL'} {name}: {len(findings)} findings")
        failed += not passed

    print(f"RESULT: {'PASS' if failed == 0 else 'FAIL'} ({len(cases) - failed}/{len(cases)} cases)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
