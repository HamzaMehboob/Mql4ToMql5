"""Conversion report model and JSON export."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from mql4tomql5.engine import RuleResult

REPORT_VERSION = "1.0"


@dataclass
class ConversionReport:
    input_path: str | None
    output_path: str | None
    findings: list[RuleResult] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        auto = sum(1 for f in self.findings if f.severity == "auto")
        manual = sum(1 for f in self.findings if f.severity == "manual")
        unsupported = sum(1 for f in self.findings if f.severity == "unsupported")
        rules_applied = len({f.rule_id for f in self.findings if f.severity == "auto"})
        return {
            "rules_applied": rules_applied,
            "auto_converted": auto,
            "manual_required": manual,
            "unsupported": unsupported,
        }

    @property
    def has_manual_review(self) -> bool:
        return self.summary["manual_required"] > 0 or self.summary["unsupported"] > 0

    def to_dict(self) -> dict:
        return {
            "version": REPORT_VERSION,
            "input": self.input_path,
            "output": self.output_path,
            "summary": self.summary,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "line": f.line,
                    "severity": f.severity,
                    "message": f.message,
                    "before": f.before,
                    "after": f.after,
                }
                for f in self.findings
            ],
        }

    def write_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    def manual_findings(self) -> list[RuleResult]:
        return [f for f in self.findings if f.severity in ("manual", "unsupported")]
