# 零成本工具箱 / Zero-Cost Tools

> 免费、注重隐私的纯前端在线工具合集。所有处理都在浏览器本地完成，图片与数据**不会上传到任何服务器**。

🔗 **在线使用：https://ckstc.github.io/zero-cost-tools/**

![GitHub Pages](https://img.shields.io/badge/hosted-GitHub%20Pages-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Privacy](https://img.shields.io/badge/privacy-本地运行-important)
![Tools](https://img.shields.io/badge/tools-24-orange)
![Sponsor](https://img.shields.io/badge/sponsor-%E2%98%95%20Ko--fi%20%2F%20GitHub%20Sponsors-pink)

## 工具列表（24 款，全部免费、本地运行）

| 工具 | 说明 | 在线链接 |
|---|---|---|
| 图片压缩工具 | 在线压缩 JPG/PNG/WebP，本地处理不上传，免费无水印 | [compress/](https://ckstc.github.io/zero-cost-tools/compress/) |
| JSON 格式化工具 | 在线 JSON 美化/压缩/校验，本地运行，保护隐私 | [jsonfmt/](https://ckstc.github.io/zero-cost-tools/jsonfmt/) |
| PDF 工具箱 | 在线压缩 PDF、PDF 转图片，纯前端处理不泄露文件 | [pdf/](https://ckstc.github.io/zero-cost-tools/pdf/) |
| 二维码生成器 | 免费生成网址/文本/ WiFi 二维码，可下载 PNG | [qrcode/](https://ckstc.github.io/zero-cost-tools/qrcode/) |
| 单位换算器 | 长度/重量/温度/面积等单位在线换算 | [convert/](https://ckstc.github.io/zero-cost-tools/convert/) |
| 密码生成器 | 生成高强度随机密码，可自定义长度与字符集 | [password/](https://ckstc.github.io/zero-cost-tools/password/) |
| 字数统计工具 | 实时统计中英文单词、字符、句子、行数 | [word-counter/](https://ckstc.github.io/zero-cost-tools/word-counter/) |
| 大小写转换工具 | 英文大小写、标题化、句首大写一键转换 | [case-converter/](https://ckstc.github.io/zero-cost-tools/case-converter/) |
| URL 编解码工具 | 在线 URL 编码/解码，处理中文与特殊字符 | [url-codec/](https://ckstc.github.io/zero-cost-tools/url-codec/) |
| Base64 编解码 | 文本 Base64 编码/解码，支持中文 UTF-8 | [base64-codec/](https://ckstc.github.io/zero-cost-tools/base64-codec/) |
| 时间戳转换工具 | Unix 时间戳与日期互转，支持本地/UTC | [timestamp/](https://ckstc.github.io/zero-cost-tools/timestamp/) |
| Markdown 预览器 | 实时 Markdown 渲染预览，离线可用 | [markdown/](https://ckstc.github.io/zero-cost-tools/markdown/) |
| 文本对比工具 | 逐行对比两段文本差异，新增删除高亮 | [text-diff/](https://ckstc.github.io/zero-cost-tools/text-diff/) |
| CSV JSON 互转 | CSV 与 JSON 在线互转，首行作表头 | [csv-json/](https://ckstc.github.io/zero-cost-tools/csv-json/) |
| UUID 生成器 | 生成 RFC4122 v4 UUID，支持批量 | [uuid/](https://ckstc.github.io/zero-cost-tools/uuid/) |
| 颜色值转换 | HEX/RGB/HSL 互转，取色器 | [color-hex/](https://ckstc.github.io/zero-cost-tools/color-hex/) |
| 进制转换器 | 二进制/八进制/十进制/十六进制在线互转 | [number-base/](https://ckstc.github.io/zero-cost-tools/number-base/) |
| 文本哈希工具 | 生成 SHA-1/SHA-256/SHA-512 摘要，本地运算不上传 | [hash/](https://ckstc.github.io/zero-cost-tools/hash/) |
| 正则表达式测试 | 在线测试正则，高亮匹配结果，支持语法选项 | [regex/](https://ckstc.github.io/zero-cost-tools/regex/) |
| 文本去重工具 | 按行去除重复内容保留顺序，本地处理 | [dedup/](https://ckstc.github.io/zero-cost-tools/dedup/) |
| URL 别名生成 | 把标题转换为 SEO 友好的 URL slug（短链接别名） | [slug/](https://ckstc.github.io/zero-cost-tools/slug/) |
| 占位文本生成器 | 一键生成 Lorem Ipsum 段落，可调数量 | [lorem/](https://ckstc.github.io/zero-cost-tools/lorem/) |
| 词频统计工具 | 统计文本中词语出现频率，导出结果 | [wordfreq/](https://ckstc.github.io/zero-cost-tools/wordfreq/) |
| 随机数生成器 | 生成指定范围与数量的随机整数，可去重 | [randnum/](https://ckstc.github.io/zero-cost-tools/randnum/) |

## 特点

- 🆓 完全免费，无需注册
- 🔒 隐私安全：纯前端运行，不上传数据
- ⚡ 零服务器成本：托管于 GitHub Pages 免费额度
- 📱 响应式设计，移动端可用
- 🔎 每款工具配有 SEO 教程与结构化数据，易于被搜索引擎发现

## 本地运行

直接用浏览器打开仓库内对应 `index.html` 即可，无需任何依赖或构建步骤。

## 数字商店 & 资源采集（变现路径）

本项目在“免费工具站 + 广告/打赏”之外，额外提供一条**合规转售数字产品**的路径：

- **`store/` 数字商店**：纯静态店面，由 `build.py` 的 `PRODUCTS` 列表数据驱动生成。
  上架方式：在 `build.py` 的 `PRODUCTS` 里加一条 `dict(slug, title, desc, price, checkout, license)`，
  把 `checkout` 填成你的 Ko-fi 商店 / Stripe Payment Link / 自有收款页，重跑 `python build.py` 即可。
  ⚠️ 仅上架**明确可转售授权**的资源（PLR / CC0 / 公有领域 / MIT）。
- **`scripts/collect_resources.py` 资源采集器**：用 Playwright 批量搜索“免费分享”的网络资源，
  并做**许可感知分级**（low 可直接转售 / medium 待人工复核 / high 明确禁止→排除）。
  自检（无需浏览器）：`python scripts/collect_resources.py --selftest`
  实跑（需先 `pip install playwright && playwright install chromium`）：
  `python scripts/collect_resources.py --all --out results/collected.json`

## ☕ 赞助作者 / Sponsor

如果这个工具箱帮到了你，欢迎请作者喝杯咖啡 ☕：

- **GitHub Sponsors**：点仓库右上角「Sponsor」按钮，用 GitHub 绑定信用卡直接打赏（仓库已配置 `.github/FUNDING.yml`）。开启 Sponsors 需本人绑定 Stripe 收款（一次性）。
- **Ko-fi**：https://ko-fi.com/ckstc
- **微信扫码**：见任意工具页底部的收款码。

所有赞助都用于维持站点与持续开发，感谢支持 ❤️

## 许可证

MIT — 自由使用、修改、分发。
