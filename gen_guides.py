#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成全部工具的使用教程（SEO 长尾页）：
  - 每个工具一篇 {slug}-guide.html，含 FAQ 富媒体结构 + 链回工具页 + 链向相关工具
  - 两篇支柱型指南（免费工具推荐 / 隐私保护）
  - 全部纳入 sitemap/atom/Hub（由 build.py 自动读取 blog 目录）
复用 build.py 的 ALL_TOOLS / BASE / SHARED_CSS，保证风格一致。
"""
import os, json, datetime, shutil
import build  # 复用常量（导入时会先生成一遍页面，无副作用）

ROOT = build.ROOT
BASE = build.BASE
BLOG = os.path.join(ROOT, "blog")
os.makedirs(BLOG, exist_ok=True)

# 清空旧教程（避免命名变更后残留死链）
for fn in os.listdir(BLOG):
    if fn.endswith(".html"):
        os.remove(os.path.join(BLOG, fn))

TODAY = datetime.datetime.utcnow().strftime("%Y-%m-%d")
SHARED_CSS = build.SHARED_CSS

# 每篇工具教程的专属文案；缺失则走通用模板
SPEC = {
    "compress": dict(extra="压缩时采用浏览器原生画质调节，可在体积与清晰度之间自由权衡，适合公众号配图、网页素材瘦身。"),
    "jsonfmt": dict(extra="支持折叠层级与错误定位，粘贴一段格式混乱的 JSON 即可一键美化，便于阅读接口返回数据。"),
    "pdf": dict(extra="PDF 压缩与转图片都在本地完成，敏感合同、证件类文件无需担心上传泄露。"),
    "qrcode": dict(extra="可把网址、WiFi 账号密码、文本内容生成二维码，保存为 PNG 后打印或分享都很方便。"),
    "convert": dict(extra="覆盖长度、重量、温度、面积等常见单位，输入即换算，适合海淘、烹饪、工程场景。"),
    "password": dict(extra="可设定长度与是否包含符号，生成的高强度密码适合作为各网站独立密码。"),
}

def faq_json(items):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    }, ensure_ascii=False)

def art_json(title, desc):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Organization", "name": "零成本工具箱"},
        "publisher": {"@type": "Organization", "name": "零成本工具箱"},
        "datePublished": TODAY,
        "dateModified": TODAY
    }, ensure_ascii=False)

def related_links(slug):
    slugs = [s for s, *_ in build.ALL_TOOLS]
    idx = slugs.index(slug)
    n = len(slugs)
    picks = [(idx + 2 + i) % n for i in range(3)]
    items = "".join(
        f'  <a class="card" href="../{build.ALL_TOOLS[p][0]}/"><h3>{build.ALL_TOOLS[p][1]}</h3><p>{build.ALL_TOOLS[p][2]}</p></a>'
        for p in picks)
    return f'<div class="related"><h2>你也可能用得到</h2><div class="cards">\n{items}\n</div></div>'

def tool_guide(slug, title, desc, keywords):
    spec = SPEC.get(slug, {})
    extra = spec.get("extra", f"它专注于「{desc}」，适合日常办公、开发与学习中的高频小任务。")
    kw = "、".join(keywords.split(",")[:3])
    p1 = (f"如果你正在找一款好用的{title}，这篇指南带你从打开到上手一气呵成。"
          f"{title}是一款完全免费的在线工具，所有计算与处理都在你的浏览器本地完成，数据不会上传到任何服务器。")
    p2 = (f"相比需要下载安装的桌面软件，在线{title}打开网页即用、跨平台、不占空间。本文介绍的{title}{extra}")
    steps = [
        f"进入 {title} 页面（可在站点首页点对应卡片，或直接访问本页顶部的工具入口）。",
        "在输入框中粘贴或输入需要处理的内容。",
        "点击页面上的功能按钮，结果会即时显示，无需等待。",
        "如需留存，使用「复制」或「下载」按钮保存结果。",
        "全程无需注册登录，关闭页面即结束，不留任何痕迹。",
    ]
    faqs = [
        (f"{title}需要付费或注册吗？", "不需要。本工具完全免费，且无需注册登录，打开即用。"),
        (f"{title}会保存我处理的数据吗？", "不会。所有处理都在你的浏览器本地运行，数据不会被上传或存储到任何服务器。"),
        (f"{title}在手机上能用吗？", "支持。页面采用响应式设计，手机、平板、电脑均可正常使用。"),
        (f"处理失败了怎么办？", "请检查输入格式是否符合要求；若仍失败，刷新页面后重试即可。"),
    ]
    return render(f"{title}使用指南", desc, p1, p2, steps, faqs,
                  back_link=f'<p><a href="../{slug}/">→ 直接使用{title}</a></p>',
                  related=related_links(slug))

def render(title, desc, p1, p2, steps, faqs, back_link="", related=""):
    step_html = "<ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"
    faq_html = "".join(f"<div class=\"faq\"><p class=\"q\">{q}</p><p class=\"a\">{a}</p></div>" for q, a in faqs)
    faq_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                       "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }, ensure_ascii=False)
    art_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Organization", "name": "零成本工具箱"},
        "publisher": {"@type": "Organization", "name": "零成本工具箱"},
        "datePublished": TODAY,
        "dateModified": TODAY
    }, ensure_ascii=False)
    url = BASE + "blog/" + (title_to_file(title) if False else "")
    canonical = None  # 由调用处传入
    return dict(
        title=title, desc=desc,
        body=f'''<p>{p1}</p>
<p>{p2}</p>
<h2>如何使用</h2>
{step_html}
{back_link}
<h2>常见问题</h2>
{faq_html}
{related}''',
        faq_ld=faq_ld, art_ld=art_ld)

def title_to_file(t): return t

# 单独写文件的函数
def write_guide(filename, title, desc, body, faq_ld, art_ld, canonical):
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:image" content="../og.png">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="../atom.xml">
<script type="application/ld+json">{art_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
<style>{SHARED_CSS}</style>
</head>
<body>
<header><a class="logo" href="../">零成本工具箱</a><nav><a href="../">全部工具</a></nav></header>
<main>
<h1>{title}</h1>
<p class="lead">{desc}</p>
{body}
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，支持作者持续做免费工具</span>
    <img src="../wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
</div>
</main>
<footer>© 零成本工具箱 · 免费 · 本地运行 · 隐私优先</footer>
</body>
</html>'''
    with open(os.path.join(BLOG, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("guide ->", filename)

count = 0
for slug, title, desc, keywords in build.ALL_TOOLS:
    g = tool_guide(slug, title, desc, keywords)
    filename = f"{slug}-guide.html"
    canonical = BASE + "blog/" + filename
    write_guide(filename, g["title"], g["desc"], g["body"], g["faq_ld"], g["art_ld"], canonical)
    count += 1

# 支柱型指南 1：免费在线工具推荐
pillar1_body = '''<p>零成本工具箱汇集了 {n} 款完全免费的在线工具，全部在浏览器本地运行，不上传数据、不打水印、不弹广告。</p>
<h2>为什么选在线工具</h2>
<ol><li>打开网页即用，无需下载安装。</li><li>跨平台，手机电脑都能用。</li><li>本地处理，隐私更有保障。</li><li>永久免费，无功能阉割。</li></ol>
<h2>热门工具一览</h2>
<div class="cards">
{cards}
</div>
<p><a href="../">→ 进入工具箱首页</a></p>'''.format(
    n=len(build.ALL_TOOLS),
    cards="".join(f'  <a class="card" href="../{s}/"><h3>{t}</h3><p>{d}</p></a>' for s, t, d, k in build.ALL_TOOLS))
write_guide("free-tools-guide.html", "免费在线工具推荐合集",
            "精选多款完全免费、本地运行的在线工具，覆盖图片、文本、开发、办公场景。",
            pillar1_body,
            faq_json([("这些工具真的免费吗？", "全部免费，且无需注册。"),
                      ("数据安全吗？", "所有处理在浏览器本地完成，数据不上传。")]),
            art_json("免费在线工具推荐合集", "精选免费在线工具"),
            BASE + "blog/free-tools-guide.html")
count += 1

# 支柱型指南 2：隐私保护
pillar2_body = '''<p>使用在线工具时，最让人担心的往往是隐私。本文介绍如何判断并安全地使用在线工具，避免敏感数据泄露。</p>
<h2>判断工具是否安全</h2>
<ol><li>看是否「本地运行」：纯前端工具不会把你的数据发到服务器。</li><li>优先选择开源、可自查代码的工具。</li><li>涉及证件、合同等敏感文件时，确认不上传。</li></ol>
<h2>本站的隐私做法</h2>
<p>零成本工具箱所有工具均为纯前端实现，处理过程完全在你的浏览器内完成，文件与文本不会被上传到任何服务器，关闭页面即结束。</p>
<p><a href="../">→ 浏览全部本地运行工具</a></p>'''
write_guide("privacy-guide.html", "如何安全使用在线工具保护隐私",
            "教你判断在线工具是否安全，以及本站纯前端工具如何保护你的数据隐私。",
            pillar2_body,
            faq_json([("在线工具会窃取我的数据吗？", "纯前端工具不会上传数据；使用前应确认工具是否本地运行。"),
                      ("敏感文件能用在线工具处理吗？", "应选择明确本地运行、不上传的工具，如本站的 PDF、图片压缩等。")]),
            art_json("如何安全使用在线工具保护隐私", "在线工具隐私保护指南"),
            BASE + "blog/privacy-guide.html")
count += 1

print(f"ALL GUIDES DONE: {count} 篇")
