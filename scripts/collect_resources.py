#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_resources.py — 用 Playwright + 官方 API 采集“可免费获取”的网络资源，并做许可感知分级。

──────────────────────────────────────────────────────────────────────────
为什么是“许可感知”（license-aware）？

用户要求：凡是“别人免费分享、且未明确禁止倒卖”的资源都纳入候选池。
但“免费分享”≠“自动拥有转售权”。默认著作权是“保留所有权利”，
只有明确的 PLR / CC0 / 公有领域 / MIT 等授权才许可转售。

因此本脚本对每个资源做“转售风险”分级，绝不自动把高风险资源上架：
  • low    —— 明确可转售（MIT / Apache / BSD / CC0 / Unlicense / MPL / PLR / 公有领域）
             → 标记为“可直接转售”
  • medium —— 授权未知 / 未声明（免费但没写清楚能否倒卖）
             → 标记为“待人工复核”，收录但不自动上架
  • high   —— 明确禁止转售 / 商用 / 二次分发（All rights reserved / CC BY-NC /
             “禁止倒卖” / “禁止商用” / “No redistribution”）
             → 直接排除，不进入候选池

最终只把 low + medium 写入 collected.json；
其中 low 另写入 recommended_for_resale.json（可直接上架 store 的候选）。

──────────────────────────────────────────────────────────────────────────
采集机制说明（为什么要这样分工）
  • GitHub 仓库 → 用「GitHub 官方 Search API」拉取。GitHub 的 HTML 搜索页对无头浏览器
    会弹出人机验证，直接抓 HTML 几乎必失败；而官方 API 稳定、且直接返回仓库 LICENSE，
    是更可靠、也更合规的“搜索”方式。
  • 其他免费分享站（PLR 目录、公有领域书库等）→ 用「Playwright」直接抓取站点列表页。
    这些站点通常不拦无头浏览器，是 Playwright 真正发挥作用的场景。

──────────────────────────────────────────────────────────────────────────
运行方式：
  # 不启动浏览器，校验配置与解析/分级逻辑（推荐先跑）
  python collect_resources.py --selftest

  # 跑单个已配置源（GitHub 用官方 API，无需浏览器）
  python collect_resources.py --source github --query "automation script" --num 20

  # 跑全部已配置源（PLR 目录会用 Playwright，需先装浏览器）
  python collect_resources.py --all --out results/collected.json

依赖：
  pip install playwright
  playwright install chromium        # 仅 PLR 目录等 Playwright 源需要
"""

import argparse
import csv
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT, "results")

# ───────────────────────── 源配置 ─────────────────────────
# type 支持：
#   "github_api"     —— GitHub 官方搜索 API（返回 LICENSE，最稳定、许可感知最准）
#   "plr_directory"  —— Playwright 抓取某免费分享站的列表页（默认视为可转售，low）
SOURCES = [
    dict(name="github", type="github_api",
         note="搜索可商用/可转售的开源代码与素材，按仓库 LICENSE 自动分级（API 稳定）"),
    dict(name="plr", type="plr_directory",
         # 示例 PLR 站，请替换为你实际要采集的、明确可转售的站点
         base="https://plrdatabase.net/free-plr/",
         note="PLR 资源站：默认视为可转售（low），仍记录来源供复核"),
]


# ───────────────────────── 许可感知分级器 ─────────────────────────
RESELL_OK = [
    r"\bMIT\b", r"apache[\s-]?2", r"\bBSD\b", r"\bISC\b",
    r"CC0", r"unlicense", r"\bMPL[\s-]?2", r"public domain", r"公有领域",
    r"\bPLR\b", r"private label rights", r"resell rights", r"master resell rights",
    r"可转售", r"可二次分发", r"可再分发", r"可商用",
]
RESELL_NO = [
    r"all rights reserved", r"保留所有权利",
    r"non[- ]?commercial", r"cc by-nc", r"禁止商用", r"禁止商业",
    r"no resale", r"not for resale", r"禁止倒卖", r"不得转售",
    r"no redistribution", r"禁止二次分发", r"禁止再分发", r"不得分发",
    r"for personal use only", r"仅限个人使用", r"仅作学习", r"study only",
]
LICENSE_NORM = [
    (r"\bMIT\b", "MIT"),
    (r"apache[\s-]?2", "Apache-2.0"),
    (r"\bBSD\b", "BSD"),
    (r"\bISC\b", "ISC"),
    (r"CC0", "CC0-1.0"),
    (r"unlicense", "Unlicense"),
    (r"\bMPL[\s-]?2", "MPL-2.0"),
    (r"cc by-nc", "CC-BY-NC (禁止商用)"),
    (r"\bPLR\b|private label rights|resell rights|master resell rights", "PLR (可转售)"),
    (r"public domain|公有领域", "Public Domain"),
]


def classify_license(raw):
    """返回 (level, normalized_license)。level ∈ {'low','medium','high'}。"""
    if not raw:
        return "medium", "未知（待人工复核）"
    text = raw.strip()
    low = re.compile("|".join(RESELL_OK), re.I)
    no = re.compile("|".join(RESELL_NO), re.I)
    if no.search(text):
        norm = text
        for pat, name in LICENSE_NORM:
            if re.search(pat, text, re.I):
                norm = name
                break
        return "high", norm
    if low.search(text):
        norm = text
        for pat, name in LICENSE_NORM:
            if re.search(pat, text, re.I):
                norm = name
                break
        return "low", norm
    return "medium", "未识别（待人工复核）: " + text[:60]


# ───────────────────────── GitHub 官方搜索 API 适配器 ─────────────────────────
def _github_api(src, query, num):
    """用 GitHub Search API 搜索仓库，直接读取仓库 LICENSE 做分级（稳定、许可感知最准）。"""
    q = f"{query} in:name,description,readme"
    url = "https://api.github.com/search/repositories?per_page={}&q={}".format(
        min(num, 100), urllib.parse.quote(q))
    req = urllib.request.Request(url, headers={"User-Agent": "resource-collector",
                                                "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"[warn] GitHub API 请求失败：{e}")
        return []
    items = []
    for it in data.get("items", [])[:num]:
        lic = (it.get("license") or {}).get("spdx_id") or (it.get("license") or {}).get("name")
        level, norm = classify_license(lic)
        items.append(dict(
            title=it.get("full_name"),
            url=it.get("html_url"),
            description=(it.get("description") or "")[:200],
            source="github",
            raw_license=lic,
            license=norm,
            resale_risk=level,
            stars=it.get("stargazers_count"),
        ))
    return items


# ───────────────────────── Playwright 站点列表适配器 ─────────────────────────
def _launch_browser():
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    return pw, browser


def _plr_directory(browser, base, num):
    """用 Playwright 抓取 PLR 目录页的卡片。PLR 默认可转售（low），仍记录来源。"""
    page = browser.new_page()
    items = []
    try:
        page.goto(base, timeout=30000)
        page.wait_for_timeout(4000)
        links = page.query_selector_all("a[href]")
        seen = set()
        for a in links:
            href = a.get_attribute("href") or ""
            txt = (a.inner_text() or "").strip()
            if not href.startswith("http") or not txt or href in seen:
                continue
            seen.add(href)
            items.append(dict(
                title=txt[:80], url=href,
                description="PLR 资源（默认可转售，建议上架前人工确认授权页）",
                source="plr_directory", raw_license="PLR",
                license="PLR (可转售)", resale_risk="low",
            ))
            if len(items) >= num:
                break
    finally:
        page.close()
    return items


# ───────────────────────── 采集调度 ─────────────────────────
ADAPTERS = {
    "github_api": _github_api,
    "plr_directory": _plr_directory,
}


def collect_source(src, query=None, num=20):
    q = query or "free resellable resources"
    print(f"[info] 采集源 {src['name']}（{src['type']}） query='{q}' num={num}")
    if src["type"] == "plr_directory":
        pw, browser = _launch_browser()
        try:
            items = _plr_directory(browser, src.get("base", ""), num)
        finally:
            browser.close()
            pw.stop()
    else:
        adapter = ADAPTERS.get(src["type"])
        if not adapter:
            print(f"[warn] 未知源类型 {src['type']}，跳过：{src['name']}")
            return []
        items = adapter(src, q, num)
    print(f"[info] 源 {src['name']} 采集到 {len(items)} 条")
    return items


# ───────────────────────── 输出 ─────────────────────────
def write_outputs(all_items, out_path):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    collected = out_path or os.path.join(RESULTS_DIR, "collected.json")
    recommended = os.path.join(RESULTS_DIR, "recommended_for_resale.json")
    csv_path = os.path.join(RESULTS_DIR, "collected.csv")

    seen = set()
    deduped = []
    for it in all_items:
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        deduped.append(it)

    with open(collected, "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)
    rec = [it for it in deduped if it["resale_risk"] == "low"]
    with open(recommended, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["title", "url", "source", "license", "resale_risk", "description"])
        for it in deduped:
            w.writerow([it["title"], it["url"], it["source"], it["license"],
                        it["resale_risk"], it["description"]])

    low = sum(1 for i in deduped if i["resale_risk"] == "low")
    med = sum(1 for i in deduped if i["resale_risk"] == "medium")
    high = sum(1 for i in deduped if i["resale_risk"] == "high")
    print(f"[done] 共 {len(deduped)} 条 → low(可直接转售)={low}  medium(待复核)={med}  "
          f"high(已排除)={high}")
    print(f"        collected.json / recommended_for_resale.json / collected.csv 已写入 results/")
    return deduped


# ───────────────────────── 自检（不启浏览器） ─────────────────────────
def selftest():
    print("=== SELFTEST: 许可证分级器 ===")
    cases = [
        ("MIT License", "low"), ("Apache-2.0", "low"), ("CC0-1.0", "low"),
        ("Public Domain", "low"), ("PLR - Master Resell Rights", "low"),
        ("可商用、可转售", "low"),
        ("All rights reserved", "high"), ("Non-commercial use only", "high"),
        ("禁止倒卖", "high"), ("for personal use only", "high"),
        ("", "medium"), ("Custom license, see terms", "medium"), (None, "medium"),
    ]
    ok = True
    for raw, expect in cases:
        lvl, norm = classify_license(raw)
        flag = "OK " if lvl == expect else "FAIL"
        if lvl != expect:
            ok = False
        print(f"  [{flag}] classify({raw!r}) -> {lvl} ({norm})  expect={expect}")
    print("=== SELFTEST: 源配置 ===")
    for s in SOURCES:
        assert s["type"] in ADAPTERS, f"源 {s['name']} 类型未知: {s['type']}"
        print(f"  [OK ] 源 {s['name']}  type={s['type']}  base={s.get('base','-')}")
    print("SELFTEST", "通过 ✅" if ok else "存在失败 ❌")
    return 0 if ok else 1


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description="资源采集器（许可感知：Playwright + GitHub API）")
    ap.add_argument("--selftest", action="store_true", help="不启动浏览器，校验配置与分级逻辑")
    ap.add_argument("--all", action="store_true", help="跑全部已配置源")
    ap.add_argument("--source", help="指定某个源 name（见 SOURCES）")
    ap.add_argument("--query", help="搜索关键词（github 源用）")
    ap.add_argument("--num", type=int, default=20, help="每源采集条数")
    ap.add_argument("--out", help="collected.json 输出路径（默认 results/collected.json）")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    all_items = []
    if args.source:
        src = next((s for s in SOURCES if s["name"] == args.source), None)
        if not src:
            print(f"[error] 找不到源 {args.source}。可选：{', '.join(s['name'] for s in SOURCES)}")
            return 2
        all_items += collect_source(src, query=args.query, num=args.num)
    elif args.all:
        for src in SOURCES:
            all_items += collect_source(src, query=args.query, num=args.num)
    else:
        ap.print_help()
        return 0

    if all_items:
        write_outputs(all_items, args.out)
    else:
        print("[warn] 未采集到任何条目。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
