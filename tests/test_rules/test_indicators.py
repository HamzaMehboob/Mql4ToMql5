from mql4tomql5.rules.indicators import ImaCopyBufferRule


def test_ima_copy_buffer_conversion():
    source = (
        "void OnTick() {\n"
        "    double ma = iMA(NULL, 0, MovingAveragePeriod, 0, MODE_SMA, PRICE_CLOSE, 0);\n"
        "    if (Bid > ma) { }\n"
        "}\n"
    )
    converted, results = ImaCopyBufferRule().apply(source)
    assert "iMA(NULL" not in converted
    assert "CopyBuffer(ma_handle" in converted
    assert "ma[0]" in converted
    assert "double ma =" not in converted
    assert results[0].rule_id == "RULE-IND-001"
