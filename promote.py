#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全自动推广脚本（零账号、零成本）—— 覆盖所有无需登录即可自主提交的渠道：
  1) IndexNow      —— Bing / Yandex / Naver 秒级收录
  2) Sitemap Ping  —— Google / Bing / Yandex 主动提交 sitemap
  3) Ping-O-Matic  —— 向数十个 feed/博客聚合服务广播更新
  4) 开放提交端点 —— Mojeek / Seznam / Gigablast / Entireweb 等（容错，失败不影响）
  5) Wayback       —— 逐页存档到 archive.org，触发爬虫 + 反向链接
仅用 Python 标准库。由定时任务 / WorkBuddy 自动化每日自动运行。
"""
import os, json, glob, urllib.request, urllib.parse, urllib.error, datetime, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://ckstc.github.io/zero-cost-tools/"

# 发现 IndexNow 密钥文件
key_files = [f for f in glob.glob(os.path.join(ROOT, "*.txt"))
             if os.path.basename(f)[:-4].isalnum() and len(os.path.basename(f)[:-4]) >= 32]
KEY = open(key_files[0], encoding="utf-8").read().strip() if key_files else None
KEY_LOC = BASE + KEY + ".txt" if KEY else None

# 动态发现所有工具页（任何含 index.html 的子目录），避免硬编码列表与 build.py 脱节
def discover_slugs():
    slugs = []
    for d in os.listdir(ROOT):
        p = os.path.join(ROOT, d)
        if os.path.isdir(p) and not d.startswith(".") and d not in ("blog",) \
           and os.path.isfile(os.path.join(p, "index.html")):
            slugs.append(d)
    return sorted(slugs)

SLUGS = discover_slugs()

UA = {"User-Agent": "Mozilla/5.0 (compatible; zero-cost-tools/1.0)"}

def all_urls():
    urls = [BASE, BASE + "sitemap.xml", BASE + "atom.xml", BASE + "blog/"]
    for s in SLUGS:
        urls.append(BASE + s + "/")
    blog_dir = os.path.join(ROOT, "blog")
    if os.path.isdir(blog_dir):
        for fn in os.listdir(blog_dir):
            if fn.endswith(".html"):
                urls.append(BASE + "blog/" + fn)
    return urls

def get(url, timeout=20):
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1

def post_json(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1

def sitemap_pings(sitemap_url):
    print("  Sitemap Ping：")
    for name, ep in [
        ("Google", "https://www.google.com/ping?sitemap="),
        ("Bing",   "https://www.bing.com/ping?sitemap="),
        ("Yandex", "https://webmaster.yandex.com/ping?sitemap="),
    ]:
        st = get(ep + urllib.parse.quote(sitemap_url, safe=""))
        print(f"    [{st}] {name} sitemap ping")

def ping_o_matic():
    print("  Ping-O-Matic：")
    params = urllib.parse.urlencode({
        "title": "零成本工具箱",
        "website": BASE,
        "rss": BASE + "atom.xml",
        "chk_bing": "on", "chk_google": "on", "chk_feedburner": "on",
        "chk_technorati": "on", "chk_weblogs": "on", "chk_yahoo": "on",
        "chk_aol": "on", "chk_bloglines": "on", "chk_moreover": "on",
        "chk_msn": "on", "chk_newsgator": "on", "chk_pubsub": "on",
        "chk_rojo": "on", "chk_skybuilders": "on", "chk_syndic8": "on",
        "chk_tailrank": "on",
    })
    for proto in ("https", "http"):
        st = get(f"{proto}://pingomatic.com/ping/?{params}", timeout=25)
        print(f"    [{st}] pingomatic ({proto})")
        if st in (200, 301, 302):
            return
    print("    (pingomatic 未返回成功，忽略)")

def open_engines():
    print("  开放提交端点：")
    smap = urllib.parse.quote(BASE + "sitemap.xml", safe="")
    endpoints = [
        ("Mojeek",     f"https://www.mojeek.com/submit?url={smap}"),
        ("Seznam",     f"https://search.seznam.cz/submit.jsp?url={smap}"),
        ("Gigablast",  f"https://www.gigablast.com/addurl?url={smap}"),
        ("Entireweb",  f"https://www.entireweb.com/addurl/?url={smap}"),
    ]
    for name, url in endpoints:
        st = get(url, timeout=18)
        print(f"    [{st}] {name}")

def wayback_save(url):
    try:
        req = urllib.request.Request("https://web.archive.org/save/" + url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status
    except Exception:
        return -1

def main():
    urls = all_urls()
    print(f"[{datetime.datetime.now():%F %T}] 推广开始，共 {len(urls)} 个 URL")
    if KEY:
        st = post_json("https://api.indexnow.org/indexnow", {
            "host": "ckstc.github.io",
            "key": KEY,
            "keyLocation": KEY_LOC,
            "urlList": urls,
        })
        print(f"  IndexNow -> HTTP {st}")
    else:
        print("  IndexNow -> 未找到密钥文件，跳过")
    sitemap_pings(BASE + "sitemap.xml")
    ping_o_matic()
    open_engines()
    print("  Wayback 存档：")
    ok = bad = 0
    for u in urls:
        code = wayback_save(u)
        if code in (200, 302, 301):
            ok += 1
        else:
            bad += 1
        print(f"    [{code}] {u}")
    print(f"  Wayback 成功 {ok} / 失败 {bad}")
    x_autopost()
    print("推广完成。")

def x_autopost():
    print("  X 自动发帖：")
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "post_x.py")],
                           capture_output=True, text=True, timeout=160)
        for line in (r.stdout + r.stderr).strip().splitlines()[:8]:
            print("    " + line)
    except Exception as e:
        print("    X 发帖跳过：" + str(e)[:160])

if __name__ == "__main__":
    main()
