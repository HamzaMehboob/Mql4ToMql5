from pathlib import Path

from mql4tomql5 import convert_mql4_to_mql5

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_sample_golden_conversion():
    source = (FIXTURES / "sample.mq4").read_text(encoding="utf-8")
    expected = (FIXTURES / "sample.expected.mq5").read_text(encoding="utf-8")
    assert convert_mql4_to_mql5(source) == expected


def test_idempotency():
    source = (FIXTURES / "sample.mq4").read_text(encoding="utf-8")
    once = convert_mql4_to_mql5(source)
    twice = convert_mql4_to_mql5(once)
    assert once == twice
