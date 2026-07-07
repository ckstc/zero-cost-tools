#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通过 GitHub API 设置仓库 metadata：主页、双语描述、topics（提升发现面）。"""
import os, json, subprocess, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://ckstc.github.io/zero-cost-tools/"

# 从 git credential helper 取 token
out = subprocess.run(["git", "credential", "fill"],
                     input="protocol=https\nhost=github.com\n",
                     capture_output=True, text=True).stdout
TOKEN = ""
for line in out.splitlines():
    if line.startswith("password="):
        TOKEN = line.split("=", 1)[1].strip()
if not TOKEN:
    print("NO TOKEN"); raise SystemExit(1)

payload = {
    "description": "免费在线工具箱：图片压缩/JSON/PDF/二维码/单位换算/密码/开发小工具等 24 款纯前端工具，本地运行保护隐私。Free online tools: image compress, JSON, PDF, QR, converter, dev utilities — 24 local-first privacy tools.",
    "homepage": BASE,
    "topics": ["tools", "free-tools", "web-tools", "utilities", "privacy",
               "static-site", "online-tools", "developer-tools", "productivity",
               "html", "javascript"]
}
req = urllib.request.Request(
    "https://api.github.com/repos/ckstc/zero-cost-tools",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {TOKEN}",
             "Accept": "application/vnd.github+json"},
    method="PATCH")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode())
    print("PATCH status:", r.status)
    print("homepage:", d.get("homepage"))
    print("topics:", d.get("topics"))
    print("description:", d.get("description"))
