#!/usr/bin/env python3
"""Policy simulations for important interview branches."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import sys


class Action(str, Enum):
    START = "start_with_one_question"
    ASK_SCOPE = "ask_scope"
    ASK_OWNER = "ask_owner"
    ASK_HUMAN_REVIEW = "ask_human_review"
    ASK_CONFLICT = "ask_conflict"
    REQUEST_ONE_DOCUMENT = "request_one_document"
    CHECK_CONTINUE = "check_continue"
    PAUSE = "pause_with_three_line_summary"
    PRODUCE_DRAFT = "produce_requirements_draft"
    CONTINUE_FOR_HANDOFF = "continue_for_engineer_handoff"
    PRODUCE_ENGINEER_READY = "produce_engineer_ready_requirements"


@dataclass(frozen=True)
class Scenario:
    name: str
    event: str
    answers: int = 0
    conflict: bool = False
    scope_known: bool = True
    owner_known: bool = True
    exact_rule_needed: bool = False
    ai_external_send_without_review: bool = False
    handoff_requested: bool = False
    all_gates_ready: bool = False
    expected: Action = Action.ASK_SCOPE


def decide(case: Scenario) -> Action:
    if case.event == "start":
        return Action.START
    if case.event == "pause":
        return Action.PAUSE
    if case.event == "finish":
        return Action.PRODUCE_DRAFT
    if case.handoff_requested and not case.all_gates_ready:
        return Action.CONTINUE_FOR_HANDOFF
    if case.handoff_requested and case.all_gates_ready:
        return Action.PRODUCE_ENGINEER_READY
    if case.conflict:
        return Action.ASK_CONFLICT
    if case.ai_external_send_without_review:
        return Action.ASK_HUMAN_REVIEW
    if case.exact_rule_needed:
        return Action.REQUEST_ONE_DOCUMENT
    if case.answers > 0 and case.answers % 5 == 0:
        return Action.CHECK_CONTINUE
    if not case.scope_known:
        return Action.ASK_SCOPE
    if not case.owner_known:
        return Action.ASK_OWNER
    return Action.ASK_SCOPE


def main() -> int:
    cases = [
        Scenario("trigger", "start", expected=Action.START),
        Scenario("unknown_scope", "answer", scope_known=False, expected=Action.ASK_SCOPE),
        Scenario("missing_owner", "answer", owner_known=False, expected=Action.ASK_OWNER),
        Scenario("contradiction", "answer", conflict=True, expected=Action.ASK_CONFLICT),
        Scenario("formal_rule", "answer", exact_rule_needed=True, expected=Action.REQUEST_ONE_DOCUMENT),
        Scenario("unsafe_ai_send", "answer", ai_external_send_without_review=True, expected=Action.ASK_HUMAN_REVIEW),
        Scenario("five_question_break", "answer", answers=5, expected=Action.CHECK_CONTINUE),
        Scenario("pause", "pause", expected=Action.PAUSE),
        Scenario("finish_with_unknowns", "finish", expected=Action.PRODUCE_DRAFT),
        Scenario("handoff_missing_requirements", "answer", handoff_requested=True, expected=Action.CONTINUE_FOR_HANDOFF),
        Scenario("handoff_all_gates_ready", "answer", handoff_requested=True, all_gates_ready=True, expected=Action.PRODUCE_ENGINEER_READY),
    ]

    failed = 0
    for case in cases:
        actual = decide(case)
        status = "PASS" if actual == case.expected else "FAIL"
        print(f"{status} {case.name}: {actual.value}")
        failed += actual != case.expected

    print(f"RESULT: {'PASS' if failed == 0 else 'FAIL'} ({len(cases) - failed}/{len(cases)} scenarios)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
