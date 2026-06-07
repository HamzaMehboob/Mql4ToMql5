"""Registered conversion rules in execution order."""

from mql4tomql5.engine import ConversionRule
from mql4tomql5.rules.directives import RemoveStrictPropertyRule
from mql4tomql5.rules.indicators import ImaCopyBufferRule
from mql4tomql5.rules.price import AskRule, BidRule
from mql4tomql5.rules.scan import ManualReviewScanRule
from mql4tomql5.rules.trade import OpBuyRule, OpSellRule, OrderSendAskRule

ALL_RULES: list[ConversionRule] = [
    RemoveStrictPropertyRule(),
    OpBuyRule(),
    OpSellRule(),
    OrderSendAskRule(),
    ImaCopyBufferRule(),
    BidRule(),
    AskRule(),
    ManualReviewScanRule(),
]
