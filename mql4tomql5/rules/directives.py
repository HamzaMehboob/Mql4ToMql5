"""MQL4 directive conversions."""

import re

from mql4tomql5.engine import RuleResult
from mql4tomql5.rules.base import line_number_at

_STRICT_PATTERN = re.compile(r"^[ \t]*#property\s+strict[ \t]*(?:\r?\n|$)", re.MULTILINE)


class RemoveStrictPropertyRule:
    rule_id = "RULE-DIR-001"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        results: list[RuleResult] = []
        for match in _STRICT_PATTERN.finditer(source):
            line = line_number_at(source, match.start())
            line_text = source.splitlines()[line - 1] if line <= len(source.splitlines()) else "#property strict"
            results.append(
                RuleResult(
                    rule_id=self.rule_id,
                    line=line,
                    severity="auto",
                    message="Removed #property strict (no MQL5 equivalent)",
                    before=line_text.strip(),
                    after=None,
                )
            )
        return _STRICT_PATTERN.sub("", source), results
