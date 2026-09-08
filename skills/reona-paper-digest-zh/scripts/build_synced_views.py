#!/usr/bin/env python3
"""Build matching standalone-reader and WeChat-copy preview pages.

Both pages embed the exact same #wechat-content HTML. The visible controls live
outside that element, so the preview's copy button copies only article content.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
from pathlib import Path
import re
import sys

import yaml


def resolve_cover(article_dir: Path, cover_value: str) -> Path:
    cover = Path(cover_value)
    candidates = [
        cover if cover.is_absolute() else article_dir / cover,
        article_dir.parents[1] / cover,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(
        "Cover not found. Checked: " + ", ".join(str(p) for p in candidates)
    )


def data_url(path: Path) -> str:
    suffix = path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix)
    if not mime:
        raise ValueError(f"Unsupported cover format: {path.suffix}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_content(meta: dict, article_fragment: str, cover_url: str) -> str:
    title = html.escape(str(meta["title"]))
    subtitle = html.escape(str(meta.get("subtitle", "")))
    article_number = int(meta.get("article_number", 0))
    series = html.escape(str(meta.get("series", "论文精读")))
    label = f"{series} · {article_number:03d}" if article_number else series

    header = f'''<section class="wechat-article-header" style="font-family: 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', Arial, sans-serif;color: #172238;background: #ffffff;">
<img class="wechat-cover" src="{cover_url}" alt="{title}封面" style="display: block;width: 100%;height: auto;margin: 0;" />
<section style="padding: 30px 28px 24px;border-bottom: 1px solid #e8e6ee;">
<p style="margin: 0 0 13px;color: #7854ab;font-size: 14px;line-height: 1.6;letter-spacing: 2px;">{label}</p>
<p style="margin: 0 0 10px;color: #172238;font-size: 28px;line-height: 1.5;font-weight: 700;text-align: left;">{title}</p>
<p style="margin: 0;color: #67728a;font-size: 15px;line-height: 1.8;text-align: left;">{subtitle}</p>
</section>
</section>'''
    return header + "\n" + article_fragment


SHELL_CSS = r'''
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:#eff0f5;color:#172238;font-family:"Microsoft YaHei","PingFang SC","Noto Sans CJK SC",Arial,sans-serif}
.actionbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;padding:12px 16px;background:#fff;border-bottom:1px solid #ddd}
.actionbar button{font:inherit;cursor:pointer;border:1px solid #d7d0e4;background:#f5f1fb;color:#5b3c87;border-radius:7px;padding:8px 14px}
.actionbar .primary{border-color:#0f4c81;background:#0f4c81;color:#fff}
.status{font-size:13px;color:#6f7b8d}
.page{max-width:757px;margin:28px auto 60px;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 10px 40px #1222440a}
#wechat-content>.container,#wechat-content>p+section.container{padding:24px 40px 36px}
#wechat-content img{max-width:100%}
#wechat-content .wechat-cover{width:100%;max-width:none}
dialog{border:0;border-radius:12px;padding:0;width:min(96vw,1800px);max-width:none;height:94vh;background:#f7f8fc}
dialog::backdrop{background:#0b142cdd}
.dialogbar{display:flex;gap:12px;padding:12px 16px;align-items:center;border-bottom:1px solid #ddd;background:#fff;height:63px}
.dialogbar span{flex:1;font-size:13px;color:#5e6d82}
.image-scroll{height:calc(100% - 63px);overflow:auto;padding:16px;text-align:center}
#zoom-image{max-width:100%;height:auto;background:#fff;vertical-align:top}
#zoom-image.original{max-width:none}
@media(max-width:600px){body{background:#fff}.page{margin:0;border-radius:0;box-shadow:none}.actionbar{padding:10px 12px}.status{font-size:12px}#wechat-content>.container,#wechat-content>p+section.container{padding:20px}.wechat-article-header>section{padding:26px 20px 22px!important}.wechat-article-header>section>p:nth-child(2){font-size:25px!important}.dialogbar{padding:8px;gap:6px}.dialogbar span{font-size:11px}.actionbar button,.dialogbar button{padding:8px 10px;font-size:13px}}
'''


def shell(*, title: str, content: str, digest: str, mode: str) -> str:
    is_preview = mode == "preview"
    button_text = "📋 复制完整微信富文本" if is_preview else "复制完整文章"
    hint = "复制内容包含封面、栏目、标题、副标题和正文" if is_preview else "点击论文插图可放大阅读"
    zoom = "" if is_preview else '''
<dialog id="image-dialog" aria-label="论文插图放大视图">
<div class="dialogbar"><span id="image-label">论文插图</span><button id="toggle-size" type="button">原始尺寸</button><button id="close-dialog" type="button">关闭</button></div>
<div class="image-scroll"><img id="zoom-image" alt="放大的论文插图" /></div>
</dialog>'''
    zoom_script = "" if is_preview else r'''
const dialog=document.getElementById('image-dialog'),zoom=document.getElementById('zoom-image'),toggle=document.getElementById('toggle-size');
document.querySelectorAll('#wechat-content .container img').forEach(img=>img.addEventListener('click',()=>{zoom.src=img.src;zoom.alt=img.alt;zoom.classList.remove('original');toggle.textContent='原始尺寸';document.getElementById('image-label').textContent=img.alt||'论文插图';dialog.showModal()}));
document.getElementById('close-dialog').addEventListener('click',()=>dialog.close());
toggle.addEventListener('click',()=>{const original=zoom.classList.toggle('original');toggle.textContent=original?'适应宽度':'原始尺寸'});'''
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{html.escape(title)}</title>
<style>{SHELL_CSS}</style>
</head>
<body data-view="{mode}" data-content-sha256="{digest}">
<div class="actionbar"><button class="primary" id="copy" type="button">{button_text}</button><span class="status" id="copy-status">{hint}</span></div>
<main class="page"><div id="wechat-content" data-content-sha256="{digest}">{content}</div></main>
{zoom}
<script>
window.__INNER__=document.getElementById('wechat-content').innerHTML;
document.getElementById('copy').addEventListener('click',async()=>{{
  const content=document.getElementById('wechat-content'),status=document.getElementById('copy-status');
  try{{await navigator.clipboard.write([new ClipboardItem({{'text/html':new Blob([content.innerHTML],{{type:'text/html'}}),'text/plain':new Blob([content.innerText],{{type:'text/plain'}})}})]);status.textContent='✅ 已复制，可到公众号编辑器粘贴';status.style.color='#2e7d32'}}
  catch(error){{const selection=getSelection();selection.removeAllRanges();const range=document.createRange();range.selectNodeContents(content);selection.addRange(range);status.textContent='复制权限不可用，正文已选中，请按 Ctrl+C';status.style.color='#b45309'}}
}});
{zoom_script}
</script>
</body>
</html>'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("article_dir", type=Path)
    parser.add_argument(
        "--screenshot",
        action="store_true",
        help="Capture the synchronized preview page as dist/preview.png.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify that existing reading.html and preview.html share identical content.",
    )
    return parser.parse_args()


def extract_content(document: str) -> str:
    match = re.search(
        r'<div id="wechat-content"[^>]*>(.*)</div></main>', document, re.S
    )
    if not match:
        raise ValueError("Missing #wechat-content")
    return match.group(1)


def verify(dist: Path) -> str:
    reading = (dist / "reading.html").read_text(encoding="utf-8")
    preview = (dist / "preview.html").read_text(encoding="utf-8")
    reading_content = extract_content(reading)
    preview_content = extract_content(preview)
    if reading_content != preview_content:
        raise AssertionError("reading.html and preview.html contain different article HTML")
    digest = hashlib.sha256(reading_content.encode("utf-8")).hexdigest()
    for name, document in (("reading.html", reading), ("preview.html", preview)):
        marker = re.search(r'data-content-sha256="([0-9a-f]{64})"', document)
        if not marker or marker.group(1) != digest:
            raise AssertionError(f"{name} has a missing or stale content hash")
    return digest


def main() -> None:
    args = parse_args()
    article_dir = args.article_dir.resolve()
    dist = article_dir / "dist"
    if args.verify_only:
        digest = verify(dist)
        print(f"PASS synchronized content {digest}")
        return

    meta = yaml.safe_load((article_dir / "meta.yaml").read_text(encoding="utf-8"))
    missing = [key for key in ("title", "cover_image") if not meta.get(key)]
    if missing:
        raise ValueError("Missing meta fields: " + ", ".join(missing))
    article_fragment = (dist / "article.html").read_text(encoding="utf-8")
    cover = resolve_cover(article_dir, str(meta["cover_image"]))
    content = build_content(meta, article_fragment, data_url(cover))
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()

    reading = shell(
        title=f'{meta["title"]} · 独立阅读页', content=content, digest=digest, mode="reading"
    )
    preview = shell(
        title=f'{meta["title"]} · 微信公众号预览', content=content, digest=digest, mode="preview"
    )
    dist.mkdir(parents=True, exist_ok=True)
    (dist / "reading.html").write_text(reading, encoding="utf-8")
    (dist / "preview.html").write_text(preview, encoding="utf-8")
    verified = verify(dist)
    if args.screenshot:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Playwright is required for --screenshot; rerun without that option or use the ReoNa environment."
            ) from exc
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 900, "height": 1000})
            page.goto((dist / "preview.html").as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.screenshot(path=str(dist / "preview.png"), full_page=True)
            browser.close()
    print(f"PASS built synchronized views {verified}")
    print(dist / "reading.html")
    print(dist / "preview.html")
    if args.screenshot:
        print(dist / "preview.png")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise
