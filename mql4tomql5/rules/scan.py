"""Post-conversion scan for patterns that need manual review."""

import re

from mql4tomql5.engine import RuleResult

_MANUAL_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    (
        "RULE-SCAN-001",
        re.compile(r"\biMA\s*\(\s*NULL"),
        "iMA(NULL, ...) - use handle + CopyBuffer pattern (see RULE-IND-001)",
    ),
    (
        "RULE-SCAN-003",
        re.compile(r"\bOrderSelect\b"),
        "OrderSelect() - migrate to Positions/Orders API manually",
    ),
    (
        "RULE-SCAN-004",
        re.compile(r"\bOrderClose\b"),
        "OrderClose() - migrate to Positions/Orders API manually",
    ),
    (
        "RULE-SCAN-005",
        re.compile(r"\bOrderType\b"),
        "OrderType() - migrate to Positions/Orders API manually",
    ),
    (
        "RULE-SCAN-006",
        re.compile(r"\bOrdersTotal\b"),
        "OrdersTotal() - migrate to PositionsTotal/OrdersTotal MQL5 API manually",
    ),
    (
        "RULE-SCAN-007",
        re.compile(r"\binit\s*\("),
        "init() - rename to OnInit() manually",
    ),
    (
        "RULE-SCAN-008",
        re.compile(r"\bdeinit\s*\("),
        "deinit() - rename to OnDeinit() manually",
    ),
    (
        "RULE-SCAN-009",
        re.compile(r"\bstart\s*\("),
        "start() - rename to OnTick() manually",
    ),
    (
        "RULE-SCAN-010",
        re.compile(r"\bextern\b"),
        "extern - replace with input keyword manually",
    ),
]


class ManualReviewScanRule:
    rule_id = "RULE-SCAN-MANUAL"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        results: list[RuleResult] = []
        seen: set[tuple[int, str]] = set()

        for line_num, line in enumerate(source.splitlines(), 1):
            for scan_id, pattern, msg in _MANUAL_PATTERNS:
                if not pattern.search(line):
                    continue
                key = (line_num, scan_id)
                if key in seen:
                    continue
                seen.add(key)
                results.append(
                    RuleResult(
                        rule_id=scan_id,
                        line=line_num,
                        severity="manual",
                        message=msg,
                        before=line.strip(),
                        after=None,
                    )
                )

        return source, results
