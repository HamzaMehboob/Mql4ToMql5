# MQL4 to MQL5 Converter

A Python CLI tool that helps migrate **MetaTrader 4 (MQL4)** Expert Advisors, indicators, and scripts toward **MetaTrader 5 (MQL5)**. It applies rule-based source transformations and reports what was changed automatically versus what still needs manual review.

> **Status: MVP.** Core conversion rules, CLI, reports, and tests are implemented. Full EA migration is not automatic — always review output in MetaEditor.

---

## Features

- CLI: `python -m mql4tomql5 convert file.mq4`
- Automatic rules for `Bid`, `Ask`, `#property strict`, `OP_BUY`/`OP_SELL`, `OrderSend` price args
- JSON conversion report with line-level findings
- Manual-review warnings for `iMA`, legacy order APIs, and event handlers
- pytest golden-file and per-rule tests

---

## Requirements

- **Python 3.9+**
- **pytest** (development only)

---

## Installation

```bash
git clone https://github.com/your-org/mql4_to_mql5.git
cd mql4_to_mql5
pip install -e .
```

Development install (includes pytest):

```bash
pip install -e ".[dev]"
```

---

## Quick start

### Convert a file

```bash
python -m mql4tomql5 convert examples/sample.mq4 -o examples/sample.mq5
```

### Write a JSON report

```bash
python -m mql4tomql5 convert examples/sample.mq4 --report report.json
```

### Preview without writing

```bash
python -m mql4tomql5 convert examples/sample.mq4 --dry-run
```

### Demo script

```bash
python scripts/convert_example.py
```

### Use as a library

```python
from mql4tomql5 import convert_mql4_to_mql5, convert_with_report

mql5 = convert_mql4_to_mql5(open("my_ea.mq4").read())

converted, report = convert_with_report(source, input_path="my_ea.mq4")
print(report.summary)
```

---

## CLI reference

```
python -m mql4tomql5 convert <input.mq4> [-o output.mq5] [--dry-run]
                              [--verbose|--quiet] [--report report.json]
```

| Flag | Description |
|------|-------------|
| `-o`, `--output` | Output path (default: same name with `.mq5`) |
| `--dry-run` | Show summary without writing output |
| `--verbose` | Log each auto-conversion |
| `--quiet` | Summary and errors only |
| `--report` | Write JSON report to path |

### Exit codes

| Code | Meaning |
|------|------|
| `0` | Success, no manual-review warnings |
| `1` | Converted with manual-review warnings |
| `2` | Fatal error (missing file, I/O failure, invalid args) |

### Report JSON schema

```json
{
  "version": "1.0",
  "input": "path/to/file.mq4",
  "output": "path/to/file.mq5",
  "summary": {
    "rules_applied": 5,
    "auto_converted": 8,
    "manual_required": 2,
    "unsupported": 0
  },
  "findings": [
    {
      "rule_id": "RULE-PRICE-001",
      "line": 10,
      "severity": "auto",
      "message": "Replaced Bid with SymbolInfoDouble(Symbol(), SYMBOL_BID)",
      "before": "if (Bid > ma)",
      "after": "if (SymbolInfoDouble(Symbol(), SYMBOL_BID) > ma)"
    }
  ]
}
```

See [MIGRATION.md](MIGRATION.md) for the full pattern table.

---

## Project structure

```
mql4_to_mql5/
├── README.md
├── MIGRATION.md
├── pyproject.toml
├── mql4tomql5/
│   ├── __init__.py
│   ├── __main__.py       # python -m mql4tomql5
│   ├── cli.py
│   ├── converter.py
│   ├── engine.py
│   ├── report.py
│   └── rules/            # One module per rule category
├── scripts/
│   └── convert_example.py
├── examples/
│   ├── sample.mq4
│   └── sample.mq5
└── tests/
    ├── fixtures/
    ├── test_converter.py
    └── test_rules/
```

---

## Limitations

- **Partial conversion** — order loops, indicator handles, and trade classes need manual work
- **Source only** — `.mq4` / `.mqh` input; no `.ex4` decompilation
- **Single file (MVP)** — `#include` graphs not yet supported
- **No compile step** — output is not validated against MetaEditor

Always review converted code before live trading.

---

## Development

```bash
pytest tests/ -v
python -m mql4tomql5 convert examples/sample.mq4 -o examples/sample.mq5
```

Implementation backlog: `docs/TODO.md` (local, gitignored).

---

## Roadmap

| Release | Highlights |
|---------|------------|
| **MVP** | CLI, rule registry, core rules, JSON report, tests |
| **v1.1** | Batch mode, `--in-place` with backup, diff output, config presets |
| **v2** | Multi-file projects, pip publish, optional MetaEditor integration |

---

## License

MIT
