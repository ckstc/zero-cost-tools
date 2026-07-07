#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全自动工具站生成器 —— 统一产出所有页面（工具页 / Hub / sitemap / atom），
保证 SEO 元数据、结构化数据、微信收款码一致。新增工具只需往 NEW_TOOLS 加数据。
"""
import os, json, datetime, uuid

BASE = "https://ckstc.github.io/zero-cost-tools/"
ROOT = os.path.dirname(os.path.abspath(__file__))

WECHAT_IMG = "wechat-qr.png"

# 全站工具清单（用于 Hub / sitemap / atom）
ALL_TOOLS = [
    ("compress",      "图片压缩工具",        "在线压缩 JPG/PNG/WebP，本地处理不上传，免费无水印", "图片压缩,压缩jpg,压缩png,图片减肥"),
    ("jsonfmt",       "JSON 格式化工具",      "在线 JSON 美化/压缩/校验，本地运行，保护隐私", "json格式化,json美化,json校验,json压缩"),
    ("pdf",           "PDF 工具箱",          "在线压缩 PDF、PDF 转图片，纯前端处理不泄露文件", "pdf压缩,pdf转图片,pdf工具"),
    ("qrcode",        "二维码生成器",         "免费生成网址/文本/ WiFi 二维码，可下载 PNG", "二维码生成,生成二维码,wifi二维码"),
    ("convert",       "单位换算器",           "长度/重量/温度/面积等单位在线换算", "单位换算,换算器,长度换算"),
    ("password",      "密码生成器",           "生成高强度随机密码，可自定义长度与字符集", "密码生成,强密码,随机密码"),
    ("word-counter",  "字数统计工具",         "实时统计中英文单词、字符、句子、行数", "字数统计,字符统计,词数统计"),
    ("case-converter", "大小写转换工具",       "英文大小写、标题化、句首大写一键转换", "大小写转换,英文大小写,标题大写"),
    ("url-codec",     "URL 编解码工具",       "在线 URL 编码/解码，处理中文与特殊字符", "url编码,url解码,百分号编码"),
    ("base64-codec",  "Base64 编解码",        "文本 Base64 编码/解码，支持中文 UTF-8", "base64,base64编码,base64解码"),
    ("timestamp",     "时间戳转换工具",       "Unix 时间戳与日期互转，支持本地/UTC", "时间戳转换,unix时间,时间戳"),
    ("markdown",      "Markdown 预览器",      "实时 Markdown 渲染预览，离线可用", "markdown预览,md编辑器,markdown"),
]

# 新工具：需生成完整页面（body + js）
NEW_TOOLS = {
    "word-counter": dict(
        h1="字数统计工具",
        lead="粘贴或输入任意文本，实时统计单词数、字符数、句子数、行数。完全在浏览器本地运行，不上传你的内容。",
        body=r'''
<textarea id="ta" placeholder="在此粘贴或输入文本…" spellcheck="false"></textarea>
<div class="stats">
  <div class="stat"><span class="num" id="s-words">0</span><span class="lbl">单词</span></div>
  <div class="stat"><span class="num" id="s-chars">0</span><span class="lbl">字符(含空格)</span></div>
  <div class="stat"><span class="num" id="s-chars-nospace">0</span><span class="lbl">字符(无空格)</span></div>
  <div class="stat"><span class="num" id="s-sent">0</span><span class="lbl">句子</span></div>
  <div class="stat"><span class="num" id="s-lines">0</span><span class="lbl">行数</span></div>
  <div class="stat"><span class="num" id="s-para">0</span><span class="lbl">段落</span></div>
</div>
<button class="btn ghost" id="clear">清空</button>
''',
        js=r'''
const ta=document.getElementById('ta');
function count(){
  const t=ta.value;
  const words=(t.trim().match(/[A-Za-z0-9_\u00C0-\uFFFF]+(?:['-][A-Za-z0-9_\u00C0-\uFFFF]+)*/g)||[]).length;
  const chars=t.length;
  const charsNo=t.replace(/\s/g,'').length;
  const sent=(t.match(/[。！？!?\.]+/g)||[]).length;
  const lines=t.split(/\r\n|\r|\n/).filter(x=>x.length||true).length;
  const para=t.split(/\n\s*\n/).filter(x=>x.trim()).length;
  document.getElementById('s-words').textContent=words;
  document.getElementById('s-chars').textContent=chars;
  document.getElementById('s-chars-nospace').textContent=charsNo;
  document.getElementById('s-sent').textContent=sent;
  document.getElementById('s-lines').textContent=lines;
  document.getElementById('s-para').textContent=para;
}
ta.addEventListener('input',count);
document.getElementById('clear').onclick=()=>{ta.value='';count();};
count();
'''),
    "case-converter": dict(
        h1="英文大小写转换工具",
        lead="一键把英文转换为大写、小写、标题大写或句首大写。本地处理，瞬时完成。",
        body=r'''
<textarea id="in" placeholder="输入英文文本…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" data-mode="upper">UPPER CASE</button>
  <button class="btn" data-mode="lower">lower case</button>
  <button class="btn" data-mode="title">Title Case</button>
  <button class="btn" data-mode="sentence">Sentence case</button>
  <button class="btn" data-mode="invert">Invert Case</button>
  <button class="btn" data-mode="alt">aLtErNaTe</button>
</div>
<textarea id="out" placeholder="转换结果…" readonly spellcheck="false"></textarea>
<button class="btn ghost" id="copy">复制结果</button>
''',
        js=r'''
const inp=document.getElementById('in'), out=document.getElementById('out');
function titleCase(s){return s.toLowerCase().replace(/(^|\s|_)([a-z])/g,(m,p,l)=>p+l.toUpperCase());}
function sentenceCase(s){return s.toLowerCase().replace(/(^\s*|[.!?]\s+)([a-z])/g,(m,p,l)=>p+l.toUpperCase());}
function invert(s){return s.replace(/[a-zA-Z]/g,c=>c===c.toUpperCase()?c.toLowerCase():c.toUpperCase());}
function alt(s){let f=true;return s.replace(/[a-zA-Z]/g,c=>{const r=f?c.toUpperCase():c.toLowerCase();f=!f;return r;});}
const fns={upper:s=>s.toUpperCase(),lower:s=>s.toLowerCase(),title:titleCase,sentence:sentenceCase,invert:invert,alt:alt};
document.querySelectorAll('.btn[data-mode]').forEach(b=>b.onclick=()=>{out.value=(fns[b.dataset.mode]||((x)=>x))(inp.value);});
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "url-codec": dict(
        h1="URL 编解码工具",
        lead="对网址或文本进行 URL 编码（百分号编码）与解码，正确处理中文与特殊字符。",
        body=r'''
<textarea id="in" placeholder="输入要编码或解码的文本…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" id="enc">URL 编码</button>
  <button class="btn" id="dec">URL 解码</button>
</div>
<textarea id="out" placeholder="结果…" readonly spellcheck="false"></textarea>
<button class="btn ghost" id="copy">复制</button>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
document.getElementById('enc').onclick=()=>{try{out.value=encodeURIComponent(inp.value);}catch(e){out.value='编码失败';}};
document.getElementById('dec').onclick=()=>{try{out.value=decodeURIComponent(inp.value);}catch(e){out.value='解码失败：格式不正确';}};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "base64-codec": dict(
        h1="Base64 编解码",
        lead="文本与 Base64 互转，支持中文 UTF-8。数据不出浏览器。",
        body=r'''
<textarea id="in" placeholder="输入文本…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" id="enc">编码 →</button>
  <button class="btn" id="dec">← 解码</button>
</div>
<textarea id="out" placeholder="结果…" readonly spellcheck="false"></textarea>
<button class="btn ghost" id="copy">复制</button>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
function utoa(s){return btoa(unescape(encodeURIComponent(s)));}
function atou(s){return decodeURIComponent(escape(atob(s)));}
document.getElementById('enc').onclick=()=>{try{out.value=utoa(inp.value);}catch(e){out.value='编码失败';}};
document.getElementById('dec').onclick=()=>{try{out.value=atou(inp.value);}catch(e){out.value='解码失败：不是合法 Base64';}};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "timestamp": dict(
        h1="时间戳转换工具",
        lead="Unix 时间戳与日期时间互转，支持本地时间与 UTC，一键获取当前时间戳。",
        body=r'''
<div class="row">
  <input type="number" id="ts" placeholder="Unix 时间戳(秒)">
  <button class="btn" id="ts2dt">→ 日期</button>
</div>
<div class="row">
  <input type="datetime-local" id="dt">
  <button class="btn" id="dt2ts">→ 时间戳</button>
</div>
<div class="row">
  <button class="btn ghost" id="now">当前时间</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const ts=document.getElementById('ts'),dt=document.getElementById('dt'),res=document.getElementById('res');
function pad(n){return String(n).padStart(2,'0');}
function fmt(d){return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+' '+pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());}
document.getElementById('ts2dt').onclick=()=>{
  const v=parseInt(ts.value);if(isNaN(v)){res.textContent='请输入有效时间戳';return;}
  const d=new Date(v*1000);
  res.innerHTML='本地：'+fmt(d)+'<br>UTC：'+d.toUTCString();
};
document.getElementById('dt2ts').onclick=()=>{
  const v=dt.value;if(!v){res.textContent='请选择日期时间';return;}
  const d=new Date(v);res.textContent='时间戳(秒)：'+Math.floor(d.getTime()/1000);
};
document.getElementById('now').onclick=()=>{
  const d=new Date();ts.value=Math.floor(d.getTime()/1000);
  dt.value=d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate())+'T'+pad(d.getHours())+':'+pad(d.getMinutes());
  res.innerHTML='当前时间戳(秒)：'+Math.floor(d.getTime()/1000)+'<br>本地：'+fmt(d);
};
'''),
    "markdown": dict(
        h1="Markdown 预览器",
        lead="左侧输入 Markdown，右侧实时渲染。完全离线，内容不离开你的设备。",
        body=r'''
<div class="md-wrap">
  <textarea id="md" placeholder="# 标题&#10;输入 **Markdown** 试试…" spellcheck="false"></textarea>
  <div id="prev" class="md-preview"></div>
</div>
''',
        js=r'''
const md=document.getElementById('md'),prev=document.getElementById('prev');
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function render(src){
  let s=esc(src);
  s=s.replace(/^###### (.*)$/gm,'<h6>$1</h6>')
     .replace(/^##### (.*)$/gm,'<h5>$1</h5>')
     .replace(/^#### (.*)$/gm,'<h4>$1</h4>')
     .replace(/^### (.*)$/gm,'<h3>$1</h3>')
     .replace(/^## (.*)$/gm,'<h2>$1</h2>')
     .replace(/^# (.*)$/gm,'<h1>$1</h1>')
     .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
     .replace(/\*(.+?)\*/g,'<em>$1</em>')
     .replace(/`([^`]+?)`/g,'<code>$1</code>')
     .replace(/!\[([^\]]*)\]\(([^)]+)\)/g,'<img alt="$1" src="$2">')
     .replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  s=s.replace(/(?:\r?\n){2,}/g,'</p><p>').replace(/\r?\n/g,'<br>');
  prev.innerHTML='<p>'+s+'</p>';
}
md.addEventListener('input',()=>render(md.value));
render('# 欢迎\n输入 **Markdown** 实时预览。\n\n- 列表项一\n- 列表项二\n\n> 引用示例');
'''),
}

SHARED_CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1f2430;--muted:#6b7280;--brand:#2f6df6;--brand-d:#1f4fc4;--line:#e6e8ec;--ok:#16a34a}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}
header{background:var(--card);border-bottom:1px solid var(--line);padding:14px 20px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:5}
header .logo{font-weight:700;color:var(--brand);text-decoration:none;font-size:18px}
header nav a{color:var(--muted);text-decoration:none;font-size:14px}
header nav a:hover{color:var(--brand)}
main{max-width:880px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:26px;margin:0 0 8px}
.lead{color:var(--muted);margin:0 0 22px}
textarea,input{width:100%;border:1px solid var(--line);border-radius:10px;padding:12px;font-size:15px;font-family:inherit;background:#fff;color:var(--ink);resize:vertical}
textarea{min-height:150px}
.row{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}
.btn{border:none;background:var(--brand);color:#fff;padding:10px 16px;border-radius:10px;font-size:14px;cursor:pointer;font-weight:600}
.btn:hover{background:var(--brand-d)}
.btn.ghost{background:#eef2ff;color:var(--brand)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;text-align:center}
.stat .num{display:block;font-size:24px;font-weight:700;color:var(--brand)}
.stat .lbl{font-size:13px;color:var(--muted)}
.result{margin-top:14px;padding:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;font-size:15px}
.md-wrap{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.md-preview{border:1px solid var(--line);border-radius:10px;padding:14px;background:#fff;overflow:auto;min-height:200px}
.md-preview h1,.md-preview h2,.md-preview h3{margin:.4em 0}
.md-preview code{background:#f1f3f7;padding:2px 5px;border-radius:4px}
.support-links{margin-top:34px;padding-top:22px;border-top:1px dashed var(--line);text-align:center}
.wechat-qr-wrap{display:inline-block}
.qr-label{display:block;font-weight:600;margin-bottom:8px}
.qr-img{width:180px;height:180px;border:1px solid var(--line);border-radius:10px}
footer{text-align:center;color:var(--muted);font-size:13px;padding:24px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:10px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;text-decoration:none;color:inherit;transition:.15s}
.card:hover{border-color:var(--brand);transform:translateY(-2px)}
.card h3{margin:0 0 6px;font-size:17px}
.card p{margin:0;color:var(--muted);font-size:14px}
@media(max-width:640px){.stats{grid-template-columns:repeat(2,1fr)}.md-wrap{grid-template-columns:1fr}}
"""

def jsonld(slug, title, desc):
    url = BASE if slug == "" else BASE + slug + "/"
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "description": desc,
        "url": url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }, ensure_ascii=False)

TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESC%%">
<meta name="keywords" content="%%KEYWORDS%%">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESC%%">
<meta property="og:type" content="website">
<meta property="og:url" content="%%CANONICAL%%">
<link rel="canonical" href="%%CANONICAL%%">
<script type="application/ld+json">%%JSONLD%%</script>
<style>%%CSS%%</style>
</head>
<body>
<header>
  <a class="logo" href="../">零成本工具箱</a>
  <nav><a href="../">全部工具</a></nav>
</header>
<main>
<h1>%%H1%%</h1>
<p class="lead">%%LEAD%%</p>
%%BODY%%
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，支持作者</span>
    <img src="../wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
</div>
</main>
<footer>© 零成本工具箱 · 全部工具本地运行，免费无水印</footer>
<script>%%JS%%</script>
</body>
</html>"""

def gen_tool(slug, title, desc, keywords, h1, lead, body, js):
    canon = BASE if slug == "" else BASE + slug + "/"
    html = (TPL
            .replace("%%TITLE%%", title)
            .replace("%%DESC%%", desc)
            .replace("%%KEYWORDS%%", keywords)
            .replace("%%CANONICAL%%", canon)
            .replace("%%H1%%", h1)
            .replace("%%LEAD%%", lead)
            .replace("%%BODY%%", body)
            .replace("%%JS%%", js)
            .replace("%%JSONLD%%", jsonld(slug, title, desc))
            .replace("%%CSS%%", SHARED_CSS))
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("generated", slug)

# 生成新工具页
for slug, t in NEW_TOOLS.items():
    meta = next(x for x in ALL_TOOLS if x[0] == slug)
    gen_tool(slug, meta[1], meta[2], meta[3], t["h1"], t["lead"], t["body"], t["js"])

# 生成 Hub / 根页
cards = "\n".join(
    f'  <a class="card" href="./{s}/"><h3>{t}</h3><p>{d}</p></a>' for s, t, d, k in ALL_TOOLS)
hub_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>零成本工具箱 — 免费在线工具集合</title>
<meta name="description" content="免费在线工具集合：图片压缩、JSON格式化、PDF工具、二维码、单位换算、密码生成、字数统计等，全部本地运行，保护隐私。">
<meta property="og:title" content="零成本工具箱">
<meta property="og:description" content="免费在线工具集合，本地运行保护隐私">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE}">
<script type="application/ld+json">{jsonld("", "零成本工具箱", "免费在线工具集合")}</script>
<style>{SHARED_CSS}</style>
</head>
<body>
<header><a class="logo" href="./">零成本工具箱</a><nav><a href="./">全部工具</a></nav></header>
<main>
<h1>零成本工具箱</h1>
<p class="lead">12 个免费在线工具，全部在你的浏览器本地运行，不上传数据、无水印、无广告骚扰。</p>
<div class="cards">
{cards}
</div>
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，支持作者持续做免费工具</span>
    <img src="wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
</div>
</main>
<footer>© 零成本工具箱 · 免费 · 本地运行 · 隐私优先</footer>
</body>
</html>"""
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(hub_html)
print("generated index.html (hub)")

# sitemap.xml
now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
urls = [BASE] + [BASE + s + "/" for s, *_ in ALL_TOOLS]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sitemap += f"  <url><loc>{u}</loc><lastmod>{now}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
sitemap += "</urlset>\n"
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)
print("generated sitemap.xml")

# atom.xml (供爬虫发现)
atom = f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>零成本工具箱</title>
<id>{BASE}</id>
<updated>{datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</updated>
<link rel="self" href="{BASE}atom.xml"/>
'''
for s, t, d, k in ALL_TOOLS:
    atom += f'''<entry><title>{t}</title><id>{BASE}{s}/</id><updated>{now}T00:00:00Z</updated><link href="{BASE}{s}/"/><summary>{d}</summary></entry>
'''
atom += "</feed>\n"
with open(os.path.join(ROOT, "atom.xml"), "w", encoding="utf-8") as f:
    f.write(atom)
print("generated atom.xml")

print("ALL DONE")
