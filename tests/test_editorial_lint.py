#!/usr/bin/env python3
"""Minimal regression tests for editorial rules added from real article revisions."""

import sys
from pathlib import Path


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")


SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from editorial_lint import lint_article  # noqa: E402


CHECKS = []


def check(name: str, condition: bool):
    CHECKS.append((name, bool(condition)))
    print(("PASS" if condition else "FAIL"), name)


def messages(text: str):
    return [message for _severity, message in lint_article(text)]


good = """研究未报告每个 iPSC 的 MK 产量或每个 MK 的血小板产量。

| 研究 | 产品 | 生产信息 | 证据 |
|---|---|---|---|
| Norbnop 2020 | iPSC-MK | 未报告每个 iPSC 的 MK 产量 | 检测至 24 小时 |
"""
check("准确的未报告措辞通过", not messages(good))

bad_rate = "| Norbnop 2020 | 无 MK/iPSC 或 PLT/MK |"
check("拦截无 MK/iPSC 歧义缩写", any("产率缺失表述有歧义" in m for m in messages(bad_rate)))

bad_tone = "值得注意的是，这一结果具有重要意义。"
tone_messages = messages(bad_tone)
check("拦截 AI 腔禁用表达", len([m for m in tone_messages if "禁用表达" in m]) == 2)

bad_h1 = "# 重复文章标题\n\n正文。"
check("拦截正文一级标题", any("一级标题" in m for m in messages(bad_h1)))

too_many_marks = " ".join(f"==高亮{i}==" for i in range(6))
check("拦截超过五处高亮", any("高亮共 6 处" in m for m in messages(too_many_marks)))

wide_table = "| A | B | C | D | E |\n|---|---|---|---|---|"
check("拦截超过四列表格", any("表格有 5 列" in m for m in messages(wide_table)))

latex_power = r"单次输注量约为 $3\times10^{11}$。"
check("拦截简单科学计数法的 LaTeX 写法", any("科学计数法" in m for m in messages(latex_power)))

native_power = "单次输注量约为 3×10^11^。"
check("原生上标科学计数法通过", not messages(native_power))

failed = [name for name, ok in CHECKS if not ok]
print()
if failed:
    print(f"[gate] {len(failed)} 项失败：{failed}")
    sys.exit(1)
print(f"[gate] 全部 {len(CHECKS)} 项通过")
