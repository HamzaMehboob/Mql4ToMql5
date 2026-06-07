# MQL4 → MQL5 Migration Guide

Patterns the converter handles automatically, flags for manual review, and recommended MQL5 replacements.

## Legend

| Status | Meaning |
|--------|---------|
| **Auto** | Converted automatically |
| **Manual** | Tool warns; you must edit by hand |
| **Unsupported** | No automation in current release |

## Automatic conversions (MVP)

| MQL4 | MQL5 | Rule ID | Status |
|------|------|---------|--------|
| `#property strict` | *(line removed)* | RULE-DIR-001 | Auto |
| `Bid` | `SymbolInfoDouble(Symbol(), SYMBOL_BID)` | RULE-PRICE-001 | Auto |
| `Ask` | `SymbolInfoDouble(Symbol(), SYMBOL_ASK)` | RULE-PRICE-002 | Auto |
| `Ask` in `OrderSend(...)` line | `SymbolInfoDouble(Symbol(), SYMBOL_ASK)` | RULE-TRADE-003 | Auto |
| `OP_BUY` | `ORDER_TYPE_BUY` | RULE-TRADE-001 | Auto |
| `OP_SELL` | `ORDER_TYPE_SELL` | RULE-TRADE-002 | Auto |
| `double ma = iMA(NULL, 0, period, ...)` | Handle + `CopyBuffer()` + `ma[0]` | RULE-IND-001 | Auto |

## Manual review (reported, not auto-converted)

| Pattern | Rule ID | MQL5 guidance |
|---------|---------|---------------|
| `iMA(NULL, ...)` not matching RULE-IND-001 | RULE-SCAN-001 | Convert to handle + `CopyBuffer()` manually |
| `OrderSelect` | RULE-SCAN-003 | Use Positions/Orders API |
| `OrderClose` | RULE-SCAN-004 | Use `PositionClose()` or close request |
| `OrderType` | RULE-SCAN-005 | Use position/order type properties |
| `OrdersTotal` | RULE-SCAN-006 | Use `PositionsTotal()` / MQL5 orders functions |
| `init()` | RULE-SCAN-007 | Rename to `OnInit()` |
| `deinit()` | RULE-SCAN-008 | Rename to `OnDeinit()` |
| `start()` | RULE-SCAN-009 | Rename to `OnTick()` |
| `extern` | RULE-SCAN-010 | Replace with `input` |

## After conversion

1. Open the output file in **MetaEditor** (MT5).
2. Compile and fix remaining errors.
3. Test on a demo account before live trading.

## Report JSON

When using `--report report.json`, findings use severity values:

- `auto` — applied by the converter
- `manual` — needs your attention
- `unsupported` — not handled in this release

See [README.md](README.md) for exit codes and CLI usage.
