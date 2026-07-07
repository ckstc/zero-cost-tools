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
}

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
  <a class="logo" href="../">零成本工具箱</a>
  <nav><a href="../">全部工具</a></nav>
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
<header><a class="logo" href="./">零成本工具箱</a><nav><a href="./">全部工具</a></nav></header>
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

# sitemap.xml
now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
urls = [BASE] + [BASE + s + "/" for s, *_ in ALL_TOOLS] + [BASE + "blog/" + f for f in blog_files]
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
atom += "</feed>\n"
with open(os.path.join(ROOT, "atom.xml"), "w", encoding="utf-8") as f:
    f.write(atom)
print("generated atom.xml")

print("ALL DONE")
