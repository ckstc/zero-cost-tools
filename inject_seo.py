#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 6 个手写原工具页（生成器不重写它们）补上与其他页一致的 SEO 增强：
  og:image / atom 订阅 link / BreadcrumbList 结构化数据 / 相关工具内链。
只动 <head> 与 support-links 之前的位置，不触碰功能代码。
"""
import os, json
import build

ROOT = build.ROOT
ORIGINALS = ["compress", "jsonfmt", "pdf", "qrcode", "convert", "password"]

def related_html(slug):
    slugs = [s for s, *_ in build.ALL_TOOLS]
    idx = slugs.index(slug)
    n = len(slugs)
    picks = [(idx + 1 + i) % n for i in range(4)]
    items = "".join(
        f'  <a class="card" href="../{build.ALL_TOOLS[p][0]}/"><h3>{build.ALL_TOOLS[p][1]}</h3><p>{build.ALL_TOOLS[p][2]}</p></a>'
        for p in picks)
    return f'<div class="related"><h2>相关工具</h2><div class="cards">\n{items}\n</div></div>'

for slug in ORIGINALS:
    path = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(path):
        print("skip (missing)", slug); continue
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "og:image" in html and "BreadcrumbList" in html:
        print("already done", slug); continue
    title = next(t for s, t, d, k in build.ALL_TOOLS if s == slug)
    crumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "零成本工具箱", "item": build.BASE},
            {"@type": "ListItem", "position": 2, "name": title, "item": build.BASE + slug + "/"}
        ]
    }, ensure_ascii=False)
    head_add = (
        '<meta property="og:image" content="../og.png">\n'
        '<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="../atom.xml">\n'
        f'<script type="application/ld+json">{crumb}</script>\n'
    )
    html = html.replace("</head>", head_add + "</head>", 1)
    rel = related_html(slug)
    html = html.replace('<div class="support-links">', rel + '\n  <div class="support-links">', 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("enhanced", slug)

print("DONE")
