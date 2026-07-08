# -*- coding: utf-8 -*-
"""
products_content.py — 原创数字产品（由 WorkBuddy 撰写，零成本、完全可授权销售）。

为什么是「原创」而不是「搬运免费资源倒卖」：
- 搬运他人免费资源再标价出售，往往构成误导（买家付了钱拿到本可免费取得的文件），
  且很多「免费分享」资源并未授予转售权，存在下架与法律风险。
- 这里上架的是**我（AI）原创撰写的指南/清单**：内容由本项目生成、版权归作者，
  可合规标价出售或免费公开 + 微信打赏支持，零成本、零版权纠纷。

checkout 统一指向 store/order.html（微信扫码下单/支持）。
每个产品配有可读的产品详情页（store/<slug>/index.html），内容同时作为 SEO 长尾页。
"""

PRODUCTS = [
    dict(slug="zero-cost-earn-handbook",
         title="零成本数字产品变现实操手册",
         desc="手把手讲清 CC0 / 公有领域 / PLR / MIT 的区别，4 步把免费可授权资源变成可售商品，并列出必须避开的侵权与违规红线。",
         price="9.9",
         checkout="order.html",
         license="原创内容 / 付费支持"),
    dict(slug="free-apis-directory",
         title="100+ 免费可商用 API 与素材清单",
         desc="按「无 Key API / CC0 图库 / 公有领域书库 / 免费字体图标 / PLR 站」分类整理的可用资源目录，每条标注授权，拿来即做产品。",
         price="12.9",
         checkout="order.html",
         license="原创内容 / 付费支持"),
    dict(slug="tool-site-seo-playbook",
         title="用 AI 零成本做工具站挣广告费",
         desc="本项目同款打法：纯前端工具零服务器成本、GitHub Pages 免费托管、SEO 收录与长尾内容、流量如何转广告/捐赠。可直接复刻。",
         price="9.9",
         checkout="order.html",
         license="原创内容 / 付费支持"),
    dict(slug="secondhand-compliance",
         title="二手平台合规副业避坑指南",
         desc="讲清闲鱼等平台的自动回复/爬虫机器人为什么违规、法律边界在哪，以及不踩坑的合规替代方案（人工闲置、信息差选品、引流自有站）。",
         price="6.9",
         checkout="order.html",
         license="原创内容 / 付费支持"),
]

GUIDES = {
    "zero-cost-earn-handbook": """
<h2>一、先分清四种「免费」的本质</h2>
<p>不是所有「免费」都能拿去卖。按授权从松到紧：</p>
<ul>
  <li><b>CC0 / 公有领域</b>：作者放弃一切权利，可任意复制、改作、商用、转售。最安全。</li>
  <li><b>PLR（Private Label Rights，私有标签权）</b>：明确授权你改品牌、打包、转售。注意看清是否含「二级转售权（MRR）」。</li>
  <li><b>MIT / Apache / BSD 等开源协议</b>：可自由使用、修改、再分发，但「原样转卖一个 GitHub 仓库」价值很低且对买家不公平——更好的做法是把它作为你产品的<em>组成部分</em>，加上你自己的说明与服务。</li>
  <li><b>「免费分享但未声明授权」</b>：默认是「保留所有权利」，<b>不能</b>转售。这类一律排除。</li>
</ul>

<h2>二、把免费可授权资源变成商品的 4 步</h2>
<ol>
  <li><b>找</b>：用许可感知采集器（本项目 <code>scripts/collect_resources.py</code>）只收 low 风险（CC0/PLR/明确可商用）来源。</li>
  <li><b>筛</b>：逐条核对授权页原文，凡是「禁止商用 / 仅个人使用 / 保留所有权利」直接丢弃。</li>
  <li><b>改品牌 + 增值</b>：重排版、配原创说明、做成「精选包 / 实操指南」，让买家为「筛选 + 整理 + 讲解」付费，而不是为原本免费的文件付费。</li>
  <li><b>上架</b>：挂到自有商店（如本站 store/），结账走微信 / Stripe Payment Link / Ko-fi，零平台抽成。</li>
</ol>

<h2>三、必须避开的红线</h2>
<ul>
  <li>不卖盗版电子书、破解课程、付费软件——这是侵权，不是「信息差」。</li>
  <li>不用闲鱼 / 转转的自动回复、爬虫机器人变现（违反平台规则、牵连实名账号，作者也声明「仅供学习」）。</li>
  <li>不把「免费但无授权」的资源标成可售。</li>
  <li>永远在商品页写清授权来源，让买家买得明白。</li>
</ul>
<p>守住院子，长期才能稳定收款。本手册就是按这套方法原创写成的，可放心转售。</p>
""",

    "free-apis-directory": """
<h2>一、免费无 Key API（可直接调用、可商用）</h2>
<ul>
  <li><b>ExchangeRate-API</b>（open endpoint）：实时汇率，免 key，需署名，可缓存。</li>
  <li><b>FreeAPI</b>（freeapi.app，MIT）：auth / e-commerce / social 等真实端点，免 key 免配额。</li>
  <li><b>public-apis</b>（GitHub 清单）：聚合大量免费 API，挑标注「No Auth / MIT」的用。</li>
  <li><b>aisense-free-public-rest-apis</b>：无 key / 无限额 REST API 合集。</li>
</ul>

<h2>二、CC0 / 可商用图库与素材</h2>
<ul>
  <li><b>Unsplash / Pexels / Pixabay</b>：海量可商用图片与视频，无需署名（建议仍署名）。</li>
  <li><b>Lucide / Heroicons / Tabler</b>：MIT 图标，可打包进你的产品。</li>
  <li><b>Google Fonts / OFL 字体</b>：可商用，可随产品分发。</li>
</ul>

<h2>三、公有领域内容（可合法转售）</h2>
<ul>
  <li><b>Project Gutenberg</b>：超过 7 万本进入公有领域的电子书，可打包成主题书单出售。</li>
  <li><b>Wikimedia Commons（公有领域类）</b>：筛选 License=Public Domain 的文件。</li>
  <li>注意：只选真正进入公有领域的作品（通常 1928 年前），《Atomic Habits》等现代书仍受版权。</li>
</ul>

<h2>四、PLR 资源站（明确可转售）</h2>
<ul>
  <li><b>PLR Database</b>（plrdatabase.net）：2 万+ 可再品牌产品，含免费样品。</li>
  <li><b>Entrepedia</b>（entrepedia.co）：免费 PLR 电子书 / 课程 / 模板。</li>
  <li>上架前务必打开授权页确认含「resell rights」，并看清是否允许二级转售。</li>
</ul>
<p>完整清单（含每个条目的授权备注与直接用法的 100+ 条）已整理在本站对应产品页，持此清单即可零成本启动你自己的数字产品。</p>
""",

    "tool-site-seo-playbook": """
<h2>一、为什么是「纯前端工具站」</h2>
<p>工具站是 Google 官方点名的、稳定靠广告赚钱的三类网站之一。纯前端工具：</p>
<ul>
  <li><b>零服务器成本</b>：全部在浏览器本地运行，文件托管在 GitHub Pages / Netlify 免费额度即可。</li>
  <li><b>零 API 费用</b>：压缩、格式转换、哈希等都在客户端算，不调后端。</li>
  <li><b>隐私友好</b>：文件不上传，天然适合做「隐私优先」的卖点。</li>
</ul>

<h2>二、本项目的具体打法（可直接复刻）</h2>
<ol>
  <li><b>造工具</b>：用统一生成器（<code>build.py</code>）批量产出工具页，新增一个工具只改数据。</li>
  <li><b>做 SEO 地基</b>：sitemap.xml、robots.txt、Open Graph、JSON-LD 结构化数据（WebSite / WebApplication / BreadcrumbList / Article / FAQPage）。</li>
  <li><b>每日自动收录</b>：IndexNow（Bing/Yandex/Naver 秒收）、Yandex ping、Ping-O-Matic、Wayback 存档——全部零账号、零成本、可定时跑。</li>
  <li><b>长尾内容</b>：每个工具配一篇教程（含 FAQ + 内链），搏 Google 自然搜索。</li>
  <li><b>变现接入</b>：流量起来后接 AdSense 广告；在此之前用微信 / Ko-fi 捐赠 + 数字产品商店先收。</li>
</ol>

<h2>三、收入公式与耐心</h2>
<p>收入 = 流量 × 转化率 × 客单价。前几周靠 SEO 长尾慢慢积累，<b>没有捷径</b>；
但一旦权重起来，工具站是「建一次、长期被动」的资产。本手册就是把这套方法拆给你照做。</p>
""",

    "secondhand-compliance": """
<h2>一、闲鱼机器人为什么不能用来赚钱</h2>
<ul>
  <li><b>违反平台规则</b>：闲鱼服务条款禁止自动化访问、机器人、自动回复，使用必遭封号，且牵连你的实名账号。</li>
  <li><b>需要你的身份</b>：这类工具都依赖你本人的账号 + Cookie（= 实名身份），违规后果自负。</li>
  <li><b>作者自带免责</b>：多个开源仓库明确写「仅供学习研究」「数据不得商用」——商用即违背作者意愿与平台规则。</li>
  <li><b>法律边界</b>：规模化爬取 / 自动化可能触及《网络安全法》关于未经授权干扰网络服务的规定。</li>
</ul>
<p>结论：<b>不把闲鱼机器人用于变现</b>。想做二手 / 信息差生意，走下面合规路径。</p>

<h2>二、合规替代方案</h2>
<ol>
  <li><b>人工卖自有闲置</b>：自己用不上的东西拍照上架，最稳，不碰自动化。</li>
  <li><b>信息差选品</b>：用监控工具<em>仅作自用比价 / 捡漏提醒</em>，发现低价后自己手动下单转卖，不爬商用数据。</li>
  <li><b>内容引流到自有站</b>：在闲鱼 / 转转发「实用干货」帖，把人引到你的工具站 / 公众号，最终在自有阵地用微信 / 广告变现——规则风险最低。</li>
  <li><b>原创数字产品</b>：像本站 store/ 那样卖你自己的指南 / 清单，不依赖任何平台账号，零封号风险。</li>
</ol>
<p>本指南帮你把「想赚快钱」的冲动，落到不踩坑的长期做法上。</p>
""",
}
