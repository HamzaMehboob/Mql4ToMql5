#!/usr/bin/env python3
"""Convert the bundled sample EA (examples/sample.mq4 → examples/sample.mq5)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mql4tomql5 import convert_with_report

INPUT_FILE = ROOT / "examples" / "sample.mq4"
OUTPUT_FILE = ROOT / "examples" / "sample.mq5"


def main() -> int:
    source = INPUT_FILE.read_text(encoding="utf-8")
    converted, report = convert_with_report(
        source,
        input_path=str(INPUT_FILE),
        output_path=str(OUTPUT_FILE),
    )
    OUTPUT_FILE.write_text(converted, encoding="utf-8")

    summary = report.summary
    print(f"Conversion completed: {OUTPUT_FILE}")
    print(f"  Auto-converted: {summary['auto_converted']} | Manual review: {summary['manual_required']}")
    return 1 if report.has_manual_review else 0


if __name__ == "__main__":
    raise SystemExit(main())
