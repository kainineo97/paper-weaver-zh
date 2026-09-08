"""Deterministic editorial checks for ReoNa paper-digest articles."""

import re


BANNED_TONE_PATTERNS = {
    "值得注意的是": r"值得注意的是",
    "不难发现": r"不难发现",
    "由此可见": r"由此可见",
    "综上所述": r"综上所述",
    "毋庸置疑": r"毋庸置疑",
    "深刻揭示": r"深刻揭示",
    "具有重要意义": r"具有重要意义",
    "深远影响": r"深远影响",
    "随着……的发展": r"随着[^。；\n]{0,24}的发展",
    "近年来……引起广泛关注": r"近年来[^。；\n]{0,24}引起(?:了)?广泛关注",
    "相信在未来": r"相信在未来",
    "让我们共同期待": r"让我们共同期待",
}

# “无 MK/iPSC”通常想表达“论文未报告该产率”，但字面含义会被理解为
# 没有生成 MK。只拦截带斜杠的拉丁字母产率缩写，不影响“无显著差异”等正常表述。
AMBIGUOUS_MISSING_RATE_RE = re.compile(
    r"(?<!\w)无\s*[A-Za-zβΒ][A-Za-zβΒ0-9+^_-]*\s*/\s*"
    r"[A-Za-zβΒ][A-Za-zβΒ0-9+^_-]*"
)

SIMPLE_SCI_NOTATION_LATEX_RE = re.compile(
    r"\$\s*\d+(?:\.\d+)?\s*\\times\s*10\^\{[-+]?\d+\}\s*\$"
)


def _strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def _table_column_issues(text: str):
    issues = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell for cell in re.split(r"(?<!\\)\|", stripped)[1:-1]]
        if len(cells) > 4:
            issues.append(
                ("error", f"第 {line_no} 行表格有 {len(cells)} 列；移动端表格最多 4 列")
            )
    return issues


def lint_article(text: str):
    """Return a list of ``(severity, message)`` editorial issues."""
    prose = _strip_fenced_code(text)
    issues = []

    if re.search(r"(?m)^#(?!#)\s+", prose):
        issues.append(("error", "正文含一级标题；文章标题应只由 meta.yaml.title 提供"))

    highlight_count = len(re.findall(r"==[^=\n]+==", prose))
    if highlight_count > 5:
        issues.append(("error", f"高亮共 {highlight_count} 处；每篇最多 5 处"))

    for label, pattern in BANNED_TONE_PATTERNS.items():
        if re.search(pattern, prose):
            issues.append(("error", f"命中 AI 腔禁用表达：{label}"))

    ambiguous_rates = AMBIGUOUS_MISSING_RATE_RE.findall(prose)
    if ambiguous_rates:
        examples = "、".join(dict.fromkeys(match.strip() for match in ambiguous_rates))
        issues.append(
            (
                "error",
                f"产率缺失表述有歧义：{examples}；请改为“未报告每个 X 的 Y 产量”",
            )
        )

    simple_latex_powers = SIMPLE_SCI_NOTATION_LATEX_RE.findall(prose)
    if simple_latex_powers:
        examples = "、".join(dict.fromkeys(simple_latex_powers))
        issues.append(
            (
                "error",
                f"简单科学计数法不应使用 LaTeX：{examples}；请改为“3×10^11^”式原生上标",
            )
        )

    issues.extend(_table_column_issues(prose))
    return issues
