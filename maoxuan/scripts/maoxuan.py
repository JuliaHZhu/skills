#!/usr/bin/env python3
"""
maoxuan.py — 毛选逐篇蒸馏的机械层脚本（爬取/提取/状态跟踪）。

职责边界（重要）：
  - 脚本只做机械活：fetch(抓取+抽正文) / status(进度) / next(下一篇)。
  - "蒸馏成 skill"（cangjie RIA 六段 + 核对交互）是 agent 的活，不是脚本的活。
  - 脚本不生成 SKILL.md，只准备原文和跟踪状态。

用法：
  python3 maoxuan.py fetch <slug>     # 抓一篇 → raw/<slug>.md，标记 fetched
  python3 maoxuan.py next            # 下一篇未蒸馏的 slug
  python3 maoxuan.py status          # 进度总览
  python3 maoxuan.py mark <slug> <st># 手动改状态 fetched|distilled
"""

import json, re, html, subprocess, sys, os, time, random, urllib.parse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../maoxuan/
RAW = os.path.join(REPO, "raw")
MANIFEST = os.path.join(REPO, "MANIFEST.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
BASE = "https://maoxuan.app"


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(items):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


def find_item(items, slug):
    for it in items:
        if it["slug"] == slug:
            return it
    return None


def curl(url):
    """抓 HTML，失败重试 3 次带退避。"""
    for attempt in range(3):
        try:
            r = subprocess.run(
                ["curl", "-s", "--compressed", "--max-time", "30",
                 "--connect-timeout", "10", "-A", UA, url],
                capture_output=True, timeout=40)
            if r.returncode == 0 and len(r.stdout) > 5000:
                return r.stdout.decode("utf-8", errors="replace")
        except Exception:
            pass
        time.sleep(2 + attempt * 3)
    return None


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    # 去掉脚注标记 〔1〕 与上标引用
    s = re.sub(r"〔\s*\d+\s*〕", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


SITE_BADGE = "由maoxuan.app整理"


def extract_article(raw):
    """从文章页 HTML 抽 title / 原文段落列表（保真：剔除站方导读与站方小标题标注）。

    关键事实（两篇实测）：
    - 站方导读（"一句话概括/核心观点/阅读提示"）放在 `<aside>` 里，非原文，直接删。
    - 原文在 `prose prose-lg` 容器里；但日期段落可能单独占一个 `prose-lg`（-mb-4），
      所以不能只 find 第一个 prose-lg 就完事——正确顺序是：先删 aside，再抽 prose-lg 区。
    - 原文区内的 h2/h3 是站方加的小标题（带"该标题由maoxuan.app整理"徽标），透明标注。
    """
    m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    title = clean(m.group(1)) if m else ""

    # 1) 删掉站方导读块（<aside>...</aside>，含导读/核心观点/阅读提示/相关文章等非原文内容）
    raw = re.sub(r"<aside\b.*?</aside>", "", raw, flags=re.S)

    start = raw.find("prose prose-lg")
    if start < 0:
        # 兜底：抓所有正文段落
        paras = re.findall(r'<p class="mb-4 leading-relaxed[^"]*">(.*?)</p>', raw, re.S)
        body = [clean(p) for p in paras]
        return title, "", [p for p in body if p]

    # 原文区边界：到「注释」脚注区（或下一篇/相关文章）为止
    end = raw.find("注释", start)
    for probe in ("下一篇", "相关文章", "返回"):
        if end < 0:
            end = raw.find(probe, start)
    if end < 0:
        end = len(raw)
    region = raw[start:end]

    blocks = []  # (kind, text) 按出现顺序
    for m in re.finditer(r'<(h[234]|p|blockquote|li)\b[^>]*>(.*?)</\1>', region, re.S):
        kind, inner = m.group(1), m.group(2)
        txt = clean(inner)
        if not txt:
            continue
        if kind in ("h2", "h3"):
            site_added = SITE_BADGE in txt
            # 去掉徽标文本（"该标题/该导读由maoxuan.app整理" 等）
            txt = re.sub(r"该(标题|导读|小标题|编者)[^由]*由maoxuan\.app整理", "", txt).strip()
            blocks.append(("heading" if not site_added else "site-heading", txt))
        elif kind == "blockquote":
            blocks.append(("quote", txt))
        elif kind == "li":
            blocks.append(("li", txt))
        else:
            blocks.append(("p", txt))
    return title, "", blocks


def to_markdown(title, date, blocks):
    out = [f"# {title}", ""]
    if date:
        out += [f"> {date}", ""]
    for kind, txt in blocks:
        if kind == "p":
            out.append(txt + "\n")
        elif kind == "quote":
            out.append("> " + txt + "\n")
        elif kind == "li":
            out.append("- " + txt + "\n")
        elif kind == "heading":
            out.append(f"\n## {txt}\n")
        elif kind == "site-heading":
            out.append(f"\n**[站方小标题] {txt}**\n")
    return "\n".join(out)


def cmd_fetch(items, slug):
    it = find_item(items, slug)
    if it is None:
        print(f"未知 slug: {slug}")
        sys.exit(1)
    url = f"{BASE}/articles/{slug}"
    print(f"抓取: {it['volume']} · {it['title']}  ({slug})")
    raw = curl(url)
    if raw is None:
        print("抓取失败（3 次重试仍失败）")
        sys.exit(1)
    title, date, blocks = extract_article(raw)
    if not blocks:
        print("正文为空——可能被风控或模板不同，需人工看。")
        sys.exit(1)
    os.makedirs(RAW, exist_ok=True)
    path = os.path.join(RAW, slug + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_markdown(title, date, blocks))
    it["status"] = "fetched"
    it["chars"] = sum(len(txt) for _, txt in blocks)
    save_manifest(items)
    print(f"已存 {path}  ·  标题={title}  ·  {len(blocks)} 块 / {it['chars']} 字")


def cmd_next(items):
    for it in items:
        if it.get("status", "") != "distilled":
            print(it["order"], it["slug"], "|", it["volume"], "|", it["title"],
                  "|", it.get("status", "未抓"))
            return
    print("全部完成")


def cmd_status(items):
    from collections import Counter
    c = Counter(it.get("status", "未抓") for it in items)
    print(f"总 {len(items)} 篇：", dict(c))
    print("--- 未完成清单（menu 式，标进度）---")
    for it in items:
        if it.get("status", "") != "distilled":
            print(f"[{'✓' if it.get('status')=='fetched' else ' '}] "
                  f"{it['order']:>3} {it['volume']} {it['title']}  "
                  f"({it['slug']})")


def cmd_mark(items, slug, st):
    it = find_item(items, slug)
    if it is None:
        print(f"未知 slug: {slug}")
        sys.exit(1)
    it["status"] = st
    save_manifest(items)
    print(f"{slug} -> {st}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    items = load_manifest()
    cmd = sys.argv[1]
    if cmd == "fetch" and len(sys.argv) >= 3:
        cmd_fetch(items, sys.argv[2])
    elif cmd == "next":
        cmd_next(items)
    elif cmd == "status":
        cmd_status(items)
    elif cmd == "mark" and len(sys.argv) >= 4:
        cmd_mark(items, sys.argv[2], sys.argv[3])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
