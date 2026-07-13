# 自动化执行记录

## 2026-07-10 (运行)
- 新增工具：**passphrase（密码短语生成器）**——纯前端，常见单词+分隔符生成好记高强度密码短语，已加入 build.py 的 ALL_TOOLS + NEW_TOOLS。
- 严重构建 Bug 修复：`build.py` 的 `gen_tool()` 只拼接 HTML 却**从未写入磁盘**，导致所有工具页（含新工具）都不会被生成。补上 `os.makedirs + open().write()` 后，全站工具页现已能正确生成（此前很多工具页是陈旧的历史提交版本，本次一并刷新）。
- backlog.txt 清理：移除了已在过往运行中上线的重复点子（regex/number-base/lorem/percent-calc/roman-numeral/dedup/hash/randnum/rmb-upper），仅保留 8 条未实现点子；passphrase 已写入 done.txt。
- IndexNow 状态：**HTTP 200**（本轮 90 个 URL，含 passphrase）。
- 校验：全站 *.html 无 `%%` 占位符残留。
- 提交并推送：commit 7c68b8b（fix + 上线 passphrase 页）。
- 部署抽查：passphrase/、首页、passphrase-guide.html 均返回 **HTTP 200**。
- 注意：promote.py 的 Wayback 存档 + X 自动发帖（post_x.py, 160s 超时）耗时较长，且 stdout 重定向时块缓冲导致日志需等进程结束才落盘；用 PYTHONUNBUFFERED=1 可实时读 IndexNow。
