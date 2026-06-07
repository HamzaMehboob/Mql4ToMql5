from mql4tomql5.rules.directives import RemoveStrictPropertyRule
from mql4tomql5.rules.price import AskRule, BidRule
from mql4tomql5.rules.trade import OpBuyRule, OpSellRule, OrderSendAskRule


def test_remove_strict_property():
    source = "#property strict\n\nvoid OnTick() {}\n"
    converted, results = RemoveStrictPropertyRule().apply(source)
    assert "#property strict" not in converted
    assert len(results) == 1
    assert results[0].rule_id == "RULE-DIR-001"


def test_bid_replacement():
    source = "if (Bid > ma) { }\n"
    converted, results = BidRule().apply(source)
    assert "SymbolInfoDouble(Symbol(), SYMBOL_BID)" in converted
    assert "Bid" not in converted
    assert results[0].rule_id == "RULE-PRICE-001"


def test_bid_does_not_replace_substring():
    source = "double MyBidValue = 1;\n"
    converted, _ = BidRule().apply(source)
    assert converted == source


def test_ask_replacement():
    source = "double price = Ask;\n"
    converted, results = AskRule().apply(source)
    assert "SymbolInfoDouble(Symbol(), SYMBOL_ASK)" in converted
    assert results[0].rule_id == "RULE-PRICE-002"


def test_op_buy_replacement():
    source = "OrderSend(Symbol(), OP_BUY, 0.1, 0, 0, 0, 0, \"\", 0, 0, clrBlue);\n"
    converted, results = OpBuyRule().apply(source)
    assert "ORDER_TYPE_BUY" in converted
    assert "OP_BUY" not in converted
    assert results[0].rule_id == "RULE-TRADE-001"


def test_op_sell_replacement():
    source = "OrderSend(Symbol(), OP_SELL, 0.1, 0, 0, 0, 0, \"\", 0, 0, clrBlue);\n"
    converted, results = OpSellRule().apply(source)
    assert "ORDER_TYPE_SELL" in converted
    assert results[0].rule_id == "RULE-TRADE-002"


def test_order_send_ask_replacement():
    source = 'OrderSend(Symbol(), OP_BUY, 0.1, Ask, 2, 0, 0, "", 0, 0, clrBlue);\n'
    converted, results = OrderSendAskRule().apply(source)
    assert "SymbolInfoDouble(Symbol(), SYMBOL_ASK)" in converted
    assert results[0].rule_id == "RULE-TRADE-003"
