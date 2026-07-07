#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 6 篇长尾 SEO 指南到 blog/，每篇链回对应工具，含 FAQ 与 JSON-LD。"""
import os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://ckstc.github.io/zero-cost-tools/"
BLOG = os.path.join(ROOT, "blog")
os.makedirs(BLOG, exist_ok=True)

SHARED_CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1f2430;--muted:#6b7280;--brand:#2f6df6;--brand-d:#1f4fc4;--line:#e6e8ec}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}
header{background:var(--card);border-bottom:1px solid var(--line);padding:14px 20px;position:sticky;top:0;z-index:5}
header .logo{font-weight:700;color:var(--brand);text-decoration:none;font-size:18px}
header nav a{color:var(--muted);text-decoration:none;font-size:14px;margin-left:12px}
main{max-width:820px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:28px;margin:0 0 8px}
h2{font-size:21px;margin:28px 0 10px;border-left:4px solid var(--brand);padding-left:10px}
.lead{color:var(--muted);margin:0 0 20px}
p{margin:0 0 14px}
.cta{margin:22px 0;padding:16px;background:#eef2ff;border:1px solid #dbe4ff;border-radius:12px;font-weight:600}
.cta a{color:var(--brand)}
.faq{margin-top:30px;padding-top:18px;border-top:1px dashed var(--line)}
.faq h2{border:none;padding:0}
.faq details{margin:10px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.faq summary{cursor:pointer;font-weight:600}
.faq p{margin:10px 0 0}
.support-links{margin-top:34px;padding-top:22px;border-top:1px dashed var(--line);text-align:center}
.wechat-qr-wrap{display:inline-block}
.qr-label{display:block;font-weight:600;margin-bottom:8px}
.qr-img{width:180px;height:180px;border:1px solid var(--line);border-radius:10px}
footer{text-align:center;color:var(--muted);font-size:13px;padding:24px}
"""

def make_guide(fname, title, desc, keywords, h1, lead, sections, faq, tool_link, tool_name):
    url = BASE + "blog/" + fname
    art = json.dumps({
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":desc,"url":url,
        "author":{"@type":"Organization","name":"零成本工具箱"},
        "publisher":{"@type":"Organization","name":"零成本工具箱"}
    }, ensure_ascii=False)
    sec_html = "\n".join(f"<h2>{h}</h2>\n{b}" for h,b in sections)
    faq_html = '<div class="faq"><h2>常见问题</h2>' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faq) + "</div>"
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{art}</script>
<style>{SHARED_CSS}</style>
</head>
<body>
<header><a class="logo" href="../">零成本工具箱</a><nav><a href="../">全部工具</a></nav></header>
<main>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{sec_html}
<div class="cta">需要随时用？打开 <a href="../{tool_link}/">{tool_name}</a> 立即在线处理，全部在浏览器本地完成。</div>
{faq_html}
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，支持作者持续做免费工具</span>
    <img src="../wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
</div>
</main>
<footer>© 零成本工具箱 · 免费 · 本地运行 · 隐私优先</footer>
</body>
</html>"""
    with open(os.path.join(BLOG, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("guide", fname)

GUIDES = {
"compress-guide.html": dict(
  title="图片压缩指南：体积减半画质不降（2026 最新方法）",
  desc="教你如何在线压缩 JPG/PNG/WebP 图片，体积减小 50%–80% 同时保持清晰，无需安装软件、不上传原图。",
  keywords="图片压缩,压缩图片,图片减肥,jpg压缩,png压缩",
  h1="图片压缩指南：体积减半，画质不降",
  lead="无论发朋友圈、做网站还是传邮件，图片太大都让人头疼。本文教你用纯浏览器工具把图片压到最小，且全程不上传你的原图。",
  sections=[
    ("为什么要压缩图片？", "<p>大图会拖慢网页加载、占满手机空间、超出平台上传限制。把图片压到合适体积，加载更快、体验更好，画质肉眼几乎看不出差别。</p>"),
    ("在线压缩的 3 个要点", "<p>① 优先用 <strong>有损压缩</strong> 处理照片类 JPEG/WebP；② 截图/插画类 PNG 可转 WebP 进一步缩小；③ 批量处理时统一目标质量（建议 70%–85%）。关键是<strong>本地处理</strong>——图片不离开你的设备，隐私无忧。</p>"),
    ("一步搞定", "<p>打开下方图片压缩工具，拖入图片，拖动质量滑块，实时预览效果，满意后下载即可。</p>"),
  ],
  faq=[
    ("压缩后画质会变差吗？", "适度压缩（质量 70% 以上）肉眼基本无感；可按需微调直到满意再下载。"),
    ("我的图片会被上传吗？", "不会。本工具在浏览器内本地处理，图片不出你的电脑。"),
  ],
  tool_link="compress", tool_name="图片压缩工具"),

"jsonfmt-guide.html": dict(
  title="JSON 格式化指南：一键美化、压缩与校验",
  desc="什么是 JSON 格式化？如何用在线工具把杂乱的 JSON 美化、压缩、校验错误，提升开发与调试效率。",
  keywords="json格式化,json美化,json校验,格式化json",
  h1="JSON 格式化指南：一键美化与校验",
  lead="后端返回的 JSON 常常挤成一行、难以阅读。本文讲清 JSON 格式化的作用，并教你用本地工具快速整理。",
  sections=[
    ("JSON 格式化是什么？", "<p>就是把结构混乱、缺少换行的 JSON 文本，按层级重新缩进、换行，让人一眼看清字段嵌套关系。</p>"),
    ("常见使用场景", "<p>① 调试接口返回数据；② 对比两份配置差异；③ 把 JSON 压缩成单行节省传输体积。格式化与压缩可一键互转。</p>"),
    ("安全提醒", "<p>含有密钥、Token 的 JSON 不要粘贴到不可信的在线网站。用<strong>本地运行</strong>的工具，数据只留在你浏览器里。</p>"),
  ],
  faq=[
    ("JSON 报错怎么定位？", "好的格式化工具会在出错位置高亮提示，按提示修正引号或逗号即可。"),
    ("支持大文件吗？", "本地工具受浏览器内存限制，一般几 MB 内流畅；超大文件建议分段。"),
  ],
  tool_link="jsonfmt", tool_name="JSON 格式化工具"),

"password-guide.html": dict(
  title="密码安全指南：如何生成高强度密码（附工具）",
  desc="弱密码是账号被盗主因。本文讲清什么是强密码、长度与字符集怎么选，并用本地生成器一键产出。",
  keywords="强密码,密码生成,密码安全,随机密码",
  h1="密码安全指南：如何生成高强度密码",
  lead="123456、生日、连续数字仍是大多数人密码。本文教你用正确姿势生成难以破解的密码。",
  sections=[
    ("强密码的三个特征", "<p>① 足够长（≥12 位）；② 混合大小写字母、数字、符号；③ 随机而非字典词。长度比复杂度更重要。</p>"),
    ("不要做的事", "<p>别用姓名、生日、单词；别所有网站同一密码；别把密码写在明处。建议每个重要账号用密码管理器存一段随机密码。</p>"),
    ("一键生成", "<p>用下方生成器，选好长度和字符集，点一下即得随机强密码，可批量生成多个。</p>"),
  ],
  faq=[
    ("多长才安全？", "12 位以上随机密码已很难暴力破解；重要账号建议 16 位。"),
    ("密码会泄露给服务器吗？", "不会，生成在浏览器本地完成，不上传。"),
  ],
  tool_link="password", tool_name="密码生成器"),

"convert-guide.html": dict(
  title="单位换算指南：长度/重量/温度/面积公式与在线工具",
  desc="厘米米英尺、公斤磅、摄氏度华氏度怎么换算？汇总常用单位换算公式，并附在线换算器。",
  keywords="单位换算,换算器,长度换算,温度换算,重量换算",
  h1="单位换算指南：常用公式与在线工具",
  lead="海淘、留学、做菜、装修都逃不开单位换算。本文汇总最常用公式，并给出一键换算工具。",
  sections=[
    ("长度", "<p>1 米 = 100 厘米 = 3.2808 英尺；1 英寸 = 2.54 厘米；1 英尺 = 30.48 厘米。</p>"),
    ("重量", "<p>1 公斤 = 2.2046 磅；1 磅 ≈ 453.6 克；1 斤 = 500 克 = 1.1023 磅。</p>"),
    ("温度", "<p>华氏 = 摄氏 × 9/5 + 32；摄氏 = (华氏 − 32) × 5/9。0℃=32℉，100℃=212℉。</p>"),
    ("面积", "<p>1 平方米 ≈ 10.764 平方英尺；1 亩 ≈ 666.7 平方米。</p>"),
  ],
  faq=[
    ("换算结果不准？", "确保选对单位类别，输入数值后工具实时给出结果。"),
    ("支持哪些类别？", "长度、重量、温度、面积等常用类别均可在线换算。"),
  ],
  tool_link="convert", tool_name="单位换算器"),

"csvjson-guide.html": dict(
  title="CSV 转 JSON 指南：在线互转方法与注意事项",
  desc="CSV 与 JSON 怎么互相转换？讲解字段映射规则，并给出本地互转工具，数据不出浏览器。",
  keywords="csv转json,json转csv,csv json 互转,格式转换",
  h1="CSV 转 JSON 指南：在线互转方法",
  lead="表格数据（CSV）和接口数据（JSON）经常要互转。本文讲清规则并给出零上传的互转工具。",
  sections=[
    ("CSV 转 JSON 怎么映射？", "<p>默认第一行为表头，作为每个对象的键；后续每行对应一个对象的值。例如表头 a,b 对应 {a:.., b:..}。</p>"),
    ("JSON 转 CSV 怎么处理？", "<p>取数组第一个对象的键作为表头，逐行写出各字段值；嵌套对象建议先展平。</p>"),
    ("为什么用本地工具？", "<p>业务数据常含敏感信息，本地处理可避免上传泄露风险。</p>"),
  ],
  faq=[
    ("带逗号的内容会出错吗？", "标准 CSV 用引号包裹含逗号的字段；本工具按逗号分隔，复杂场景建议规范转义。"),
    ("大数据量卡顿？", "极大量数据建议分批处理。"),
  ],
  tool_link="csv-json", tool_name="CSV/JSON 互转工具"),

"textdiff-guide.html": dict(
  title="文本对比指南：快速找出两段文字的差异",
  desc="如何对比两个版本的文字差异？介绍逐行 diff 原理，并附本地文本对比工具，增删一目了然。",
  keywords="文本对比,文本比较,diff,找不同",
  h1="文本对比指南：快速找出文字差异",
  lead="改了稿子、比对配置、检查翻译，都需要看清楚改了哪里。本文介绍文本对比的用法与工具。",
  sections=[
    ("逐行 diff 是什么？", "<p>把两段文本按行拆解，找出相同、新增、删除的行，并以颜色区分，快速定位改动。</p>"),
    ("典型场景", "<p>① 代码或配置改动审查；② 文章多版本比对；③ 翻译与原文核对。新增通常标绿、删除标红。</p>"),
    ("本地即可用", "<p>用下方工具粘贴两段文本，点一下即得差异高亮，无需上传。</p>"),
  ],
  faq=[
    ("支持中文吗？", "支持，按行比较，中英文均可。"),
    ("能比对整个文件吗？", "可粘贴文件内容逐行比较，适合中小篇幅。"),
  ],
  tool_link="text-diff", tool_name="文本对比工具"),
}

for f, g in GUIDES.items():
    make_guide(f, g["title"], g["desc"], g["keywords"], g["h1"], g["lead"],
               g["sections"], g["faq"], g["tool_link"], g["tool_name"])
print("ALL GUIDES DONE")
