from mql4tomql5.converter import convert_with_report
from mql4tomql5.rules.scan import ManualReviewScanRule


def test_manual_scan_finds_unconverted_ima():
    source = "double ma = iMA(NULL, 0, 14, 0, MODE_SMA, PRICE_CLOSE, 0);\n"
    _, results = ManualReviewScanRule().apply(source)
    rule_ids = {r.rule_id for r in results}
    assert "RULE-SCAN-001" in rule_ids


def test_manual_scan_ignores_converted_ima():
    source = "int ma_handle = iMA(_Symbol, PERIOD_CURRENT, 14, 0, MODE_SMA, PRICE_CLOSE);\n"
    _, results = ManualReviewScanRule().apply(source)
    assert not any(r.rule_id == "RULE-SCAN-001" for r in results)


def test_sample_converts_without_manual_review():
    source = open("examples/sample.mq4", encoding="utf-8").read()
    _, report = convert_with_report(source)
    assert report.summary["manual_required"] == 0
