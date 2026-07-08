# 你只需做这几步（一次性登录 / 开关）

机器（我）已经把「除了你本人身份验证之外」的一切都建好了。下面每一条都是**非我不可**的
物理动作，按顺序做即可让整条变现链转起来。每条都标注了预计耗时。

---

## 0. 先填配置（2 分钟）
编辑 `monetization_content.py`，把空字符串换成你自己的：
- `CONTACT_EMAIL`：你的接收邮箱（线索页兜底用）
- `LEAD_FORM_ENDPOINT`：可选，Formspree/Getform 的 POST URL（不填则用 mailto 兜底）
- `AFF_LINKS`：各平台的**推广链接**（完成第 2 步注册后粘回来）
- `ADSENSE_CLIENT` / `ADSENSE_SLOT`：过审 AdSense 后填（见 `ADSENSE_APPLY.md`）
- `ACCOUNT_INFO`：昵称 + 邮箱（仅用于第 2 步自动填表，不外泄）

填完运行（本地预览 + 让每日自动机部署）：
```
python build.py
```

---

## 1. GitHub Sponsors（5 分钟）— 最快到账的打赏
1. 打开 https://github.com/sponsors/ckstc/settings
2. 点「Become a sponsorable user / 加入 Sponsors」，完成赞助资料、设置赞助档位。
3. 按提示绑定 **Stripe** 收款账户（需本人实名 + 银行卡/税务信息）。
4. 开启两步验证（GitHub 强制要求）。
完成即生效：仓库已配置 `.github/FUNDING.yml`（ko-fi + github），访客点「Sponsor」可直接打赏，
钱进你的 Stripe。⚠️ 全程需本人实名，AI 无法代做。

---

## 2. 联盟 / 返利注册（各 2 分钟，免费）
两个都免费加入、合法：
- **walubee**（70% 分成）：https://www.walubee.com/affiliate
- **GoogieHost**（$0.25/免费注册）：https://googiehost.com/affiliates

自动化方式：
```
python automation/affiliate_signup.py
```
脚本会打开浏览器自动填表，**在「邮箱验证 / CAPTCHA / 密码」处暂停**，你处理完按回车即可。
注册成功后在后台复制你的推广链接，粘回 `AFF_LINKS['walubee']` / `AFF_LINKS['googiehost']`，
重跑 `python build.py`，`/deals/` 页就开始真正返利。
（也可直接网页手动注册，更快。）

---

## 3. AdSense（20 分钟 + 等审核）
见 `ADSENSE_APPLY.md`。要点：用本人 Google 账号申请 → 填 `ADSENSE_CLIENT` 让构建注入代码 →
等审核 → 收 PIN 明信片绑定提现。需本人实名，AI 不能代提交/代收 PIN。

---

## 4. 种子流量（一次性，约 10 分钟，之后全自动长尾）
```
python automation/seed_traffic.py
```
脚本依次打开 Reddit / V2EX / 知乎 / 微博，在**登录处暂停**，你登录后它自动发预写文案
（文案在 `promo_content.py`，都是「先给价值再带链接」、符合版规，不 spam）。
朋友圈无稳定网页端，脚本只打印文案，你手动粘贴。
发完这一波即触发第一批访客；之后靠 SEO 长尾持续累积，无需重复手动发。

---

## 之后全自动的部分
- 每日自动机（`零成本工具站·自动推广与扩张`）会自动：重新构建、提交 sitemap/IndexNow/ping、
  把新页面收录进搜索引擎 —— 你不用管。
- 资源采集器（`scripts/collect_resources.py`）持续产出可合规转售资源，刷新 `/store/` 策展产品。

## 一句话
你只做「实名 + 登录 + 粘链接」这三件机器代不了的事，其余全在跑。完成上面 1–4，
第一笔收入（Sponsors 打赏 / 联盟返利 / 微信扫码）就只差「有人点进来」。
