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

# 原创数字产品（由 products_content.py 驱动；缺失时回退为空，保证构建不崩）
try:
    from products_content import PRODUCTS, GUIDES
except Exception:
    PRODUCTS, GUIDES = [], {}

# 四条「激进但合法」变现通道的内容与配置槽（缺失时回退为空，保证构建不崩）
try:
    from monetization_content import (
        AFFILIATE_OFFERS, AFF_LINKS, LEAD_NICHES, PRO_TIER,
        CURATION_SLUG, CURATION_TITLE, CURATION_DESC, CURATION_PRICE,
        CONTACT_EMAIL, LEAD_FORM_ENDPOINT,
        ADSENSE_CLIENT, ADSENSE_SLOT,
    )
except Exception:
    AFFILIATE_OFFERS, AFF_LINKS, LEAD_NICHES, PRO_TIER = [], {}, [], None
    CURATION_SLUG, CURATION_TITLE, CURATION_DESC, CURATION_PRICE = "", "", "", ""
    CONTACT_EMAIL, LEAD_FORM_ENDPOINT = "", ""
    ADSENSE_CLIENT, ADSENSE_SLOT = "", ""

# 全站统一导航（根相对路径，适配各深度页面）
NAV_HTML = (
    '<a href="/zero-cost-tools/">全部工具</a>'
    '<a href="/zero-cost-tools/store/">数字商店</a>'
    '<a href="/zero-cost-tools/deals/">联盟精选</a>'
    '<a href="/zero-cost-tools/leads/">线索·合作</a>'
    '<a href="/zero-cost-tools/pro/">升级Pro</a>'
)

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
    ("text-diff",     "文本对比工具",         "逐行对比两段文本差异，新增删除高亮", "文本对比,diff,代码对比"),
    ("csv-json",      "CSV JSON 互转",        "CSV 与 JSON 在线互转，首行作表头", "csv转json,json转csv,格式转换"),
    ("uuid",          "UUID 生成器",          "生成 RFC4122 v4 UUID，支持批量", "uuid生成,uuid,随机id"),
    ("color-hex",     "颜色值转换",           "HEX/RGB/HSL 互转，取色器", "颜色转换,hex转rgb,取色器"),
    ("number-base",   "进制转换器",           "二进制/八进制/十进制/十六进制在线互转", "进制转换,二进制,十六进制,十进制"),
    ("hash",          "文本哈希工具",         "生成 SHA-1/SHA-256/SHA-512 摘要，本地运算不上传", "文本哈希,sha256,sha1,哈希值"),
    ("regex",         "正则表达式测试",       "在线测试正则，高亮匹配结果，支持语法选项", "正则测试,正则表达式,regex"),
    ("dedup",         "文本去重工具",         "按行去除重复内容保留顺序，本地处理", "文本去重,去除重复行,去重工具"),
    ("slug",          "URL 别名生成",         "把标题转换为 SEO 友好的 URL slug（短链接别名）", "url别名,slug,短链接,url生成"),
    ("lorem",         "占位文本生成器",       "一键生成 Lorem Ipsum 段落，可调数量", "占位文本,lorem ipsum,假文生成"),
    ("wordfreq",      "词频统计工具",         "统计文本中词语出现频率，导出结果", "词频统计,词语频率,文本分析"),
    ("randnum",       "随机数生成器",         "生成指定范围与数量的随机整数，可去重", "随机数,随机整数,生成随机数"),
    ("roman-numeral", "罗马数字转换",         "阿拉伯数字与罗马数字互转，支持 1-3999", "罗马数字,阿拉伯数字,数字转换"),
    ("percent-calc",  "百分比计算器",         "求百分比、百分比数值、增减百分比", "百分比计算,百分比,增减百分比"),
    ("rmb-upper",     "金额大写转换",         "数字金额转中文大写，财务开票常用", "金额大写,人民币大写,数字转中文"),
    ("passphrase",    "密码短语生成器",       "用常见单词+分隔符生成好记又高强度的密码短语", "密码短语,passphrase,好记密码,助记密码,随机短语"),
    ("date-diff",     "日期差与倒计时工具",   "计算两个日期相差多少天，或实时倒计时到目标时间，纯前端本地运行", "日期差,天数计算,倒计时,日期计算,相差天数"),
    ("image-base64",  "图片转 Base64",        "选图即出 DataURL，纯前端本地把图片转为 Base64 编码，不上传图片", "图片转base64,图片base64,图片转dataurl,base64图片,图片编码"),
    ("html-entity",   "HTML 实体编解码",      "在线 HTML 实体编码与解码，处理 & < > 等特殊字符与中文转义，纯前端本地运行", "html实体,html实体编码,html实体解码,html编码解码,字符转义,实体编码"),
    ("url-params",    "URL 查询参数解析器",   "在线解析与重组 URL 查询参数(query string)，自动 URL 编码/解码，本地运行不上传", "url查询参数,query string 解析,url参数,query参数解析,查询串,url参数解析器"),
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
    "text-diff": dict(
        h1="文本对比工具",
        lead="粘贴两段文本，逐行对比差异，新增以绿、删除以红高亮。完全本地运行。",
        body=r'''
<div class="row">
  <textarea id="a" placeholder="原始文本…" spellcheck="false"></textarea>
  <textarea id="b" placeholder="修改后文本…" spellcheck="false"></textarea>
</div>
<button class="btn" id="go">对比差异</button>
<div id="res" class="result" style="white-space:pre-wrap;font-family:monospace;line-height:1.5"></div>
''',
        js=r'''
function diffLines(a,b){const A=a.split('\n'),B=b.split('\n');const n=A.length,m=B.length;
const dp=Array.from({length:n+1},()=>new Int32Array(m+1));
for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)dp[i][j]=A[i]===B[j]?dp[i+1][j+1]+1:Math.max(dp[i+1][j],dp[i][j+1]);
let i=0,j=0,out=[];while(i<n&&j<m){if(A[i]===B[j]){out.push(['=',A[i]]);i++;j++;}else if(dp[i+1][j]>=dp[i][j+1]){out.push(['-',A[i]]);i++;}else{out.push(['+',B[j]]);j++;}}
while(i<n){out.push(['-',A[i]]);i++;}while(j<m){out.push(['+',B[j]]);j++;}return out;}
document.getElementById('go').onclick=()=>{
  const R=diffLines(document.getElementById('a').value,document.getElementById('b').value);
  const res=document.getElementById('res');res.innerHTML='';
  R.forEach(([t,line])=>{const s=document.createElement('div');s.textContent=(t==='='?'  ':(t==='+'?'+ ':'- '))+line;
    s.style.background=t==='+'?'#e7f7ec':t==='-'?'#fdeaea':'transparent';res.appendChild(s);});
};
'''),
    "csv-json": dict(
        h1="CSV 与 JSON 互转",
        lead="CSV 转 JSON（首行作表头），或 JSON 数组转 CSV。数据不出浏览器。",
        body=r'''
<textarea id="in" placeholder="输入 CSV 或 JSON…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" id="c2j">CSV → JSON</button>
  <button class="btn" id="j2c">JSON → CSV</button>
</div>
<textarea id="out" placeholder="结果…" readonly spellcheck="false"></textarea>
<button class="btn ghost" id="copy">复制</button>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
document.getElementById('c2j').onclick=()=>{try{const lines=inp.value.trim().split(/\r?\n/);if(!lines.length){out.value='';return;}
  const head=lines[0].split(',').map(s=>s.trim());const arr=lines.slice(1).map(l=>{const c=l.split(',');const o={};head.forEach((h,k)=>o[h]=c[k]!==undefined?c[k].trim():'');return o;});out.value=JSON.stringify(arr,null,2);}catch(e){out.value='转换失败';}};
document.getElementById('j2c').onclick=()=>{try{const arr=JSON.parse(inp.value);if(!Array.isArray(arr)){out.value='需为 JSON 数组';return;}
  const keys=Object.keys(arr[0]||{});let csv=keys.join(',')+'\n';arr.forEach(o=>{csv+=keys.map(k=>(o[k]===undefined?'':o[k])).join(',')+'\n';});out.value=csv;}catch(e){out.value='JSON 解析失败';}};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "uuid": dict(
        h1="UUID 生成器",
        lead="生成 RFC4122 v4 UUID，支持批量，一键复制。",
        body=r'''
<div class="row"><input type="number" id="n" value="1" min="1" max="50" style="max-width:120px"><button class="btn" id="gen">生成</button></div>
<textarea id="out" placeholder="结果…" readonly spellcheck="false" style="min-height:120px"></textarea>
<button class="btn ghost" id="copy">复制全部</button>
''',
        js=r'''
function uuid(){return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{const r=Math.random()*16|0;const v=c==='x'?r:(r&0x3|0x8);return v.toString(16);});}
document.getElementById('gen').onclick=()=>{const n=Math.min(50,Math.max(1,parseInt(document.getElementById('n').value)||1));
  let s='';for(let i=0;i<n;i++)s+=uuid()+'\n';document.getElementById('out').value=s.trim();};
document.getElementById('copy').onclick=()=>{const o=document.getElementById('out');o.select();document.execCommand('copy');};
document.getElementById('gen').click();
'''),
    "color-hex": dict(
        h1="颜色值与 HEX 转换",
        lead="选择颜色，实时显示 HEX / RGB / HSL，可互相转换。",
        body=r'''
<div class="row"><input type="color" id="pick" value="#2f6df6" style="width:64px;height:44px;border:none;background:none"><input type="text" id="hex" value="#2f6df6" style="max-width:160px"></div>
<div id="res" class="result"></div>
''',
        js=r'''
const pick=document.getElementById('pick'),hex=document.getElementById('hex'),res=document.getElementById('res');
function h2r(h){h=h.replace('#','');return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];}
function r2hsl(r,g,b){r/=255;g/=255;b/=255;const mx=Math.max(r,g,b),mn=Math.min(r,g,b);let h,s,l=(mx+mn)/2;if(mx===mn){h=s=0;}else{const d=mx-mn;s=l>0.5?d/(2-mx-mn):d/(mx+mn);switch(mx){case r:h=(g-b)/d+(g<b?6:0);break;case g:h=(b-r)/d+2;break;default:h=(r-g)/d+4;}h*=60;}return [Math.round(h),Math.round(s*100),Math.round(l*100)];}
function show(h){const [r,g,b]=h2r(h);const [hh,ss,ll]=r2hsl(r,g,b);res.innerHTML='HEX: '+h.toUpperCase()+'<br>RGB: rgb('+r+', '+g+', '+b+')<br>HSL: hsl('+hh+', '+ss+'%, '+ll+'%)';}
pick.oninput=()=>{hex.value=pick.value;show(pick.value);};
hex.oninput=()=>{if(/^#[0-9a-fA-F]{6}$/.test(hex.value)){pick.value=hex.value;show(hex.value);}};
        show('#2f6df6');
'''),
    "number-base": dict(
        h1="进制转换器",
        lead="在二进制、八进制、十进制、十六进制之间在线互转，输入即时换算。",
        body=r'''
<div class="row">
  <input type="text" id="val" placeholder="输入数值，如 255">
  <select id="from">
    <option value="2">二进制</option>
    <option value="8">八进制</option>
    <option value="10" selected>十进制</option>
    <option value="16">十六进制</option>
  </select>
</div>
<div class="row">
  <button class="btn" data-to="2">→ 二进制</button>
  <button class="btn" data-to="8">→ 八进制</button>
  <button class="btn" data-to="10">→ 十进制</button>
  <button class="btn" data-to="16">→ 十六进制</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const val=document.getElementById('val'),from=document.getElementById('from'),res=document.getElementById('res');
const NAMES={2:'二进制',8:'八进制',10:'十进制',16:'十六进制'};
function conv(to){
  const n=parseInt(val.value.trim(),parseInt(from.value));
  if(isNaN(n)){res.textContent='请输入有效数值';return;}
  const out=to===2?n.toString(2):to===8?n.toString(8):to===10?String(n):n.toString(16).toUpperCase();
  res.innerHTML='结果（'+NAMES[to]+'）：<b>'+out+'</b>';
}
document.querySelectorAll('.btn[data-to]').forEach(b=>b.onclick=()=>conv(parseInt(b.dataset.to)));
'''),
    "hash": dict(
        h1="文本哈希工具",
        lead="生成 SHA-1 / SHA-256 / SHA-512 摘要，全程浏览器本地运算，文本不上传。",
        body=r'''
<textarea id="in" placeholder="输入要哈希的文本…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" data-alg="SHA-1">SHA-1</button>
  <button class="btn" data-alg="SHA-256">SHA-256</button>
  <button class="btn" data-alg="SHA-512">SHA-512</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const inp=document.getElementById('in'),res=document.getElementById('res');
async function digest(alg){
  const text=inp.value;
  if(!text){res.textContent='请输入文本';return;}
  const buf=await crypto.subtle.digest(alg,new TextEncoder().encode(text));
  const hex=[...new Uint8Array(buf)].map(b=>b.toString(16).padStart(2,'0')).join('');
  res.innerHTML=alg+'：<br><b style="word-break:break-all">'+hex+'</b>';
}
document.querySelectorAll('.btn[data-alg]').forEach(b=>b.onclick=()=>digest(b.dataset.alg));
'''),
    "regex": dict(
        h1="正则表达式测试",
        lead="在线测试正则表达式，支持全局与忽略大小写，实时显示匹配结果。",
        body=r'''
<textarea id="pat" placeholder="正则表达式，如 \d+" spellcheck="false" style="min-height:48px"></textarea>
<textarea id="in" placeholder="在此输入待测试文本…" spellcheck="false"></textarea>
<div class="row"><label><input type="checkbox" id="g" checked> 全局(g)</label><label><input type="checkbox" id="i"> 忽略大小写(i)</label></div>
<button class="btn" id="run">测试匹配</button>
<div id="res" class="result" style="white-space:pre-wrap"></div>
''',
        js=r'''
const pat=document.getElementById('pat'),inp=document.getElementById('in'),res=document.getElementById('res');
document.getElementById('run').onclick=()=>{
  let re;
  try{const f=(document.getElementById('g').checked?'g':'')+(document.getElementById('i').checked?'i':'');re=new RegExp(pat.value,f);}catch(e){res.textContent='正则语法错误：'+e.message;return;}
  const m=inp.value.match(re);
  if(!m){res.textContent='（无匹配）';return;}
  if(re.global){res.textContent='共 '+m.length+' 处匹配：\n'+m.join('\n');}
  else{res.textContent='匹配：'+m[0]+'\n位置：'+m.index;}
};
'''),
    "dedup": dict(
        h1="文本去重工具",
        lead="按行去除重复内容，保留首次出现顺序，数据不出浏览器。",
        body=r'''
<textarea id="in" placeholder="每行一项，自动去除重复行（保留首次出现顺序）…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" id="go">去除重复</button>
  <button class="btn ghost" id="copy">复制结果</button>
  <button class="btn ghost" id="dl">下载</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const inp=document.getElementById('in'),res=document.getElementById('res');
document.getElementById('go').onclick=()=>{
  const seen=new Set(),out=[];
  inp.value.split(/\r?\n/).forEach(l=>{const k=l.trim();if(k&&!seen.has(k)){seen.add(k);out.push(l);}});
  res.textContent='已去除重复，剩余 '+out.length+' 行。';
  inp.value=out.join('\n');
};
document.getElementById('copy').onclick=()=>{inp.select();document.execCommand('copy');};
document.getElementById('dl').onclick=()=>{const b=new Blob([inp.value],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='dedup.txt';a.click();};
'''),
    "slug": dict(
        h1="URL 别名(slug)生成",
        lead="把文章标题转换为 SEO 友好的 URL slug（短链接别名），一键复制。",
        body=r'''
<input type="text" id="in" placeholder="输入标题，如 How To Build A Site">
<textarea id="out" placeholder="生成的 slug…" readonly spellcheck="false" style="min-height:80px"></textarea>
<div class="row"><button class="btn" id="go">生成</button><button class="btn ghost" id="copy">复制</button></div>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
document.getElementById('go').onclick=()=>{
  const s=inp.value.trim().toLowerCase().replace(/[^a-z0-9\s-]/g,'').replace(/\s+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
  out.value=s;
};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "lorem": dict(
        h1="占位文本生成器",
        lead="一键生成 Lorem Ipsum 假文段落，可指定段落数量，用于排版与设计稿。",
        body=r'''
<div class="row">
  <input type="number" id="n" value="3" min="1" max="20" style="max-width:120px">
  <span>段</span>
  <button class="btn" id="go">生成</button>
</div>
<textarea id="out" readonly spellcheck="false" style="min-height:200px"></textarea>
<button class="btn ghost" id="copy">复制</button>
''',
        js=r'''
const words=('lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat').split(' ');
function sentence(){const len=8+Math.floor(Math.random()*7);let s='';for(let i=0;i<len;i++){let w=words[Math.floor(Math.random()*words.length)];if(i===0)w=w.charAt(0).toUpperCase()+w.slice(1);s+=w+' ';}return s.trim()+'.';}
document.getElementById('go').onclick=()=>{const n=Math.min(20,Math.max(1,parseInt(document.getElementById('n').value)||1));let t='';for(let p=0;p<n;p++){let para='';for(let i=0;i<5;i++)para+=sentence()+' ';t+=para.trim()+'\n\n';}document.getElementById('out').value=t.trim();};
document.getElementById('copy').onclick=()=>{const o=document.getElementById('out');o.select();document.execCommand('copy');};
'''),
    "wordfreq": dict(
        h1="词频统计工具",
        lead="统计文本中词语出现频率，按频次排序，帮助快速分析文本热点。",
        body=r'''
<textarea id="in" placeholder="粘贴文本，统计词频…" spellcheck="false"></textarea>
<div class="row"><button class="btn" id="go">统计</button><input type="number" id="top" value="20" min="1" max="100" style="max-width:90px" title="显示前 N"></div>
<div id="res" class="result"></div>
''',
        js=r'''
const inp=document.getElementById('in'),res=document.getElementById('res');
document.getElementById('go').onclick=()=>{
  const txt=inp.value.toLowerCase().replace(/[^\w\u4e00-\u9fa5\s]/g,' ');
  const m={};txt.split(/\s+/).filter(Boolean).forEach(w=>{m[w]=(m[w]||0)+1;});
  const arr=Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,Math.max(1,Math.min(100,parseInt(document.getElementById('top').value)||20)));
  res.innerHTML='共 '+Object.keys(m).length+' 个不同词。<br>'+arr.map(([w,c])=>'<div>'+w+'：'+c+'</div>').join('');
};
'''),
    "randnum": dict(
        h1="随机数生成器",
        lead="生成指定范围与数量的随机整数，支持不重复模式，本地生成。",
        body=r'''
<div class="row">
  <input type="number" id="min" value="1" style="max-width:100px" placeholder="最小">
  <input type="number" id="max" value="100" style="max-width:100px" placeholder="最大">
  <input type="number" id="cnt" value="5" min="1" max="200" style="max-width:100px" placeholder="数量">
</div>
<div class="row"><label><input type="checkbox" id="uniq"> 不重复</label></div>
<textarea id="out" readonly spellcheck="false" style="min-height:120px"></textarea>
<div class="row"><button class="btn" id="go">生成</button><button class="btn ghost" id="copy">复制</button></div>
''',
        js=r'''
const min=document.getElementById('min'),max=document.getElementById('max'),cnt=document.getElementById('cnt'),out=document.getElementById('out');
document.getElementById('go').onclick=()=>{
  const lo=parseInt(min.value),hi=parseInt(max.value),n=Math.min(200,Math.max(1,parseInt(cnt.value)||1));
  if(lo>hi){out.value='最小值不能大于最大值';return;}
  let res=[];
  if(document.getElementById('uniq').checked){const pool=[];for(let i=lo;i<=hi;i++)pool.push(i);for(let i=0;i<n&&pool.length;i++){res.push(pool.splice(Math.floor(Math.random()*pool.length),1)[0]);}}
  else{for(let i=0;i<n;i++)res.push(Math.floor(Math.random()*(hi-lo+1))+lo);}
  out.value=res.join('\n');
};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "roman-numeral": dict(
        h1="罗马数字与阿拉伯数字互转",
        lead="在阿拉伯数字（1-3999）与罗马数字之间互转，学习历史纪年或阅读旧文献时很有用。",
        body=r'''
<div class="row">
  <input id="ara" type="number" placeholder="阿拉伯数字，如 2024" style="max-width:200px">
  <button class="btn" id="atoR">→ 罗马数字</button>
</div>
<div class="row">
  <input id="rom" placeholder="罗马数字，如 MMXXIV" style="max-width:200px">
  <button class="btn" id="Rtoa">→ 阿拉伯数字</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const ara=document.getElementById('ara'),rom=document.getElementById('rom'),res=document.getElementById('res');
const MAP=[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
function toRom(n){if(!n||n<1||n>3999)return '仅支持 1-3999';let s='';for(const[v,sym]of MAP){while(n>=v){s+=sym;n-=v;}}return s;}
function toAra(s){s=(s||'').trim().toUpperCase();if(!/^[IVXLCDM]+$/.test(s))return '请输入合法罗马数字';let total=0,prev=0;const V={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};for(let i=s.length-1;i>=0;i--){const cur=V[s[i]];total+=cur<prev?-cur:cur;prev=cur;}return total;}
document.getElementById('atoR').onclick=()=>{res.innerHTML='罗马数字：<b>'+toRom(parseInt(ara.value))+'</b>';};
document.getElementById('Rtoa').onclick=()=>{res.innerHTML='阿拉伯数字：<b>'+toAra(rom.value)+'</b>';};
'''),
    "percent-calc": dict(
        h1="百分比计算器",
        lead="在线计算百分比、已知基数求百分比数值、以及增减百分比，财务与日常都常用。",
        body=r'''
<div class="row">
  <input id="part" type="number" placeholder="部分值" style="max-width:160px">
  <input id="whole" type="number" placeholder="整体值" style="max-width:160px">
  <button class="btn" id="calc">求百分比</button>
</div>
<div class="row">
  <input id="base" type="number" placeholder="基数" style="max-width:160px">
  <input id="pct" type="number" placeholder="百分比 %" style="max-width:120px">
  <button class="btn" id="of">求数值</button>
</div>
<div class="row">
  <input id="old" type="number" placeholder="原值" style="max-width:160px">
  <input id="new" type="number" placeholder="新值" style="max-width:160px">
  <button class="btn" id="chg">增减百分比</button>
</div>
<div id="res" class="result"></div>
''',
        js=r'''
const g=id=>document.getElementById(id),res=g('res');
g('calc').onclick=()=>{const p=+g('part').value,w=+g('whole').value;if(!w){res.textContent='整体值不能为0';return;}res.innerHTML='结果：<b>'+((p/w)*100).toFixed(2)+'%</b>';};
g('of').onclick=()=>{const b=+g('base').value,p=+g('pct').value;res.innerHTML='结果：<b>'+(b*p/100)+'</b>';};
g('chg').onclick=()=>{const o=+g('old').value,n=+g('new').value;if(!o){res.textContent='原值不能为0';return;}res.innerHTML='变化：<b>'+(((n-o)/o)*100).toFixed(2)+'%</b>';};
'''),
    "rmb-upper": dict(
        h1="金额大写转换",
        lead="把数字金额转换为中文大写（壹贰叁…），开票、填支票、写合同常用，自动处理角分。",
        body=r'''
<input id="amt" type="number" placeholder="输入金额，如 1234.56" style="max-width:240px">
<button class="btn" id="go">转中文大写</button>
<div id="res" class="result"></div>
''',
        js=r'''
const g=id=>document.getElementById(id),res=g('res');
function rmbUpper(num){
  if(isNaN(num))return '请输入有效数字';
  if(num===0)return '零元整';
  const neg=num<0;num=Math.abs(num);
  const d=['零','壹','贰','叁','肆','伍','陆','柒','捌','玖'];
  const ints=['','拾','佰','仟'];const units=['','万','亿'];
  let str=Math.floor(num).toString();const groups=[];
  while(str.length>0){groups.unshift(str.slice(-4));str=str.slice(0,-4);}
  let s='';
  groups.forEach((grp,gi)=>{let part='';let zero=false;const len=grp.length;
    for(let i=0;i<len;i++){const v=+grp[i];const pos=len-1-i;
      if(v===0){zero=true;}else{part+=(zero&&part?'零':'')+d[v]+ints[pos];zero=false;}}
    if(part)s+=part+units[groups.length-1-gi];});
  let dec=Math.round((num-Math.floor(num))*100);const jiao=Math.floor(dec/10),fen=dec%10;
  let decStr='';if(jiao>0)decStr+=d[jiao]+'角';if(fen>0)decStr+=d[fen]+'分';if(!decStr)decStr='整';
  return (neg?'负':'')+s+'元'+decStr;
}
    g('go').onclick=()=>{res.innerHTML='中文大写：<b>'+rmbUpper(parseFloat(g('amt').value))+'</b>';};
'''),
    "passphrase": dict(
        h1="密码短语生成器",
        lead="用语词典中的常见单词拼接成好记又高强度的密码短语（如 correct-horse-battery-staple），比随机字符更易记忆。本地生成，不上传任何数据。",
        body=r'''
<div class="row">
  <input type="number" id="nwords" value="4" min="2" max="12" style="max-width:110px" title="单词数量">
  <select id="sep"><option value="-">分隔符: -</option><option value=" ">空格</option><option value=".">.</option><option value="_">_</option><option value="/">/</option></select>
  <label><input type="checkbox" id="cap"> 首字母大写</label>
  <label><input type="checkbox" id="digit"> 末尾加数字</label>
  <button class="btn" id="go">生成</button>
</div>
<textarea id="out" readonly spellcheck="false" style="min-height:100px"></textarea>
<div class="row"><button class="btn ghost" id="copy">复制</button></div>
''',
        js=r'''
const WORDS=("apple amber anchor angel autumn baby balance ball band bank barn bear beam bean beach bell bird blue boat book boot boss bowl brick bridge brown brush cabin cake calm camel candy candle canoe canvas carpet cat cave cedar cherry chest chief circle clay cliff cloud clover coal coast cobra comet coral crane creek crowd crown crystal cup curve daisy dawn deer diamond dock dollar dolphin dome door dove dragon dream drum duck eagle earth ember echo edge engine fairy feather field fire fish flame flood flower forest fox frost fruit galaxy garden gate ghost glass globe gold grass gravity green hammer harbor hawk heart hill honey horse island ivory jet jewel jungle kernel key kite knight lake lamp leaf lemon light lion lock lotus luck magnet maple marble meadow metal mill moon mountain mouse music nail needle nest nickel noble north ocean olive onion orange owl ox panda paper pearl pencil piano pilot pine planet plaza plume polar pond portal potato prince pumpkin quarter queen rabbit radar rainbow raven river road robot rocket rose ruby sail salt sand scale scorpion shadow shark shell silver sky slate smoke snow soap solar soldier song spark sphere spider spirit spring star statue steel stone storm stream sugar sun sword table tiger token tower town tree triangle tunnel turtle valley violet volcano wagon water wave web whale wheel willow wind window witch wolf wood worm zebra zone").split(' ');
function gen(){
  const n=Math.min(12,Math.max(2,parseInt(document.getElementById('nwords').value)||4));
  let words=[];for(let i=0;i<n;i++){words.push(WORDS[Math.floor(Math.random()*WORDS.length)]);}
  if(document.getElementById('cap').checked){words=words.map(w=>w.charAt(0).toUpperCase()+w.slice(1));}
  let s=words.join(document.getElementById('sep').value);
  if(document.getElementById('digit').checked){s+=Math.floor(Math.random()*100);}
  document.getElementById('out').value=s;
}
document.getElementById('go').onclick=gen;
document.getElementById('copy').onclick=()=>{const o=document.getElementById('out');o.select();document.execCommand('copy');};
gen();
'''),
    "date-diff": dict(
        h1="日期差与倒计时工具",
        lead="计算任意两个日期相差多少天，或实时倒计时到某个目标日期时间。全部在浏览器本地运行，不上传数据。",
        body=r'''
<div class="row">
  <div style="flex:1;min-width:200px">
    <label style="display:block;font-size:14px;color:var(--muted);margin-bottom:6px">开始日期</label>
    <input type="date" id="d1">
  </div>
  <div style="flex:1;min-width:200px">
    <label style="display:block;font-size:14px;color:var(--muted);margin-bottom:6px">结束日期</label>
    <input type="date" id="d2">
  </div>
  <div style="display:flex;align-items:flex-end">
    <button class="btn" id="calc">计算相差天数</button>
  </div>
</div>
<div id="res" class="result"></div>
<hr style="margin:26px 0;border:none;border-top:1px dashed var(--line)">
<h2 style="font-size:18px;margin:0 0 12px">⏳ 实时倒计时到目标时间</h2>
<div class="row">
  <div style="flex:1;min-width:220px">
    <label style="display:block;font-size:14px;color:var(--muted);margin-bottom:6px">目标日期时间</label>
    <input type="datetime-local" id="target">
  </div>
  <div style="display:flex;gap:10px;align-items:flex-end">
    <button class="btn" id="startcd">开始倒计时</button>
    <button class="btn ghost" id="stopcd">停止</button>
  </div>
</div>
<div id="cd" class="result"></div>
''',
        js=r'''
const d1=document.getElementById('d1'),d2=document.getElementById('d2'),res=document.getElementById('res');
const g=id=>document.getElementById(id);
function parseDay(v){return new Date(v+'T00:00:00');}
g('calc').onclick=()=>{
  if(!d1.value||!d2.value){res.textContent='请选择两个日期';return;}
  const days=Math.round((parseDay(d2.value)-parseDay(d1.value))/86400000);
  const abs=Math.abs(days);
  let note = days===0?'两个日期相同。'
    : (days>0?('「结束」比「开始」晚 '+days+' 天。')
             :('「结束」比「开始」早 '+abs+' 天。'));
  res.innerHTML='相差 <b>'+abs+'</b> 天<br><span style="color:var(--muted);font-size:13px">'+note+'</span>';
};
let timer=null;
const target=g('target'),cd=g('cd');
function pad(n){return String(n).padStart(2,'0');}
function tick(){
  if(!target.value){cd.textContent='请选择目标日期时间';return;}
  const ms=new Date(target.value).getTime()-Date.now();
  if(ms<=0){cd.innerHTML='<b style="color:var(--ok)">时间到！🎉</b>';stop();return;}
  const s=Math.floor(ms/1000);
  const D=Math.floor(s/86400),H=Math.floor(s%86400/3600),M=Math.floor(s%3600/60),S=s%60;
  cd.innerHTML='剩余 <b>'+D+'</b> 天 <b>'+pad(H)+'</b> 时 <b>'+pad(M)+'</b> 分 <b>'+pad(S)+'</b> 秒';
}
function stop(){if(timer){clearInterval(timer);timer=null;}}
g('startcd').onclick=()=>{stop();tick();timer=setInterval(tick,1000);};
g('stopcd').onclick=stop;
'''),
    "image-base64": dict(
        h1="图片转 Base64 工具",
        lead="选择本地图片，立刻得到它的 Base64 DataURL（data:image/...;base64,...）。全程在浏览器本地完成，图片不会上传到任何服务器，可复制或下载。",
        body=r'''
<label class="upbtn" for="file">📂 选择图片</label>
<input type="file" id="file" accept="image/*" hidden>
<div class="row" style="align-items:center">
  <span id="meta" class="lbl" style="color:var(--muted);font-size:13px">未选择文件</span>
  <button class="btn" id="copy">复制 DataURL</button>
  <button class="btn ghost" id="dl">下载文本</button>
  <button class="btn ghost" id="clear">清空</button>
</div>
<img id="preview" alt="预览" style="display:none;max-width:100%;border:1px solid var(--line);border-radius:10px;margin:10px 0">
<textarea id="out" readonly spellcheck="false" style="min-height:160px" placeholder="选择图片后，这里会显示其 Base64 DataURL…"></textarea>
''',
        js=r'''
const fileInput=document.getElementById('file');
const out=document.getElementById('out');
const meta=document.getElementById('meta');
const preview=document.getElementById('preview');
let lastUrl='';
fileInput.onchange=()=>{
  const f=fileInput.files[0];
  if(!f){return;}
  if(!f.type.startsWith('image/')){meta.textContent='请选择图片文件';return;}
  const reader=new FileReader();
  reader.onload=e=>{
    lastUrl=e.target.result;
    out.value=lastUrl;
    meta.textContent=f.name+' · '+f.size+' 字节 · '+f.type;
    preview.src=lastUrl;
    preview.style.display='block';
  };
  reader.onerror=()=>{meta.textContent='读取失败，请重试';};
  reader.readAsDataURL(f);
};
document.getElementById('copy').onclick=()=>{if(!out.value){meta.textContent='请先选择图片';return;}out.focus();out.select();document.execCommand('copy');meta.textContent='已复制 DataURL';};
document.getElementById('dl').onclick=()=>{if(!out.value){meta.textContent='请先选择图片';return;}const b=new Blob([out.value],{type:'text/plain'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='image-base64.txt';a.click();};
document.getElementById('clear').onclick=()=>{fileInput.value='';out.value='';lastUrl='';meta.textContent='未选择文件';preview.src='';preview.style.display='none';};
'''),
    "html-entity": dict(
        h1="HTML 实体编解码",
        lead="对文本进行 HTML 实体编码（把 & < > 等特殊字符与中文转为 &#数字; 或 &amp; 等）或反向解码。完全在浏览器本地运行，不上传数据。",
        body=r'''
<textarea id="in" placeholder="输入要编码或解码的文本…" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" data-mode="min">编码（特殊字符）</button>
  <button class="btn" data-mode="all">编码（非 ASCII）</button>
  <button class="btn" id="dec">解码</button>
  <button class="btn ghost" id="swap">↑ 结果填入输入框</button>
</div>
<textarea id="out" placeholder="结果…" readonly spellcheck="false"></textarea>
<button class="btn ghost" id="copy">复制结果</button>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
const MAP={'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'};
function enc(str,mode){
  if(mode==='all'){return str.replace(/[^\x00-\x7F]/g,c=>'&#'+c.codePointAt(0)+';');}
  return str.replace(/[&<>"']/g,c=>MAP[c]||c);
}
document.querySelectorAll('.btn[data-mode]').forEach(b=>b.onclick=()=>{try{out.value=enc(inp.value,b.dataset.mode);}catch(e){out.value='编码失败';}});
document.getElementById('dec').onclick=()=>{try{const t=document.createElement('textarea');t.innerHTML=inp.value;out.value=t.value;}catch(e){out.value='解码失败';}};
document.getElementById('swap').onclick=()=>{inp.value=out.value;};
document.getElementById('copy').onclick=()=>{out.select();document.execCommand('copy');};
'''),
    "url-params": dict(
        h1="URL 查询参数解析器",
        lead="粘贴完整网址或原始 query string，一键解析成可读的参数名/值列表；编辑后可重新拼回 URL 编码后的查询串。全程浏览器本地运行，不上传任何数据。",
        body=r'''
<textarea id="in" placeholder="粘贴完整 URL（含 ?）或原始查询串，如 a=1&amp;b=hello%20world&amp;c" spellcheck="false"></textarea>
<div class="row">
  <button class="btn" id="parse">解析</button>
  <button class="btn ghost" id="clear">清空</button>
</div>
<div id="editor"></div>
<div class="row" id="editorBtns" style="display:none">
  <button class="btn" id="add">+ 添加参数</button>
  <button class="btn" id="build">重组查询串</button>
  <button class="btn ghost" id="copy">复制结果</button>
</div>
<textarea id="out" placeholder="重组后的查询串（自动 URL 编码）…" readonly spellcheck="false"></textarea>
''',
        js=r'''
const inp=document.getElementById('in'),out=document.getElementById('out');
const editor=document.getElementById('editor'),eb=document.getElementById('editorBtns');
let cur=[],base='';
function escAttr(s){return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
document.getElementById('parse').onclick=()=>{
  let s=inp.value.trim();
  base='';
  if(!s){editor.innerHTML='';eb.style.display='none';out.value='';return;}
  const h=s.indexOf('#');if(h>=0)s=s.slice(0,h);
  const q=s.indexOf('?');if(q>=0){base=s.slice(0,q);s=s.slice(q+1);}
  cur=[];
  s.split('&').forEach(pair=>{
    if(pair==='')return;
    const eq=pair.indexOf('=');let k,v;
    if(eq<0){k=pair;v='';}else{k=pair.slice(0,eq);v=pair.slice(eq+1);}
    try{k=decodeURIComponent(k.replace(/\+/g,' '));}catch(e){}
    try{v=decodeURIComponent(v.replace(/\+/g,' '));}catch(e){}
    cur.push([k,v]);
  });
  render();
};
function render(){
  if(!cur.length){editor.innerHTML='<p style="color:var(--muted)">未解析到参数。</p>';eb.style.display='none';return;}
  eb.style.display='flex';
  editor.innerHTML=cur.map((r,i)=>
    '<div class="row" style="align-items:center">'
    +'<input data-k="'+i+'" value="'+escAttr(r[0])+'" placeholder="参数名" style="flex:1">'
    +'<input data-v="'+i+'" value="'+escAttr(r[1])+'" placeholder="参数值" style="flex:1">'
    +'<button class="btn ghost" data-del="'+i+'">删除</button></div>'
  ).join('');
  editor.querySelectorAll('input[data-k]').forEach(el=>el.oninput=()=>{cur[+el.dataset.k][0]=el.value;});
  editor.querySelectorAll('input[data-v]').forEach(el=>el.oninput=()=>{cur[+el.dataset.v][1]=el.value;});
  editor.querySelectorAll('button[data-del]').forEach(b=>b.onclick=()=>{cur.splice(+b.dataset.del,1);render();});
}
document.getElementById('add').onclick=()=>{cur.push(['','']);render();};
document.getElementById('build').onclick=()=>{
  const parts=cur.filter(r=>r[0].trim()!=='').map(r=>encodeURIComponent(r[0])+'='+encodeURIComponent(r[1]));
  out.value=(base?base+'?':'')+parts.join('&');
};
document.getElementById('copy').onclick=()=>{if(!out.value){out.value='';return;}out.select();document.execCommand('copy');};
document.getElementById('clear').onclick=()=>{inp.value='';out.value='';editor.innerHTML='';eb.style.display='none';cur=[];};
'''),
}

# 数字产品由 products_content.py 驱动（原创内容，零成本、可合规销售）。
# 每个产品有可读详情页 store/<slug>/index.html（同时作 SEO 长尾页），
# 结账统一走 store/order.html（微信扫码下单/支持）。

BLOG_TITLES = {
    "compress-guide.html": "图片压缩工具使用指南",
    "jsonfmt-guide.html": "JSON 格式化工具使用指南",
    "pdf-guide.html": "PDF 工具箱使用指南",
    "qrcode-guide.html": "二维码生成器使用指南",
    "convert-guide.html": "单位换算器使用指南",
    "password-guide.html": "密码生成器使用指南",
    "word-counter-guide.html": "字数统计工具使用指南",
    "case-converter-guide.html": "大小写转换工具使用指南",
    "url-codec-guide.html": "URL 编解码工具使用指南",
    "base64-codec-guide.html": "Base64 编解码使用指南",
    "timestamp-guide.html": "时间戳转换工具使用指南",
    "markdown-guide.html": "Markdown 预览器使用指南",
    "text-diff-guide.html": "文本对比工具使用指南",
    "csv-json-guide.html": "CSV JSON 互转使用指南",
    "uuid-guide.html": "UUID 生成器使用指南",
    "color-hex-guide.html": "颜色值转换使用指南",
    "number-base-guide.html": "进制转换器使用指南",
    "hash-guide.html": "文本哈希工具使用指南",
    "regex-guide.html": "正则表达式测试使用指南",
    "dedup-guide.html": "文本去重工具使用指南",
    "slug-guide.html": "URL 别名生成使用指南",
    "lorem-guide.html": "占位文本生成器使用指南",
    "wordfreq-guide.html": "词频统计工具使用指南",
    "randnum-guide.html": "随机数生成器使用指南",
    "passphrase-guide.html": "密码短语生成器使用指南",
    "date-diff-guide.html": "日期差与倒计时使用指南",
    "image-base64-guide.html": "图片转 Base64使用指南",
    "html-entity-guide.html": "HTML 实体编解码使用指南",
    "url-params-guide.html": "URL 查询参数解析器使用指南",
    "free-tools-guide.html": "免费在线工具推荐合集",
    "privacy-guide.html": "如何安全使用在线工具保护隐私",
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
.upbtn{display:inline-block;background:var(--brand);color:#fff;padding:10px 16px;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer}
.upbtn:hover{background:var(--brand-d)}
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
.related{margin-top:34px;padding-top:22px;border-top:1px solid var(--line)}
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

def jsonld_crumb(slug, title):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "零成本工具箱", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + slug + "/"}
        ]
    }, ensure_ascii=False)

def jsonld_website():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "零成本工具箱",
        "url": BASE,
        "description": "免费在线工具集合，全部本地运行保护隐私"
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
<meta property="og:image" content="%%OGIMG%%">
<link rel="canonical" href="%%CANONICAL%%">
<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="%%ATOM%%">
<script type="application/ld+json">%%JSONLD%%</script>
<script type="application/ld+json">%%CRUMB%%</script>
<style>%%CSS%%</style>
</head>
<body>
<header>
  <a class="logo" href="/zero-cost-tools/">零成本工具箱</a>
  <nav>%%NAV%%</nav>
</header>
<main>
<h1>%%H1%%</h1>
<p class="lead">%%LEAD%%</p>
%%BODY%%
%%RELATED%%
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，支持作者</span>
    <img src="../wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
</div>
%%ADSENSE%%
</main>
<footer>© 零成本工具箱 · 全部工具本地运行，免费无水印</footer>
<script>%%JS%%</script>
</body>
</html>"""

def gen_tool(slug, title, desc, keywords, h1, lead, body, js):
    canon = BASE if slug == "" else BASE + slug + "/"
    # 相关工具内链：按当前工具位置错位取 4 个，使内链权重均匀分布
    slugs = [s for s, *_ in ALL_TOOLS]
    idx = slugs.index(slug)
    n = len(slugs)
    picks = [(idx + 1 + i) % n for i in range(4)]
    rel = "".join(
        f'  <a class="card" href="../{ALL_TOOLS[p][0]}/"><h3>{ALL_TOOLS[p][1]}</h3><p>{ALL_TOOLS[p][2]}</p></a>'
        for p in picks)
    related = f'<div class="related"><h2>相关工具</h2><div class="cards">\n{rel}\n</div></div>'
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
            .replace("%%CRUMB%%", jsonld_crumb(slug, title))
            .replace("%%RELATED%%", related)
            .replace("%%OGIMG%%", "../og.png")
            .replace("%%ATOM%%", "../atom.xml")
            .replace("%%NAV%%", NAV_HTML)
            .replace("%%ADSENSE%%", adsense_code())
            .replace("%%CSS%%", SHARED_CSS))
    d = os.path.join(ROOT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("generated %s/index.html" % slug)


def adsense_code():
    """AdSense 广告位代码。未配置 ADSENSE_CLIENT 时返回空字符串（不显示广告）。"""
    if not ADSENSE_CLIENT:
        return ""
    slot = f' data-ad-slot="{ADSENSE_SLOT}"' if ADSENSE_SLOT else ""
    return (
        '<div class="adslot" aria-label="广告">'
        f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>'
        f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE_CLIENT}"{slot} data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
        '</div>')

# 数字商店（数据驱动，从 PRODUCTS 生成）
STORE_CSS = """
.lic{display:inline-block;font-size:12px;background:#eef2ff;color:var(--brand);padding:2px 8px;border-radius:8px;margin:0 0 10px}
.card{display:flex;flex-direction:column}
.card .price{color:var(--ok);font-weight:700;font-size:17px;margin:auto 0 12px}
.note{margin-top:30px;padding:16px;background:#fff;border:1px dashed var(--line);border-radius:12px;font-size:13px;color:var(--muted)}
code{background:#f1f3f7;padding:2px 5px;border-radius:4px}
.article{max-width:760px}
.article h2{margin-top:26px;font-size:20px}
.article ul,.article ol{margin:8px 0 8px 22px}
.article li{margin:4px 0}
"""

def gen_store():
    cards = "\n".join(
        f'''  <div class="card">
    <h3><a href="./{p["slug"]}/" style="color:inherit;text-decoration:none">{p["title"]}</a></h3>
    <p>{p["desc"]}</p>
    <span class="lic">授权：{p["license"]}</span>
    <div class="price">¥{p["price"]}</div>
    <a class="btn" href="./{p["slug"]}/" rel="noopener">查看详情 / 获取</a>
  </div>''' for p in PRODUCTS)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数字产品商店 — 零成本工具箱</title>
<meta name="description" content="原创数字产品：零成本变现实操手册、免费可商用资源清单、工具站 SEO 打法、二手平台合规避坑。每一件都由本项目原创撰写，可合规付费支持。">
<meta property="og:title" content="数字产品商店">
<meta property="og:description" content="原创可售数字产品，零成本、合规">
<meta property="og:type" content="website">
<meta property="og:image" content="../og.png">
<link rel="canonical" href="https://ckstc.github.io/zero-cost-tools/store/">
<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="../atom.xml">
<style>
{SHARED_CSS}
{STORE_CSS}
</style>
</head>
<body>
<header>
  <a class="logo" href="/zero-cost-tools/">零成本工具箱</a>
  <nav>{NAV_HTML}</nav>
</header>
<main>
<h1>数字产品商店</h1>
<p class="lead">全部为<strong>本项目原创撰写</strong>的数字产品（指南 / 清单 / 实操手册）。内容零成本生成、版权清晰，可合规付费支持，也可免费阅读后自愿打赏。</p>

<div class="cards">
{cards}
</div>

<div class="note">
  📌 本商店为零成本静态页面。结账走微信扫码（见每个商品详情页的「下单 / 支持」）。
  所有商品均为原创内容，授权清晰；我们<strong>不售卖任何无授权搬运或盗版资源</strong>。
  想自建类似商店，资源筛选请用项目内的 <code>scripts/collect_resources.py</code>（许可感知，只收明确可转售来源）。
</div>
</main>
<footer>© 零成本工具箱 · 数字产品均为原创内容</footer>
</body>
</html>'''
    d = os.path.join(ROOT, "store")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("generated store/index.html")


# 单个产品详情页（同时作为 SEO 长尾可读页）
def gen_store_details():
    for p in PRODUCTS:
        slug = p["slug"]
        body = GUIDES.get(slug, "<p>（内容整理中）</p>")
        art_jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": p["title"],
            "description": p["desc"],
            "author": {"@type": "Organization", "name": "零成本工具箱"},
            "publisher": {"@type": "Organization", "name": "零成本工具箱"},
        }, ensure_ascii=False)
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]} — 数字产品商店</title>
<meta name="description" content="{p["desc"]}">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:type" content="article">
<meta property="og:image" content="../../og.png">
<link rel="canonical" href="https://ckstc.github.io/zero-cost-tools/store/{slug}/">
<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="../../atom.xml">
<script type="application/ld+json">{art_jsonld}</script>
<style>
{SHARED_CSS}
{STORE_CSS}
.article img.qr{{width:200px;height:200px;border:1px solid var(--line);border-radius:10px}}
.support-links{{margin-top:30px;padding-top:20px;border-top:1px dashed var(--line);text-align:center}}
</style>
</head>
<body>
<header>
  <a class="logo" href="../../">零成本工具箱</a>
  <nav><a href="../../">全部工具</a><a href="../">数字商店</a></nav>
</header>
<main class="article">
<h1>{p["title"]}</h1>
<p class="lead">{p["desc"]}</p>
<div style="margin:14px 0">
  <span class="lic">授权：{p["license"]}</span>
  <span class="lic">价格：¥{p["price"]}</span>
</div>
{body}
<div class="support-links">
  <div class="wechat-qr-wrap">
    <span class="qr-label">💚 微信扫一扫，付费支持 / 获取资料</span>
    <img src="../../wechat-qr.png" alt="微信收款码" class="qr-img">
  </div>
  <p style="color:var(--muted);font-size:13px;margin-top:10px">
    扫码付款时备注「{slug}」，付款后加微信即发你对应资料（内容也已在本页免费公开，付费是对作者的支持）。
  </p>
  <p><a class="btn" href="../order.html">📦 去下单 / 支持页</a></p>
</div>
<p style="margin-top:24px"><a href="../">← 返回数字商店</a> · <a href="../../">返回全部工具</a></p>
</main>
<footer>© 零成本工具箱 · 本文为原创内容</footer>
</body>
</html>'''
        d = os.path.join(ROOT, "store", slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("generated store/%s/index.html" % slug)


# 统一的微信下单 / 支持页
def gen_order():
    items = "\n".join(
        f'  <li><b>{p["title"]}</b> — ¥{p["price"]}（备注「{p["slug"]}」）</li>' for p in PRODUCTS)
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>下单 / 支持 — 零成本工具箱</title>
<meta name="description" content="微信扫码付费支持零成本工具箱的数字产品与原作者。">
<meta property="og:type" content="website">
<meta property="og:image" content="../og.png">
<link rel="canonical" href="https://ckstc.github.io/zero-cost-tools/store/order.html">
<style>
{SHARED_CSS}
{STORE_CSS}
</style>
</head>
<body>
<header>
  <a class="logo" href="/zero-cost-tools/">零成本工具箱</a>
  <nav>{NAV_HTML}</nav>
</header>
<main style="max-width:680px">
<h1>下单 / 支持</h1>
<p class="lead">微信扫码付款，备注你想购买的产品编号，付款后加微信即可获取对应资料。所有产品均为原创内容，也可在对应详情页免费阅读后自愿打赏。</p>
<div class="support-links" style="border:1px solid var(--line);border-radius:12px;padding:20px">
  <span class="qr-label">💚 微信收款码</span>
  <img src="../wechat-qr.png" alt="微信收款码" class="qr-img">
</div>
<h2 style="margin-top:26px">可选项目</h2>
<ul>{items}
</ul>
<p style="color:var(--muted);font-size:13px">说明：本商店为零成本静态页面，无后台自动发货。采用「扫码付款 + 备注编号 + 加微信发资料」的人肉交接，确保合规且零平台抽成。内容已尽量在详情页免费公开，付费是对持续创作的实质支持。</p>
<p style="margin-top:20px"><a href="./">← 返回数字商店</a></p>
</main>
<footer>© 零成本工具箱</footer>
</body>
</html>'''
    d = os.path.join(ROOT, "store")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "order.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("generated store/order.html")

# ===================== 四条「激进但合法」变现通道 =====================
PAGE_CSS = """
.badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:8px;margin:0 6px 10px 0}
.badge.cat{background:#eef2ff;color:var(--brand)}
.badge.promo{background:#fff4e5;color:#c2410c}
.badge.wait{background:#f1f3f7;color:var(--muted)}
.disc{margin:18px 0;padding:12px 14px;background:#fff8f1;border:1px solid #ffe2c2;border-radius:10px;font-size:13px;color:#9a3412}
.card p{color:var(--muted);font-size:14px}
.privacy{margin-top:14px;padding:12px 14px;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;font-size:13px;color:#166534}
form label{display:block;font-size:14px;margin:12px 0 4px;color:var(--ink)}
form input,form textarea{margin-bottom:6px}
.note{margin-top:26px;padding:14px;background:#fff;border:1px dashed var(--line);border-radius:12px;font-size:13px;color:var(--muted)}
ul.lic{margin:10px 0;padding-left:20px;list-style:none}
ul.lic li{margin:8px 0;font-size:14px}
"""

SUB_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%%TITLE%%</title>
<meta name="description" content="%%DESC%%">
<meta property="og:title" content="%%TITLE%%">
<meta property="og:description" content="%%DESC%%">
<meta property="og:type" content="website">
<meta property="og:image" content="%%OGIMG%%">
<link rel="canonical" href="%%CANON%%">
<style>%%CSS%%</style>
</head>
<body>
<header><a class="logo" href="/zero-cost-tools/">零成本工具箱</a><nav>%%NAV%%</nav></header>
<main>
<h1>%%H1%%</h1>
<p class="lead">%%LEAD%%</p>
%%BODY%%
</main>
<footer>© 零成本工具箱</footer>
</body>
</html>"""

def _w(rel, html):
    d = os.path.join(ROOT, os.path.dirname(rel))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
        f.write(html)

# ----- 1) 联盟 / CPA 精选 -----
def _aff_cta(o):
    link = AFF_LINKS.get(o["slug"], "")
    if link:
        return ('<a class="btn" href="%s" target="_blank" rel="sponsored noopener">前往领取（推广链接）</a>'
                ' <span class="badge promo">含推广链接</span>' % link)
    return ('<a class="btn ghost" href="%s" target="_blank" rel="noopener">了解 / 注册（公开官网）</a>'
            ' <span class="badge wait">待配置你的推广链接</span>' % o["official_url"])

def gen_deals():
    cards = "\n".join(
        '''  <div class="card">
    <span class="badge cat">%s</span>
    <h3><a href="./%s/" style="color:inherit;text-decoration:none">%s</a></h3>
    <p>%s</p>
    <p><a class="btn ghost" href="./%s/">查看详情</a></p>
  </div>''' % (o["category"], o["slug"], o["title"], o["blurb"], o["slug"])
        for o in AFFILIATE_OFFERS)
    body = ('''<div class="disc">⚠️ 披露：本页及下一级页面包含<strong>联盟 / 推广链接</strong>。若你通过这里的链接注册或购买，本站可能获得佣金，<strong>不会影响你支付的价格</strong>。我们只在你配置好你自己的推广 ID 后才展示返利链接；配置前仅展示平台公开官网。</div>
<div class="cards">
%s
</div>
<div class="note">如何启用你自己的返利：编辑 <code>monetization_content.py</code> 里的 <code>AFF_LINKS</code>，把各 slug 对应的值换成你在对应平台申请的推广链接，重跑 <code>build.py</code> 即可。未配置时本页不展示任何返利链接，仅作信息展示，合法合规。</div>''' % cards)
    html = (SUB_TPL
            .replace("%%NAV%%", NAV_HTML).replace("%%CSS%%", PAGE_CSS)
            .replace("%%TITLE%%", "联盟精选 · 高佣返利")
            .replace("%%DESC%%", "精选可合规返利的联盟计划（京东联盟 / 阿里云推广 / walubee 等），页面已做推广链接披露。")
            .replace("%%H1%%", "联盟精选 · 高佣返利")
            .replace("%%LEAD%%", "把高佣返利计划变成「躺着赚佣金」的合法通道。")
            .replace("%%OGIMG%%", "../og.png")
            .replace("%%CANON%%", BASE + "deals/")
            .replace("%%BODY%%", body))
    _w("deals/index.html", html); print("generated deals/index.html")
    for o in AFFILIATE_OFFERS:
        cta = _aff_cta(o)
        dbody = ('''<div class="disc">⚠️ 披露：本页含联盟 / 推广链接。通过链接注册或购买，本站可能获得佣金，不影响你的价格。</div>
<p class="lead">%s</p>
<p>%s</p>
<div class="note">这是「%s」类目下的一个返利位。配置你自己的推广链接后，上方按钮会变成带你 ID 的返利链接；在此之前点击会跳到该平台<strong>公开官网 / 注册页</strong>（非返利）。</div>'''
                 % (o["blurb"], cta, o["category"]))
        dhtml = (SUB_TPL
                 .replace("%%NAV%%", NAV_HTML).replace("%%CSS%%", PAGE_CSS)
                 .replace("%%TITLE%%", o["title"] + " — 联盟精选")
                 .replace("%%DESC%%", o["blurb"])
                 .replace("%%H1%%", o["title"])
                 .replace("%%LEAD%%", o["blurb"])
                 .replace("%%OGIMG%%", "../../og.png")
                 .replace("%%CANON%%", BASE + "deals/" + o["slug"] + "/")
                 .replace("%%BODY%%", dbody))
        _w("deals/%s/index.html" % o["slug"], dhtml)
        print("generated deals/%s/index.html" % o["slug"])

# ----- 2) 落地页线索（合法 lead-gen） -----
def _lead_form(niche):
    if LEAD_FORM_ENDPOINT:
        action, extra = LEAD_FORM_ENDPOINT, ""
    elif CONTACT_EMAIL:
        action = "mailto:%s?subject=%s" % (CONTACT_EMAIL, "线索合作：" + niche["title"])
        extra = '<p class="privacy">未配置表单端点，提交会唤起你的邮件客户端发往 <b>%s</b>；也可直接邮件联系。</p>' % CONTACT_EMAIL
    else:
        action, extra = "", '<p class="privacy">⚠️ 表单端点待配置：在 <code>monetization_content.py</code> 填 <code>LEAD_FORM_ENDPOINT</code>（如 Formspree）或 <code>CONTACT_EMAIL</code> 后，本表单即可接收线索。</p>'
    return ('''<form method="POST" action="%s">
  <label>邮箱（用于发送你订阅的周报）</label>
  <input type="email" name="email" placeholder="you@example.com" required>
  <label>你的需求 / 想对接的资源</label>
  <textarea name="msg" placeholder="例如：想要 XX 类工具、想商务合作…"></textarea>
  <button class="btn" type="submit">提交</button>
</form>%s
<p class="privacy">我们仅将你填写的信息用于发送你订阅的周报 / 商务对接，<strong>不会出售你的隐私数据</strong>；你可随时退订。</p>''' % (action, extra))

def gen_leads():
    cards = "\n".join(
        '''  <div class="card">
    <h3><a href="./%s/" style="color:inherit;text-decoration:none">%s</a></h3>
    <p>%s</p>
    <p><a class="btn ghost" href="./%s/">查看落地页</a></p>
  </div>''' % (n["slug"], n["title"], n["pitch"], n["slug"])
        for n in LEAD_NICHES)
    body = ('''<p class="lead">垂直落地页收集意向线索（免费周报订阅 / 商务合作），合规对接合作商家。所有页面明确隐私用途，不碰「出售用户数据」的灰色操作。</p>
<div class="cards">
%s
</div>''' % cards)
    html = (SUB_TPL
            .replace("%%NAV%%", NAV_HTML).replace("%%CSS%%", PAGE_CSS)
            .replace("%%TITLE%%", "线索 · 合作落地页")
            .replace("%%DESC%%", "垂直落地页收集意向线索，合规对接合作商家。")
            .replace("%%H1%%", "线索 · 合作落地页")
            .replace("%%LEAD%%", "把流量变成可对接商家的意向线索。")
            .replace("%%OGIMG%%", "../og.png")
            .replace("%%CANON%%", BASE + "leads/")
            .replace("%%BODY%%", body))
    _w("leads/index.html", html); print("generated leads/index.html")
    for n in LEAD_NICHES:
        frm = _lead_form(n)
        dbody = ('''<p class="lead">%s</p>
<h2 style="margin-top:22px">留下信息，领取 / 对接</h2>
%s''' % (n["pitch"], frm))
        dhtml = (SUB_TPL
                 .replace("%%NAV%%", NAV_HTML).replace("%%CSS%%", PAGE_CSS)
                 .replace("%%TITLE%%", n["title"] + " — 线索合作")
                 .replace("%%DESC%%", n["pitch"])
                 .replace("%%H1%%", n["title"])
                 .replace("%%LEAD%%", n["pitch"])
                 .replace("%%OGIMG%%", "../../og.png")
                 .replace("%%CANON%%", BASE + "leads/" + n["slug"] + "/")
                 .replace("%%BODY%%", dbody))
        _w("leads/%s/index.html" % n["slug"], dhtml)
        print("generated leads/%s/index.html" % n["slug"])

# ----- 3) 微 SaaS 付费墙（软付费） -----
def gen_pro():
    pts = "\n".join("<li>%s</li>" % p for p in PRO_TIER["points"])
    body = ('''<p class="lead">%s</p>
<div class="cards"><div class="card" style="grid-column:1/-1">
<span class="badge cat">一次性付费 · 无订阅</span>
<h3>%s</h3>
<ul class="lic">%s</ul>
<div class="price" style="color:var(--ok);font-weight:700;font-size:20px">¥%s</div>
<p><a class="btn" href="/zero-cost-tools/store/order.html">微信 / Ko-fi 付款获取</a></p>
</div></div>
<div class="note">软付费说明：<strong>全部 27 个在线工具永久免费、无广告强制</strong>。Pro 是「离线版 + 批量 + 去广告」的增值包，属于附加付费，不绑架免费用户。付款走微信 / Ko-fi，零平台抽成。</div>'''
            % (PRO_TIER["note"], PRO_TIER["title"], pts, PRO_TIER["price"]))
    html = (SUB_TPL
            .replace("%%NAV%%", NAV_HTML).replace("%%CSS%%", PAGE_CSS)
            .replace("%%TITLE%%", PRO_TIER["title"])
            .replace("%%DESC%%", "免费工具永久免费；Pro 是离线版 + 批量 + 去广告的增值包，微信 / Ko-fi 一次性付款。")
            .replace("%%H1%%", "升级 Pro · 增值包")
            .replace("%%LEAD%%", PRO_TIER["note"])
            .replace("%%OGIMG%%", "../og.png")
            .replace("%%CANON%%", BASE + "pro/")
            .replace("%%BODY%%", body))
    _w("pro/index.html", html); print("generated pro/index.html")

# ----- 4) 信息产品策展：把 low-risk 资源包成第 5 件商店产品 -----
CURATION_ITEMS = []
_cpath = os.path.join(ROOT, "results", "recommended_for_resale.json")
if os.path.isfile(_cpath):
    try:
        CURATION_ITEMS = json.load(open(_cpath, encoding="utf-8"))
    except Exception:
        CURATION_ITEMS = []
if CURATION_ITEMS:
    PRODUCTS.append(dict(slug=CURATION_SLUG, title=CURATION_TITLE, desc=CURATION_DESC,
                         price=CURATION_PRICE, checkout="order.html", license="策展索引 / 付费支持"))
    rows = "\n".join(
        '<li><a href="%s" target="_blank" rel="noopener">%s</a> — 授权：%s，⭐%s<br><span style="color:var(--muted);font-size:13px">%s</span></li>'
        % (it.get("url", ""), it.get("title", ""), it.get("license", ""), it.get("stars", 0), it.get("description", ""))
        for it in CURATION_ITEMS)
    GUIDES[CURATION_SLUG] = (
        '<h2>一、这是什么</h2><p>一份<strong>策展索引</strong>：从 GitHub、PLR 站、公有领域书库筛选出的 low-risk 可授权资源清单。'
        '你付费买到的是「筛选 + 整理 + 授权核对」的劳动成果，原始资源本身依然免费、链接公开，不存在任何搬运或盗版。</p>'
        '<h2>二、资源清单（逐条标注授权）</h2><ul class="lic">%s</ul>'
        '<h2>三、怎么用</h2><p>挑 CC0 / PLR / MIT 的项目，按其授权页原文二次开发或打包成你自己的产品；凡是「禁止商用 / 保留所有权利」的一律排除。'
        '本清单本身就是按这套方法原创整理的，可放心参考。</p>' % rows)

# 生成新工具页
for slug, t in NEW_TOOLS.items():
    meta = next(x for x in ALL_TOOLS if x[0] == slug)
    gen_tool(slug, meta[1], meta[2], meta[3], t["h1"], t["lead"], t["body"], t["js"])

# 生成 Hub / 根页
blog_files = sorted(f for f in os.listdir(os.path.join(ROOT, "blog")) if f.endswith(".html") and f != "index.html")
blog_cards = "\n".join(
    f'  <a class="card" href="./blog/{f}"><h3>{BLOG_TITLES.get(f, f.replace(".html","").replace("-"," ").title())}</h3><p>使用教程与技巧</p></a>' for f in blog_files)
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
<meta property="og:image" content="og.png">
<meta property="og:type" content="website">
<link rel="canonical" href="{BASE}">
<link rel="alternate" type="application/atom+xml" title="零成本工具箱" href="atom.xml">
<script type="application/ld+json">{jsonld("", "零成本工具箱", "免费在线工具集合")}</script>
<script type="application/ld+json">{jsonld_website()}</script>
<style>{SHARED_CSS}</style>
</head>
<body>
<header><a class="logo" href="/zero-cost-tools/">零成本工具箱</a><nav>{NAV_HTML}</nav></header>
<main>
<h1>零成本工具箱</h1>
<p class="lead">{len(ALL_TOOLS)} 个免费在线工具，全部在你的浏览器本地运行，不上传数据、无水印、无广告骚扰。</p>
<div class="cards">
{cards}
</div>
<h2 style="margin-top:34px">📚 使用教程</h2>
<div class="cards">
{blog_cards}
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

# 数字商店（数据驱动，从 PRODUCTS）
gen_store()
gen_store_details()
gen_order()

# 四条变现通道页面
gen_deals()
gen_leads()
gen_pro()

# sitemap.xml
now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
store_urls = [BASE + "store/"]
store_urls += [BASE + "store/" + p["slug"] + "/" for p in PRODUCTS]
store_urls += [BASE + "store/order.html"]
deal_urls = [BASE + "deals/"] + [BASE + "deals/" + o["slug"] + "/" for o in AFFILIATE_OFFERS]
lead_urls = [BASE + "leads/"] + [BASE + "leads/" + n["slug"] + "/" for n in LEAD_NICHES]
pro_urls = [BASE + "pro/"]
policy_urls = [BASE + p for p in ("privacy/", "about/", "contact/")]
urls = ([BASE] + store_urls + deal_urls + lead_urls + pro_urls + policy_urls
        + [BASE + s + "/" for s, *_ in ALL_TOOLS] + [BASE + "blog/" + f for f in blog_files])
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
for f in blog_files:
    bt = BLOG_TITLES.get(f, f.replace(".html", "").replace("-", " ").title())
    atom += f'''<entry><title>{bt}</title><id>{BASE}blog/{f}</id><updated>{now}T00:00:00Z</updated><link href="{BASE}blog/{f}"/><summary>使用教程</summary></entry>
'''
atom += f'''<entry><title>数字产品商店</title><id>{BASE}store/</id><updated>{now}T00:00:00Z</updated><link href="{BASE}store/"/><summary>可合规转售的数字产品（PLR / CC0 / 公有领域 / MIT）</summary></entry>
'''
for _t, _u, _s in (("联盟精选", BASE + "deals/", "高佣返利计划精选，含推广链接披露"),
                   ("线索·合作落地页", BASE + "leads/", "垂直落地页收集意向线索，合规对接商家"),
                   ("升级 Pro · 增值包", BASE + "pro/", "免费工具永久免费，Pro 为离线版+批量+去广告增值包")):
    atom += f'''<entry><title>{_t}</title><id>{_u}</id><updated>{now}T00:00:00Z</updated><link href="{_u}"/><summary>{_s}</summary></entry>
'''
for _t, _u in (("隐私政策", BASE + "privacy/"), ("关于本站", BASE + "about/"),
               ("联系 / 合作", BASE + "contact/")):
    atom += f'''<entry><title>{_t}</title><id>{_u}</id><updated>{now}T00:00:00Z</updated><link href="{_u}"/><summary>法律与信任页面</summary></entry>
'''
atom += "</feed>\n"
with open(os.path.join(ROOT, "atom.xml"), "w", encoding="utf-8") as f:
    f.write(atom)
print("generated atom.xml")

print("ALL DONE")
