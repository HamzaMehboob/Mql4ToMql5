"""Trade API conversions."""

import re

from mql4tomql5.engine import RuleResult
from mql4tomql5.rules.base import replace_word

_ASK_TOKEN = re.compile(r"\bAsk\b")


class OpBuyRule:
    rule_id = "RULE-TRADE-001"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        return replace_word(
            source,
            "OP_BUY",
            "ORDER_TYPE_BUY",
            self.rule_id,
            "Replaced OP_BUY with ORDER_TYPE_BUY",
        )


class OpSellRule:
    rule_id = "RULE-TRADE-002"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        return replace_word(
            source,
            "OP_SELL",
            "ORDER_TYPE_SELL",
            self.rule_id,
            "Replaced OP_SELL with ORDER_TYPE_SELL",
        )


class OrderSendAskRule:
    rule_id = "RULE-TRADE-003"
    _replacement = "SymbolInfoDouble(Symbol(), SYMBOL_ASK)"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        results: list[RuleResult] = []
        output: list[str] = []

        for line_num, line in enumerate(source.splitlines(keepends=True), 1):
            if "OrderSend" not in line or not _ASK_TOKEN.search(line):
                output.append(line)
                continue

            new_line = _ASK_TOKEN.sub(self._replacement, line)
            if new_line != line:
                results.append(
                    RuleResult(
                        rule_id=self.rule_id,
                        line=line_num,
                        severity="auto",
                        message=(
                            "Replaced Ask price argument in OrderSend with "
                            "SymbolInfoDouble(Symbol(), SYMBOL_ASK)"
                        ),
                        before=line.strip(),
                        after=new_line.strip(),
                    )
                )
            output.append(new_line)

        return "".join(output), results
