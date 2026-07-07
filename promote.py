#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全自动推广脚本（零账号、零成本）：
  1) IndexNow  —— 把全站 URL 推送给 Bing / Yandex / Naver，秒级收录
  2) Wayback   —— 逐个存档到 archive.org，触发爬虫 + 反向链接
  3) 输出报告
仅用 Python 标准库。由本机定时任务 / WorkBuddy 自动化每日自动运行。
"""
import os, json, glob, urllib.request, urllib.error, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://ckstc.github.io/zero-cost-tools/"

# 发现 IndexNow 密钥文件
key_files = [f for f in glob.glob(os.path.join(ROOT, "*.txt"))
             if os.path.basename(f)[:-4].isalnum() and len(os.path.basename(f)[:-4]) >= 32]
KEY = open(key_files[0], encoding="utf-8").read().strip() if key_files else None
KEY_LOC = BASE + KEY + ".txt" if KEY else None

SLUGS = ["compress","jsonfmt","pdf","qrcode","convert","password",
         "word-counter","case-converter","url-codec","base64-codec","timestamp","markdown"]

def all_urls():
    urls = [BASE, BASE + "sitemap.xml", BASE + "atom.xml", BASE + "blog/"]
    for s in SLUGS:
        urls.append(BASE + s + "/")
    # 博客文章
    blog_dir = os.path.join(ROOT, "blog")
    if os.path.isdir(blog_dir):
        for fn in os.listdir(blog_dir):
            if fn.endswith(".html"):
                urls.append(BASE + "blog/" + fn)
    return urls

def post_json(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode()[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except Exception as e:
        return -1, str(e)[:120]

def wayback_save(url):
    try:
        req = urllib.request.Request("https://web.archive.org/save/" + url,
                                     headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except Exception as e:
        return -1

def main():
    urls = all_urls()
    print(f"[{datetime.datetime.now():%F %T}] 推广开始，共 {len(urls)} 个 URL")
    ok_idx = bad_idx = 0
    if KEY:
        st, msg = post_json("https://api.indexnow.org/indexnow", {
            "host": "ckstc.github.io",
            "key": KEY,
            "keyLocation": KEY_LOC,
            "urlList": urls,
        })
        print(f"  IndexNow -> HTTP {st} {msg}")
    else:
        print("  IndexNow -> 未找到密钥文件，跳过")
    print("  Wayback 存档：")
    for u in urls:
        code = wayback_save(u)
        if code in (200, 302, 301):
            ok_idx += 1
        else:
            bad_idx += 1
        print(f"    [{code}] {u}")
    print(f"  Wayback 成功 {ok_idx} / 失败 {bad_idx}")
    print("推广完成。")

if __name__ == "__main__":
    main()
