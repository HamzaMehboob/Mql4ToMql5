"""Public conversion API."""

from mql4tomql5.engine import convert_source
from mql4tomql5.report import ConversionReport
from mql4tomql5.rules import ALL_RULES


def convert_mql4_to_mql5(mql4_code: str) -> str:
    """Convert MQL4 source to MQL5. Returns converted source only."""
    converted, _ = convert_with_report(mql4_code)
    return converted


def convert_with_report(
    mql4_code: str,
    input_path: str | None = None,
    output_path: str | None = None,
) -> tuple[str, ConversionReport]:
    """Convert MQL4 source and return converted text plus a full report."""
    converted, findings = convert_source(mql4_code, ALL_RULES)
    report = ConversionReport(
        input_path=input_path,
        output_path=output_path,
        findings=findings,
    )
    return converted, report
