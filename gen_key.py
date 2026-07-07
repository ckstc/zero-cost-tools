#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 IndexNow 密钥文件（只需一次）。"""
import os, uuid
ROOT = os.path.dirname(os.path.abspath(__file__))
key = uuid.uuid4().hex + uuid.uuid4().hex[:8]  # 40 hex chars
with open(os.path.join(ROOT, key + ".txt"), "w", encoding="utf-8") as f:
    f.write(key)
print("KEY=", key)
