# 四条变现通道 · 一次性配置位

本文件说明 `monetization_content.py` 里**需要你本人账号**的空槽。留空时页面会标注「待配置」并只放平台公开官网，**绝不伪造或盗用任何人的返利 ID**。

## 1) 联盟 / CPA 精选（`/deals/`）
- 配置：编辑 `monetization_content.py` 的 `AFF_LINKS`，把各 slug 对应值换成你在对应平台申请的**推广链接**。
  ```python
  AFF_LINKS = {
      "jd-union": "https://u.jd.com/你的推广位",
      "aliyun-promo": "https://www.aliyun.com/你的推广链接",
      "walubee": "https://walubee.com/?ref=你的ID",
  }
  ```
- 已内置的合法返利计划：京东联盟、阿里云推广、walubee(70%)、GoogieHost、Namecheap。
- **合规要求**：所有联盟页已强制展示「含推广链接」披露与「不影响你的价格」声明（FTC 式），无需你额外处理。

## 2) 落地页线索（`/leads/`）
- 配置（二选一）：
  - `LEAD_FORM_ENDPOINT = "https://formspree.io/f/xxxx"` —— 免费表单服务（Formspree/Getform）的 POST 端点，线索自动进你邮箱。
  - 或 `CONTACT_EMAIL = "you@example.com"` —— 未配端点时表单用邮件兜底。
- 页面仅做「免费周报订阅 / 商务合作」收集，并写明隐私用途（不出售用户数据）。

## 3) 微 SaaS 付费墙（`/pro/`）
- 软付费：27 个在线工具**永久免费**；Pro 是「离线版+批量+去广告」增值包，¥39.9 一次性，走 `store/order.html` 的微信/Ko-fi。
- 无需额外配置，已生效。

## 4) 信息产品策展（`/store/curated-free-resources/`）
- 自动：只要 `results/recommended_for_resale.json` 存在且有 low-risk 条目，构建时自动上架为第 5 件商店产品（策展索引，非搬运）。
- 运行 `scripts/collect_resources.py` 可刷新该清单（许可感知，只收 CC0/PLR/MIT）。

## 部署
- 本地改完重跑 `python build.py`，由每日自动机（在主机上下文有 git 权限）推上 GitHub Pages。
- 或在 GitHub 连接器点「信任」让我直接 push。
