"""Indicator function conversions."""

import re

from mql4tomql5.engine import RuleResult
from mql4tomql5.rules.base import line_number_at

_IMA_ASSIGN = re.compile(
    r"^(\s*)double\s+(\w+)\s*=\s*iMA\s*\(\s*NULL\s*,\s*0\s*,\s*([^,]+)\s*,\s*0\s*,"
    r"\s*MODE_SMA\s*,\s*PRICE_CLOSE\s*,\s*0\s*\)\s*;\s*$",
    re.MULTILINE,
)


class ImaCopyBufferRule:
    rule_id = "RULE-IND-001"

    def apply(self, source: str) -> tuple[str, list[RuleResult]]:
        results: list[RuleResult] = []
        converted_vars: list[str] = []

        def _replace_assignment(match: re.Match[str]) -> str:
            indent, var, period = match.group(1), match.group(2), match.group(3).strip()
            line_num = line_number_at(source, match.start())
            before = match.group(0).strip()
            block = (
                f"{indent}int {var}_handle = iMA(_Symbol, PERIOD_CURRENT, {period}, 0, MODE_SMA, PRICE_CLOSE);\n"
                f"{indent}double {var}[];\n"
                f"{indent}ArraySetAsSeries({var}, true);\n"
                f"{indent}if (CopyBuffer({var}_handle, 0, 0, 1, {var}) <= 0) return;"
            )
            converted_vars.append(var)
            results.append(
                RuleResult(
                    rule_id=self.rule_id,
                    line=line_num,
                    severity="auto",
                    message=f"Converted iMA assignment for {var} to handle + CopyBuffer pattern",
                    before=before,
                    after=block.replace("\n", " / ").strip(),
                )
            )
            return block

        converted = _IMA_ASSIGN.sub(_replace_assignment, source)

        for var in converted_vars:
            converted = self._replace_var_reads(converted, var)

        return converted, results

    def _replace_var_reads(self, source: str, var: str) -> str:
        skip_markers = (
            f"{var}_handle",
            f"double {var}[]",
            "CopyBuffer(",
            f"ArraySetAsSeries({var}",
        )
        output: list[str] = []
        read_pattern = re.compile(rf"\b{re.escape(var)}\b(?!\[)")

        for line in source.splitlines(keepends=True):
            if any(marker in line for marker in skip_markers):
                output.append(line)
            else:
                output.append(read_pattern.sub(f"{var}[0]", line))

        return "".join(output)
