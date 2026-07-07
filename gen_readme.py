#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 ALL_TOOLS 自动生成 README.md（完整工具清单 + 在线链接 + 徽章）。"""
import build

BASE = build.BASE
rows = "\n".join(
    f"| {t} | {d} | [{s}/]({BASE}{s}/) |" for s, t, d, k in build.ALL_TOOLS)
n = len(build.ALL_TOOLS)

md = f"""# 零成本工具箱 / Zero-Cost Tools

> 免费、注重隐私的纯前端在线工具合集。所有处理都在浏览器本地完成，图片与数据**不会上传到任何服务器**。

🔗 **在线使用：{BASE}**

![GitHub Pages](https://img.shields.io/badge/hosted-GitHub%20Pages-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Privacy](https://img.shields.io/badge/privacy-本地运行-important)
![Tools](https://img.shields.io/badge/tools-{n}-orange)

## 工具列表（{n} 款，全部免费、本地运行）

| 工具 | 说明 | 在线链接 |
|---|---|---|
{rows}

## 特点

- 🆓 完全免费，无需注册
- 🔒 隐私安全：纯前端运行，不上传数据
- ⚡ 零服务器成本：托管于 GitHub Pages 免费额度
- 📱 响应式设计，移动端可用
- 🔎 每款工具配有 SEO 教程与结构化数据，易于被搜索引擎发现

## 本地运行

直接用浏览器打开仓库内对应 `index.html` 即可，无需任何依赖或构建步骤。

## 许可证

MIT — 自由使用、修改、分发。
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(md)
print("README.md generated, tools:", n)
