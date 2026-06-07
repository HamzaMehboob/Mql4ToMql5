"""Conversion engine — runs registered rules in order."""

from dataclasses import dataclass
from typing import Literal, Protocol

Severity = Literal["auto", "manual", "unsupported"]


@dataclass
class RuleResult:
    rule_id: str
    line: int | None
    severity: Severity
    message: str
    before: str | None = None
    after: str | None = None


class ConversionRule(Protocol):
    rule_id: str

    def apply(self, source: str) -> tuple[str, list[RuleResult]]: ...


def convert_source(source: str, rules: list[ConversionRule]) -> tuple[str, list[RuleResult]]:
    """Apply all rules sequentially and collect findings."""
    results: list[RuleResult] = []
    current = source

    for rule in rules:
        current, rule_results = rule.apply(current)
        results.extend(rule_results)

    return current, results
