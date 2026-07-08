# AdSense 申请清单（一次性，约 20 分钟 + 等待审核）

目标：让工具站通过 Google AdSense 审核，开启展示广告收益。
前置（本项目已实现）：

- ✅ 站点已上线且内容原创、稳定可访问：`https://ckstc.github.io/zero-cost-tools/`
- ✅ 已生成 `privacy.html`（隐私政策，含 Cookie/广告说明）、`about.html`、`contact.html`
- ✅ 已在 `build.py` 预留广告位：把你的发布商 ID 填进 `monetization_content.py` 的
  `ADSENSE_CLIENT`（形如 `ca-pub-1234567890`），重跑 `python build.py` 即自动注入广告代码。

## 你的一次性步骤
1. 打开 https://www.google.com/adsense/ 用**你本人的 Google 账号**登录（建议与 GitHub 同一邮箱，便于管理）。
2. 点「立即开始 / Get started」，输入站点地址 `https://ckstc.github.io/zero-cost-tools/`。
3. 把 AdSense 给的**验证代码片段**粘到站点 `<head>` —— 本项目已自动化：
   - 填好 `ADSENSE_CLIENT` 后，`build.py` 会在每个页面注入 `<script async src=...adsbygoogle.js?client=...>`。
   - 你无需手动改 HTML，重跑构建即可。
4. 提交，等待 Google 审核（通常数天到数周）。审核期间保持站点可访问、不要改动结构。
5. 审核通过后，在 AdSense 后台建「自动广告」或「展示广告单元」，把 `data-ad-slot` 填进
   `ADSENSE_SLOT` 即可在指定位置展示。
6. **地址验证**：首次收益达到阈值前，Google 会邮寄一张含 PIN 的明信片到你填的地址，
   收到后回 AdSense 输入 PIN 才能提现。这是必须本人处理的物理步骤。

## 重要现实
- AdSense **有最低流量门槛意识**：内容合规只是入场券，真正产生收益靠**访客量**。
  当前站点 0 访客 → 即使通过审核也是 ¥0。先把种子流量（`automation/seed_traffic.py`）跑起来。
- 不要为了过审堆垃圾内容或诱导点击，会被永久封号且冻结余额。
- 收益结算到你的 AdSense 账户 → 绑定银行卡/_address 提现，需本人实名。

## 自动化能做的 / 不能做的
- 能：准备好隐私/关于/联系页、广告位代码注入、把申请所需字段整理好。
- 不能：替你点「提交申请」、替你收 PIN 明信片、替你绑定银行卡 —— 这些必须本人。
