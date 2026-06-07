"""Command-line interface."""

import argparse
import sys
from pathlib import Path

from mql4tomql5.converter import convert_with_report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mql4tomql5", description="Convert MQL4 source to MQL5")
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser("convert", help="Convert a single .mq4 file")
    convert_parser.add_argument("input", type=Path, help="Input .mq4 file")
    convert_parser.add_argument("-o", "--output", type=Path, help="Output .mq5 file")
    convert_parser.add_argument("--dry-run", action="store_true", help="Preview without writing output")
    convert_parser.add_argument("--verbose", action="store_true", help="Log each rule application")
    convert_parser.add_argument("--quiet", action="store_true", help="Show errors and summary only")
    convert_parser.add_argument("--report", type=Path, help="Write JSON conversion report to PATH")

    return parser


def _default_output(input_path: Path) -> Path:
    return input_path.with_suffix(".mq5")


def _print_summary(
    report,
    input_path: Path,
    output_path: Path,
    *,
    quiet: bool,
    verbose: bool,
    report_path: Path | None,
) -> None:
    summary = report.summary
    if quiet:
        if report.has_manual_review:
            print(f"Manual review: {summary['manual_required']} items", file=sys.stderr)
        return

    print(f"\nConverted: {input_path} -> {output_path}")
    print(f"  Rules applied: {summary['rules_applied']}")
    print(f"  Auto-converted:  {summary['auto_converted']} changes")
    print(f"  Manual review:   {summary['manual_required']} items", end="")
    if report_path:
        print(" (see report)")
    else:
        print()

    if verbose:
        for finding in report.findings:
            if finding.severity == "auto":
                print(f"  [auto] Line {finding.line}: {finding.message}")

    for finding in report.manual_findings():
        line = finding.line or "?"
        print(f"  [!] Line {line}: {finding.message}")

    if report_path:
        print(f"\nReport: {report_path}")


def _exit_code(report) -> int:
    if report.has_manual_review:
        return 1
    return 0


def run_convert(args: argparse.Namespace) -> int:
    input_path: Path = args.input.resolve()

    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 2

    output_path = args.output.resolve() if args.output else _default_output(input_path).resolve()

    try:
        source = input_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error: cannot read {input_path}: {exc}", file=sys.stderr)
        return 2

    converted, report = convert_with_report(
        source,
        input_path=str(input_path),
        output_path=str(output_path),
    )

    if args.report:
        try:
            report.write_json(args.report.resolve())
        except OSError as exc:
            print(f"Error: cannot write report: {exc}", file=sys.stderr)
            return 2

    _print_summary(
        report,
        input_path,
        output_path,
        quiet=args.quiet,
        verbose=args.verbose,
        report_path=args.report,
    )

    if args.dry_run:
        if not args.quiet:
            print("\n(dry-run - no file written)")
        return _exit_code(report)

    try:
        output_path.write_text(converted, encoding="utf-8")
    except OSError as exc:
        print(f"Error: cannot write {output_path}: {exc}", file=sys.stderr)
        return 2

    return _exit_code(report)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "convert":
        return run_convert(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
