#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成品牌 OG 分享图 og.png (1200x630)，用于社交分享卡片。"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "og.png")

def load_font(size, bold=False):
    candidates = [
        r"C:/Windows/Fonts/msyhbd.ttc" if bold else r"C:/Windows/Fonts/msyh.ttc",
        r"C:/Windows/Fonts/msyh.ttf",
        r"C:/Windows/Fonts/simhei.ttf",
        r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                continue
    return ImageFont.load_default()

W, H = 1200, 630
img = Image.new("RGB", (W, H), (247, 248, 250))
d = ImageDraw.Draw(img)

# 背景渐变（左上深蓝 -> 右下浅蓝）
top = (47, 109, 246)
bot = (120, 170, 250)
for y in range(H):
    t = y / H
    r = int(top[0] + (bot[0] - top[0]) * t)
    g = int(top[1] + (bot[1] - top[1]) * t)
    b = int(top[2] + (bot[2] - top[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 半透明卡片
d.rounded_rectangle([90, 120, W - 90, H - 120], radius=28, fill=(255, 255, 255))

title = load_font(76, bold=True)
sub = load_font(34)
small = load_font(26)

d.text((W // 2, 230), "零成本工具箱", font=title, fill=(31, 36, 48), anchor="mm")
d.text((W // 2, 330), "免费在线工具集合", font=sub, fill=(47, 109, 246), anchor="mm")
d.text((W // 2, 400), "本地运行 · 隐私优先 · 24 款实用工具", font=small, fill=(107, 114, 128), anchor="mm")
d.text((W // 2, 470), "图片压缩 · JSON · PDF · 二维码 · 单位换算 · 密码 · 开发小工具", font=small, fill=(107, 114, 128), anchor="mm")

img.save(OUT)
print("generated", OUT, os.path.getsize(OUT), "bytes")
