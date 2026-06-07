"""Shared helpers for conversion rules."""

import re

from mql4tomql5.engine import RuleResult


def line_number_at(source: str, index: int) -> int:
    return source[:index].count("\n") + 1


def replace_word(
    source: str,
    word: str,
    replacement: str,
    rule_id: str,
    message: str,
) -> tuple[str, list[RuleResult]]:
    """Replace standalone word tokens and record one finding per changed line."""
    pattern = re.compile(r"\b" + re.escape(word) + r"\b")
    results: list[RuleResult] = []
    output: list[str] = []

    for line_num, line in enumerate(source.splitlines(keepends=True), 1):
        if not pattern.search(line):
            output.append(line)
            continue

        new_line = pattern.sub(replacement, line)
        if new_line != line:
            results.append(
                RuleResult(
                    rule_id=rule_id,
                    line=line_num,
                    severity="auto",
                    message=message,
                    before=line.strip(),
                    after=new_line.strip(),
                )
            )
        output.append(new_line)

    return "".join(output), results
