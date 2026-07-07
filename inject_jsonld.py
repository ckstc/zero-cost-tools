#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给现有 6 个工具页注入 JSON-LD 结构化数据（若尚未存在）。"""
import os, json
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://ckstc.github.io/zero-cost-tools/"
META = {
    "compress":  ("图片压缩工具", "在线压缩 JPG/PNG/WebP，本地处理不上传，免费无水印"),
    "jsonfmt":   ("JSON 格式化工具", "在线 JSON 美化/压缩/校验，本地运行，保护隐私"),
    "pdf":       ("PDF 工具箱", "在线压缩 PDF、PDF 转图片，纯前端处理不泄露文件"),
    "qrcode":    ("二维码生成器", "免费生成网址/文本/ WiFi 二维码，可下载 PNG"),
    "convert":   ("单位换算器", "长度/重量/温度/面积等单位在线换算"),
    "password":  ("密码生成器", "生成高强度随机密码，可自定义长度与字符集"),
}
for slug,(title,desc) in META.items():
    p = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(p):
        print("skip (missing)", slug); continue
    html = open(p, encoding="utf-8").read()
    if "application/ld+json" in html:
        print("already has jsonld", slug); continue
    data = json.dumps({
        "@context":"https://schema.org","@type":"WebApplication","name":title,
        "description":desc,"url":BASE+slug+"/",
        "applicationCategory":"UtilitiesApplication","operatingSystem":"Any",
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}, ensure_ascii=False)
    blob = f'<script type="application/ld+json">{data}</script>\n</head>'
    html = html.replace("</head>", blob, 1)
    open(p, "w", encoding="utf-8").write(html)
    print("injected jsonld", slug)
print("DONE")
