# -*- coding: utf-8 -*-
"""
seed_traffic.py — 种子流量自动发布（Playwright）。

你要做的只有一件事：在脚本暂停时登录对应平台。其余（打开页面、填标题/正文、点发布）
脚本自动完成。每条之间随机延时，规避 spam 风控。

前置：
  pip install playwright && playwright install chromium
  （建议用本项目受管 venv）
运行：
  python automation/seed_traffic.py
  # 只发某平台：python automation/seed_traffic.py --only reddit
  # 仅打印文案不真发：python automation/seed_traffic.py --dry

平台：
  reddit  — 发到各 subreddit（先给价值再带链接，符合版规）
  v2ex    — 发到各节点
  zhihu   — 回答指定问题
  weibo   — 发微博
  wechat  — 朋友圈无稳定网页端，脚本只打印文案，你手动粘贴

注意：请勿高频重复发布同一内容，避免被社区/平台限流。本脚本默认每条间隔 30–90 秒。
"""

import sys
import time
import random
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("请先安装：pip install playwright && playwright install chromium")

import promo_content as P

HEADLESS = False
MIN_GAP, MAX_GAP = 30, 90  # 秒，平台间延时


def wait_login(page, url, hint):
    page.goto(url, wait_until="networkidle", timeout=60000)
    print(f"\n[登录] 已打开 {url}")
    print(hint)
    input("→ 请在浏览器里完成登录（如需验证码也在这里处理），登录成功后按回车继续…")


def post_reddit(page):
    for p in P.REDDIT_POSTS:
        url = f"https://www.reddit.com/r/{p['subreddit']}/submit"
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(3)
        try:
            page.fill('textarea[aria-label="Title"]', p["title"], timeout=8000)
            # 切到「Text」标签（如有）并填正文
            try:
                page.click('button:has-text("Text")', timeout=4000)
                time.sleep(1)
            except Exception:
                pass
            page.fill('div[contenteditable="true"][data-lexical-editor="true"]', p["body"], timeout=8000)
            page.click('button:has-text("Post")', timeout=8000)
            print(f"  ✅ reddit r/{p['subreddit']} 已提交")
        except Exception as e:
            print(f"  ⚠️ reddit r/{p['subreddit']} 失败（可手动补）：{e}")
        time.sleep(random.uniform(MIN_GAP, MAX_GAP))


def post_v2ex(page):
    for p in P.V2EX_POSTS:
        url = f"https://www.v2ex.com/new/{p['node']}"
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(3)
        try:
            page.fill('input#title', p["title"], timeout=8000)
            page.fill('textarea#content', p["content"], timeout=8000)
            page.click('input[type="submit"]', timeout=8000)
            print(f"  ✅ v2ex 节点「{p['node']}」已发")
        except Exception as e:
            print(f"  ⚠️ v2ex「{p['node']}」失败：{e}")
        time.sleep(random.uniform(MIN_GAP, MAX_GAP))


def post_zhihu(page):
    for p in P.ZHIHU_ANSWERS:
        print(f"\n[知乎] 问题：{p['question']}")
        print("请在浏览器手动打开该问题页并登录，脚本随后尝试填写。")
        input("→ 打开并登录后按回车，脚本尝试点「写回答」并粘贴…")
        try:
            page.click('button:has-text("写回答")', timeout=6000)
            time.sleep(2)
            page.fill('div[contenteditable="true"]', p["answer"], timeout=8000)
            page.click('button:has-text("发布")', timeout=8000)
            print("  ✅ 知乎回答已发布")
        except Exception as e:
            print(f"  ⚠️ 知乎失败（手动发也可）：{e}")
        time.sleep(random.uniform(MIN_GAP, MAX_GAP))


def post_weibo(page):
    page.goto("https://weibo.com", wait_until="networkidle", timeout=60000)
    for text in P.WEIBO_POSTS:
        try:
            box = page.locator('div[contenteditable="true"]').first
            box.click(timeout=8000)
            box.fill(text, timeout=8000)
            page.click('button:has-text("发送")', timeout=8000)
            print("  ✅ 微博已发")
        except Exception as e:
            print(f"  ⚠️ 微博失败：{e}")
        time.sleep(random.uniform(MIN_GAP, MAX_GAP))


def print_wechat():
    print("\n[朋友圈] 无稳定网页端，请手动粘贴以下文案：")
    for t in P.WECHAT_MOMENTS:
        print("  ·", t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="reddit|v2ex|zhihu|weibo|wechat")
    ap.add_argument("--dry", action="store_true", help="只打印文案，不真发")
    args = ap.parse_args()

    if args.dry:
        print("=== Reddit ==="); [print("·", p["title"]) for p in P.REDDIT_POSTS]
        print("=== V2EX ==="); [print("·", p["title"]) for p in P.V2EX_POSTS]
        print("=== 知乎 ==="); [print("·", p["question"]) for p in P.ZHIHU_ANSWERS]
        print("=== 微博 ==="); [print("·", t) for t in P.WEIBO_POSTS]
        print_wechat()
        return

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=200)
        ctx = browser.new_context(locale="zh-CN")
        page = ctx.new_page()

        if not args.only or args.only == "reddit":
            wait_login(page, "https://www.reddit.com/login", "登录 Reddit（发帖用）。")
            post_reddit(page)
        if not args.only or args.only == "v2ex":
            wait_login(page, "https://www.v2ex.com/", "登录 V2EX（发主题用）。")
            post_v2ex(page)
        if not args.only or args.only == "zhihu":
            post_zhihu(page)
        if not args.only or args.only == "weibo":
            wait_login(page, "https://weibo.com", "登录微博（发博用）。")
            post_weibo(page)
        if not args.only or args.only == "wechat":
            print_wechat()

        browser.close()
    print("\n✅ 种子流量发布完成。后续靠 SEO 长尾持续累积，无需重复手动发。")


if __name__ == "__main__":
    main()
