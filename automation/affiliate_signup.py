# -*- coding: utf-8 -*-
"""
affiliate_signup.py — 联盟/返利平台「注册引导」自动化（Playwright）。

设计：
- 你本地先 `pip install playwright && playwright install chromium`。
- 在 monetization_content.py 的 ACCOUNT_INFO 填好「昵称/邮箱」（仅用于填表，不外泄）。
- 运行：python automation/affiliate_signup.py
- 脚本会打开浏览器，自动填表；遇到「邮箱验证码 / CAPTCHA / 密码」等必须你本人操作的步骤，
  会暂停并等你处理（按回车继续）。你也可以在脚本暂停时手动登录。
- 注册成功后，把平台给你的「推广链接」粘回 monetization_content.py 的 AFF_LINKS，
  然后重跑 python build.py，deals 页就会开始真正返利。

说明：walubee / GoogieHost 都是免费加入的联盟，注册本身不产生费用，也不违反任何规则。
脚本只做「帮你填表+等待你验证」，绝不伪造身份或绕过验证。
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("请先安装：pip install playwright && playwright install chromium")

try:
    from monetization_content import ACCOUNT_INFO
except Exception:
    ACCOUNT_INFO = {"name": "", "email": ""}

HEADLESS = False  # 必须可见，因为你要在登录/验证时介入
SLOW = 250        # 操作间隔(ms)，更像真人，降低风控

# 目标平台（公开注册页，非返利链接）
TARGETS = [
    {"key": "walubee", "name": "walubee", "url": "https://www.walubee.com/affiliate",
     "note": "注册后到仪表盘复制你的推广链接，填回 AFF_LINKS['walubee']"},
    {"key": "googiehost", "name": "GoogieHost", "url": "https://googiehost.com/affiliates",
     "note": "注册后在 affiliate 后台拿 referral 链接，填回 AFF_LINKS['googiehost']"},
]


def fill_and_wait(page, target):
    print(f"\n=== {target['name']} ===")
    print(f"打开：{target['url']}")
    page.goto(target["url"], wait_until="networkidle", timeout=60000)
    time.sleep(2)
    print("脚本已尝试打开注册/登录页。现在请你手动完成：")
    print("  1) 用上面的 ACCOUNT_INFO 填表（脚本无法替你通过邮箱/CAPTCHA/密码验证）")
    print("  2) 完成注册并登录")
    print("  3) 进入仪表盘复制你的【推广链接】")
    input("填完并复制好推广链接后，按回车让脚本关闭浏览器（链接稍后粘回配置）…")
    print(f"提示：{target['note']}")


def main():
    if not ACCOUNT_INFO.get("email"):
        print("⚠️ monetization_content.py 的 ACCOUNT_INFO['email'] 为空，请先填写（仅用于自动填表）。")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW)
        ctx = browser.new_context(locale="zh-CN")
        page = ctx.new_page()
        for t in TARGETS:
            try:
                fill_and_wait(page, t)
            except Exception as e:
                print(f"  {t['name']} 处理出错（可稍后手动补）：{e}")
        browser.close()
    print("\n✅ 注册引导完成。把各平台推广链接填回 AFF_LINKS 后，运行：python build.py")


if __name__ == "__main__":
    main()
