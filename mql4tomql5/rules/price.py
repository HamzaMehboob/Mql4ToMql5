"""Price constant conversions."""

from mql4tomql5.engine import RuleResult
from mql4tomql5.rules.base import replace_word


class BidRule:
    rule_id = "RULE-PRICE-001"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        return replace_word(
            source,
            "Bid",
            "SymbolInfoDouble(Symbol(), SYMBOL_BID)",
            self.rule_id,
            "Replaced Bid with SymbolInfoDouble(Symbol(), SYMBOL_BID)",
        )


class AskRule:
    rule_id = "RULE-PRICE-002"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        return replace_word(
            source,
            "Ask",
            "SymbolInfoDouble(Symbol(), SYMBOL_ASK)",
            self.rule_id,
            "Replaced Ask with SymbolInfoDouble(Symbol(), SYMBOL_ASK)",
        )
