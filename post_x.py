#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X 平台自动发帖（为工具站引流，最终导向页面内微信收款码）。
基于官方 xurl（X API CLI）。前置条件（一次性人工）：
  1) 在 X 开发者门户免费创建 App -> 拿到 CLIENT_ID / CLIENT_SECRET
  2) 写入 ~/.workbuddy/mcp.json 的 xurl.env（或环境变量）
  3) 运行 `npx -y @xdevplatform/xurl auth oauth2` 完成授权
授权后本脚本每日自动发帖，无需再操作。
无凭证 / 免费层不可发帖时安全跳过（exit 0），供定时任务调用。
"""
import os, sys, json, datetime, subprocess

BASE = "https://ckstc.github.io/zero-cost-tools/"

# 工具亮点池：每条都是免费、本地运行、含微信收款码的卖点
HIGHLIGHTS = [
    ("图片压缩工具", "compress", "一键把 JPG/PNG 压到最小，全程浏览器本地处理，文件不上传、不水印。"),
    ("JSON 格式化工具", "jsonfmt", "粘贴混乱的 JSON 一键美化与校验，接口调试效率翻倍，数据不出本机。"),
    ("PDF 工具箱", "pdf", "在线压缩 PDF、PDF 转图片，纯前端处理，合同证件类文件不怕泄露。"),
    ("二维码生成器", "qrcode", "免费生成网址 / 文本 / WiFi 二维码，保存 PNG 即可打印分享。"),
    ("单位换算器", "convert", "长度重量温度面积在线换算，海淘烹饪工程都好用。"),
    ("密码生成器", "password", "生成高强度随机密码，可自定义长度与字符集，每个网站一把锁。"),
    ("字数统计工具", "word-counter", "实时统计中英文词数、字符、句子、行数，写稿必备。"),
    ("时间戳转换", "timestamp", "Unix 时间戳与日期互转，支持本地与 UTC，排查日志神器。"),
    ("进制转换器", "number-base", "二/八/十/十六进制在线互转，学习计算机基础轻松搞定。"),
    ("文本哈希工具", "hash", "本地生成 SHA-1/256/512 摘要，校验文件完整性不上传。"),
    ("正则表达式测试", "regex", "在线测试正则、高亮匹配结果，写爬虫清洗文本更顺手。"),
    ("CSV JSON 互转", "csv-json", "表格与 JSON 一键互转，首行作表头，数据处理零门槛。"),
    ("UUID 生成器", "uuid", "批量生成 RFC4122 v4 UUID，给资源起名不再撞车。"),
    ("颜色值转换", "color-hex", "HEX/RGB/HSL 互转带取色器，前端切图配色一气呵成。"),
    ("文本对比工具", "text-diff", "逐行对比两段文本差异，改稿找不同高亮一目了然。"),
    ("占位文本生成器", "lorem", "一键生成 Lorem Ipsum 假文，排版设计稿填充超快。"),
    ("罗马数字转换", "roman-numeral", "阿拉伯数字与罗马数字互转，读旧文献、看纪年不再头疼。"),
    ("百分比计算器", "percent-calc", "求百分比、百分比数值、增减百分比，财务日常随手算。"),
    ("金额大写转换", "rmb-upper", "数字金额转中文大写，开票填支票写合同常用，自动处理角分。"),
]


def have_xurl_creds():
    """判断 xurl 是否已具备可用凭证。"""
    if os.path.exists(os.path.expanduser("~/.xurl")):
        return True
    cid = os.environ.get("CLIENT_ID", "")
    csec = os.environ.get("CLIENT_SECRET", "")
    if cid and csec and "REPLACE" not in cid and "REPLACE" not in csec:
        return True
    return False


def post_via_xurl(text):
    """通过 xurl CLI 发推；返回 (ok, message)。"""
    try:
        r = subprocess.run(
            ["npx", "-y", "@xdevplatform/xurl", "-X", "POST", "/2/tweets",
             "-d", json.dumps({"text": text})],
            capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr)
        if r.returncode == 0 and '"data"' in out:
            return True, "posted via xurl"
        return False, out.strip()[:300]
    except Exception as e:
        return False, str(e)[:300]


def main():
    if not have_xurl_creds():
        print("X_CREDENTIALS_MISSING: xurl 未配置凭证，跳过自动发帖。")
        print("启用（一次性人工，之后全自动）：")
        print("  1) X 开发者门户免费创建 App -> 拿 CLIENT_ID/CLIENT_SECRET")
        print("  2) 写入 ~/.workbuddy/mcp.json 的 xurl.env")
        print("  3) 运行 npx -y @xdevplatform/xurl auth oauth2 完成授权")
        print("授权后本脚本每日自动发帖引流，无需再操作。")
        return 0
    today = datetime.date.today()
    name, slug, desc = HIGHLIGHTS[today.toordinal() % len(HIGHLIGHTS)]
    text = f"免费{name}：{desc}\n🔗 {BASE}{slug}/\n#免费工具 #效率 #开发"
    ok, msg = post_via_xurl(text)
    print(("X_POST_OK: " if ok else "X_POST_FAIL: ") + msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
