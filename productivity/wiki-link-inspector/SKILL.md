---
name: wiki-link-inspector
description: 本地 wiki 路由侦探：检查所有 HTML 内部链接有效性、找出 404 链接、生成站点地图。重构目录后验证链接、发现死链时批量检查、需要完整站点地图时使用。
trigger_patterns:
  - "检查.*链接"
  - "路由侦探"
  - "找.*404"
  - "生成.*站点地图"
  - "wiki.*链接检查"
tags: [wiki, html, link-check, sitemap]
---

# Wiki Link Inspector

一键检查本地 wiki 的所有 HTML 链接，生成失效链接报告和站点地图。

## 何时使用

- 重构目录结构后，验证链接是否都更新了
- 发现某个链接 404，想批量检查其他页面
- 需要一个完整的站点地图

## 执行

直接用 `execute_code` 运行以下脚本（需要 beautifulsoup4）：

```python
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict
import html as html_escape

wiki_root = Path.home() / "wiki"

# 检查依赖
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ 缺少 beautifulsoup4，正在安装...")
    import subprocess
    subprocess.check_call(['pip3', 'install', 'beautifulsoup4'])
    from bs4 import BeautifulSoup
    print("✓ 安装完成")

# 1. 扫描并提取链接
all_links = {}
for html_file in wiki_root.rglob("*.html"):
    try:
        with open(html_file, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        links = []
        for tag in soup.find_all(['a', 'link']):
            href = tag.get('href')
            if href and not href.startswith(('http://', 'https://', '#', 'mailto:', 'javascript:')):
                links.append(href)
            elif href and href.startswith('http://localhost:8765'):
                links.append(href.replace('http://localhost:8765', ''))
        
        if links:
            all_links[str(html_file.relative_to(wiki_root))] = links
    except Exception as e:
        print(f"Error parsing {html_file}: {e}")

print(f"✓ 扫描了 {len(all_links)} 个文件")

# 2. 验证链接
broken_links = []
for source, targets in all_links.items():
    source_path = wiki_root / source
    source_dir = source_path.parent
    
    for target in targets:
        target_file = target.split('#')[0]
        if not target_file:
            continue
        
        if target_file.startswith('/'):
            resolved = wiki_root / target_file.lstrip('/')
        else:
            resolved = (source_dir / target_file).resolve()
        
        if not resolved.exists():
            broken_links.append({
                'source': source,
                'target': target,
                'resolved': str(resolved.relative_to(wiki_root)) if wiki_root in resolved.parents else str(resolved),
                'reason': 'File not found'
            })

print(f"✓ 发现 {len(broken_links)} 个失效链接")

# 3. 生成站点地图
sitemap = defaultdict(list)
for html_file in sorted(wiki_root.rglob("*.html")):
    rel_path = html_file.relative_to(wiki_root)
    directory = str(rel_path.parent) if rel_path.parent != Path('.') else '根目录'
    sitemap[directory].append({
        'name': html_file.name,
        'path': str(rel_path),
        'size': html_file.stat().st_size,
        'url': f"http://localhost:8765/{rel_path}"
    })

sitemap_html = ['<!DOCTYPE html><html><head><meta charset="UTF-8"><title>站点地图</title>']
sitemap_html.append('<style>body{font-family:sans-serif;max-width:1000px;margin:40px auto;line-height:1.8}')
sitemap_html.append('h1{color:#2c5282}h2{color:#4a5568;margin-top:30px;border-bottom:2px solid #e2e8f0;padding-bottom:8px}')
sitemap_html.append('ul{list-style:none;padding-left:0}li{margin:8px 0}')
sitemap_html.append('a{color:#3182ce;text-decoration:none}a:hover{text-decoration:underline}')
sitemap_html.append('.meta{color:#718096;font-size:0.9em;margin-left:10px}</style></head><body>')
sitemap_html.append(f'<h1>Wiki 站点地图</h1><p>共 {sum(len(files) for files in sitemap.values())} 个文件</p>')

for directory in sorted(sitemap.keys()):
    sitemap_html.append(f'<h2>📁 {html_escape.escape(directory)}</h2><ul>')
    for file_info in sorted(sitemap[directory], key=lambda x: x['name']):
        size_kb = file_info['size'] / 1024
        sitemap_html.append(f"<li><a href=\"{html_escape.escape(file_info['url'])}\">{html_escape.escape(file_info['name'])}</a>")
        sitemap_html.append(f"<span class=\"meta\">({size_kb:.1f} KB)</span></li>")
    sitemap_html.append('</ul>')

sitemap_html.append('</body></html>')

with open(wiki_root / 'sitemap.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sitemap_html))

# 4. 生成报告
total_files = len(all_links)
total_links = sum(len(targets) for targets in all_links.values())
broken_count = len(broken_links)

report = ['<!DOCTYPE html><html><head><meta charset="UTF-8"><title>链接检查报告</title>']
report.append('<style>body{font-family:sans-serif;max-width:1200px;margin:40px auto;line-height:1.8}')
report.append('h1{color:#2c5282}h2{color:#4a5568;margin-top:30px}')
report.append('.summary{background:#e6fffa;padding:20px;border-radius:8px;margin:20px 0}')
report.append('.broken{background:#fff5f5;padding:15px;margin:10px 0;border-left:4px solid #f56565;border-radius:4px}')
report.append('.ok{color:#38a169}.error{color:#e53e3e}code{background:#edf2f7;padding:2px 6px;border-radius:3px}')
report.append('</style></head><body>')

report.append('<h1>📊 Wiki 链接检查报告</h1>')
report.append(f'<div class="summary">')
report.append(f'<p><strong>总文件数：</strong>{total_files}</p>')
report.append(f'<p><strong>总链接数：</strong>{total_links}</p>')
if broken_count == 0:
    report.append(f'<p class="ok"><strong>✓ 所有链接有效！</strong></p>')
else:
    report.append(f'<p class="error"><strong>✗ 发现 {broken_count} 个失效链接</strong></p>')
report.append('</div>')

if broken_count > 0:
    report.append('<h2>🔴 失效链接清单</h2>')
    for link in broken_links[:100]:  # 只显示前100个，避免报告过大
        report.append('<div class="broken">')
        report.append(f'<p><strong>源文件：</strong><code>{html_escape.escape(link["source"])}</code></p>')
        report.append(f'<p><strong>目标链接：</strong><code>{html_escape.escape(link["target"])}</code></p>')
        report.append(f'<p><strong>解析路径：</strong><code>{html_escape.escape(link["resolved"])}</code></p>')
        report.append('</div>')
    if broken_count > 100:
        report.append(f'<p>... 还有 {broken_count - 100} 个失效链接未显示</p>')

report.append('<h2>📄 站点地图</h2>')
report.append('<p><a href="sitemap.html">查看完整站点地图</a></p>')

report.append('</body></html>')

with open(wiki_root / 'link-check-report.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print(f"\n✓ 检查完成")
print(f"  报告: http://localhost:8765/link-check-report.html")
print(f"  站点地图: http://localhost:8765/sitemap.html")
```

## 如何修复失效链接

看报告后，常见修复策略：

### 1. 相对路径错误

**问题**：`lessons/量表汇总笔记.html` 里写了 `论文索引.html`，但实际文件在 `~/wiki/论文索引.html`（上一级）

**修复**：
```python
# 批量修正相对路径
from pathlib import Path
from hermes_tools import patch

wiki_root = Path.home() / "wiki"
broken_file = wiki_root / "lessons/量表汇总笔记.html"

patch(
    path=str(broken_file),
    old_string='href="论文索引.html"',
    new_string='href="../论文索引.html"',
    replace_all=True
)
```

### 2. 文件已删除

**问题**：链接指向 `deDiegoRuiz2024/lesson.html`，但该文件不存在

**修复选项**：
- 删除链接：在源文件中找到该链接并删除
- 恢复文件：如果是误删，从备份/Git 恢复
- 重定向：把链接改为指向新位置

### 3. 批量修复同类问题

**示例**：所有 `lessons/*.html` 里的 `论文索引.html` 都应该是 `../论文索引.html`

```python
from pathlib import Path
from hermes_tools import search_files, patch

wiki_root = Path.home() / "wiki"

# 找到所有有问题的文件
result = search_files(
    pattern='href="论文索引.html"',
    path=str(wiki_root / "lessons"),
    file_glob="*.html"
)

# 批量修复
for match in result['matches']:
    file_path = match['path']
    patch(
        path=file_path,
        old_string='href="论文索引.html"',
        new_string='href="../论文索引.html"',
        replace_all=True
    )
    print(f"✓ 修复 {file_path}")
```

## 输出

- `~/wiki/link-check-report.html` - 失效链接报告
- `~/wiki/sitemap.html` - 完整站点地图

访问：http://localhost:8765/link-check-report.html

## 依赖

自动安装 beautifulsoup4（如果缺失）。
